# Exam Hall Allocation System

Web application for allocating exam halls and seats, running the resit timetable from an
office-entered roster, and directing students and invigilators to their venues.

The project is a React + TypeScript single-page app backed by a Node/Express API and a
Supabase Postgres database, plus an optional Python service for crowding predictions.

---

## Requirements

| Tool | Version | Needed for |
| --- | --- | --- |
| Node.js | 20 or newer | frontend and API |
| npm | 10 or newer | installing dependencies |
| PostgreSQL | 14 or newer, or a Supabase project | the database |
| Python | 3.11 | optional ML crowding service |

---

## Install

```bash
npm install
cp .env.example .env      # then fill in the values, see below
```

---

## Configuration

`.env` is read by both Vite and the API. Values marked **required** have no sensible
default and the API will refuse to start without them.

### Required

| Variable | Purpose |
| --- | --- |
| `SUPABASE_DB_URL` | Postgres connection string. On Supabase use the **session pooler** (port `5432`) and URL-encode the password. `DATABASE_URL` is accepted as an alias. |
| `JWT_SECRET` | Signs auth tokens. Generate one with `node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"`. |

### Usually set

| Variable | Default | Purpose |
| --- | --- | --- |
| `PORT` | `3002` | API port |
| `CLIENT_ORIGIN` | `http://localhost:5173` | CORS origin allowed to call the API |
| `VITE_API_URL` | `http://localhost:3002/api` | API base URL used by the browser |
| `APP_URL` | `http://localhost:5173` | absolute base URL used to build links in emails and notifications |

### Optional

The app runs fully without any of these; each only enables an extra capability.

| Variable | Effect when empty |
| --- | --- |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_SECURE`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM` | Password-reset emails are written to a simulated inbox instead of being sent. `SMTP_PASS` needs a 16-character Google App Password. |
| `VITE_GOOGLE_MAPS_API_KEY` | Campus Locator uses free OpenStreetMap tiles, which need no billing account. |
| `SERP_API_KEY` | "Nearby places" search in the campus map is hidden. |
| `ML_SERVICE_URL`, `VITE_ML_SERVICE_URL` | Crowding predictions are unavailable and the UI hides them. |

> `VITE_`-prefixed variables are bundled into the browser code. Never put a secret in
> one. `SMTP_PASS` and `DATABASE_URL` are server-only and must not be prefixed with
> `VITE_`.

---

## Database setup

Schema changes are **numbered migrations** in `backend/migrations/`. They are applied in
order, each in its own transaction, and recorded in a `_migrations` table. Every
statement is idempotent, so running them against a database that already exists is safe
and only applies what is missing.

```bash
npm run db:migrate          # apply pending migrations
npm run db:migrate:status   # show applied / pending
npm run db:seed             # insert demo users, courses, halls, enrolments
npm run db:setup            # migrate + seed, for a new machine
```

Useful flags:

```bash
node backend/migrate.js --dry-run    # print statements without touching the database
node backend/migrate.js --force      # re-apply a migration whose file was edited
node backend/migrate.js --emit-schema  # regenerate backend/schema.sql
```

`backend/schema.sql` is a **generated** concatenation of the migration files, kept for
people who prefer to paste a schema into the Supabase SQL editor. Do not edit it by hand
— run `npm run db:schema`. A test fails if it drifts from the migrations.

To add a schema change, create the next numbered file in `backend/migrations/` and run
`npm run db:migrate`. Do not edit a migration that has already been applied; the runner
refuses to proceed if a recorded checksum no longer matches, unless you pass `--force`.

---

## The resit flow

A resit is not something a student asks for. The examinations office already knows who
is resitting, so the flow is **data entry first, scheduling second**, and the student
only ever reads the result.

```
office imports the roster  →  office places the students  →  everyone reads the timetable
      (pending)                    (scheduled)
```

There is no approval step. An imported row lands as `pending` and can be placed
immediately; `approved` still works for rows that predate the import path.

### Importing the roster

`POST /api/resit/requests/import` (admin only) takes rows of
`{ registration_number, course_code }` — one row per student and the course they are
sitting. Students and courses are **matched, never created**: a roster naming somebody
the system has never heard of is a list the office got wrong, not a request to enrol
them.

Rows that resolve commit; rows that do not come back in `problems` with the spreadsheet
line they were on, so a partly-wrong file still lands everything it got right. An
unexpected database error rolls the whole file back.

**The wizard shows its column mapping and lets the office correct it.** Headings are
guessed (`Index`/`Paper` will not be recognised, `Reg No` will), and every column is
listed with a dropdown of `registration_number`, `course_code`, `course_title` or
*ignore this column*. Changing one re-previews the rows immediately, so a department
whose spreadsheets call the same thing different names does not have to reformat the
file first. A field can only be filled from one column — pointing a second column at a
field already taken releases the first, so the wrong students can never be imported
silently. A sheet the parser did not recognise as a roster is still read as one, with
the same columns to check, rather than refused.

### What a placement is

**A resit placement is a hall, not a desk.** The `resit_seat_allocations` row per student
is what attendance is recorded against, but its `row_number`/`col_number` are `NULL`, as
are the segment's `row_start`/`row_end`/`col_start`/`col_end`. The invigilator works down
the roll by name and the student takes any free place. A legacy seated segment still
fills those columns and keeps its seat label.

A hall is therefore measured by `exam_capacity ?? total_capacity`, not by a desk grid —
a desk grid would let the office pack a hall to the last place on the last row.

**Scheduling is one transaction.** For every paper in the selected batch it will, or
will not, do all of:

1. reuse the active resit paper for the course, or create `<COURSE>-R1`;
2. register each student on that paper;
3. reuse the session for that date and time, or create it;
4. check the hall has room **for that sitting**;
5. create one **segment** — a paper sitting in one hall — and place each student;
6. recompute the segment's head count;
7. mark the requests `scheduled`.

A failure anywhere rolls the whole batch back, so a half-scheduled sitting cannot exist.

### How the timetable is shaped

- A **session** is a date and time (`resit_sessions`). Several papers share one.
- A **segment** is one paper in one hall for one session (`resit_session_papers`), and
  the invigilator staffing it.
- A **placement** is a student in a segment (`resit_seat_allocations`).

Two rules are worth knowing because they are easy to get wrong:

- **A hall is filled for a sitting, not for a day.** The same hall can host a morning and
  an afternoon resit. The capacity check is therefore scoped to the hall *and the start
  time* (`assertHallCapacity` matches the segment's `session_start`), so a hall used last
  week is free today.
- **Two papers can share a hall and a sitting.** They share the floor, not a place in it,
  so the second paper is not a double booking. Hall capacity is the constraint that keeps
  a shared sitting inside the room.

### Who can read and write what

| Audience | Endpoint | Sees |
| --- | --- | --- |
| Admin | `GET /api/resit/timetable` | every session, every segment, every student |
| Invigilator | `GET /api/resit/timetable/mine` | only the segments they are staffing |
| Student | `GET /api/resit/my-seating` | only the placements they personally hold |

The invigilator scope is taken from the token, never the query, and it is applied to the
segment *and* placement queries — filtering only the session list would have handed each
invigilator a colleague's roster. The same scope gates
`POST /api/resit/timetable/segments/:id/attendance`, and it is checked against
`resit_session_papers.supervisor_id`, the same field the "mine" view uses, because a
session can be shared between papers while each segment still has one invigilator.

### Marking the roll

| Method | Endpoint | Who |
| --- | --- | --- |
| One student | `POST /api/resit/timetable/segments/:segmentId/attendance` | admin, invigilator |
| The whole roll | `POST /api/resit/timetable/segments/:segmentId/attendance/bulk` | admin, invigilator |

Statuses are `present`, `absent` and `malpractice`, matching the column's CHECK. There
is no QR resit attendance: a student is found by name in a hall, not by scanning a
numbered desk, so the method is recorded as `manual` whatever the caller sends.

---

## Campus map and walking directions

A walking route is only as good as its two ends. The destination is an exam hall, whose
pin an administrator places on the map. The origin is the person, and that turned out to
be the weak end: the map used to fall back to an **IP location guess** whenever the phone
had no GPS fix, which is city-level — roughly ten kilometres. It never failed visibly, it
just produced a confident-looking route from the wrong place.

The rule now is that a wrong origin must be *visibly* wrong.

| Situation | Route starts from | What the person sees |
| --- | --- | --- |
| GPS fix accurate to 100 m or better | the live position | nothing; it is simply their location |
| No fix, or a fix worse than 100 m | their saved start point | a banner saying the fallback is in use and why |
| No saved start point | the campus default (main gate) | a banner asking them to save a start point |
| Nothing known at all | no route | an explanation instead of a guess |

An IP fix is never used as a route origin. It is still used for one thing: noticing that
the device is tens of kilometres from campus, which is worth saying and useless for
routing.

**Arrival times are withheld when the origin cannot support one.** If the start point is
only accurate to 400 m and the walk is 120 m, "3 minutes" is noise, so no time is shown
instead. A saved landmark or pin is a known place and always supports a time.

### Placing pins

An administrator opens **Data Center → Campus Map Template** and places every hall and
landmark by clicking the map:

- **Halls** are moved with `PATCH /api/halls/:id/position`, which writes only the two
  coordinates. A mis-click cannot overwrite capacity, seating or the written directions.
- **Landmarks** are the named places people can start from — gates, hostels, car parks.
  Exactly one is the campus default (`uq_campus_landmarks_single_default` enforces it).
- **A pin outside the campus is refused** with a message saying how far out it was. A pin
  in the wrong place is worse than no pin, because it produces a confident wrong answer.

Removing a landmark goes to the **recycle bin**, not straight to deletion, so a pin
somebody depends on can be restored.

### Saving a start point

Each person saves one start point, in the map panel or by map view: a named landmark, a
pin of their own, or nothing. It is meant to be set once in a place with signal rather
than repeatedly during a walk through a building. Coordinates are stored on the user
alongside the landmark id, so a route can still be drawn if the landmark is later
recycled — the UI then says so and asks them to pick a new one.

---

## Running

Three processes, each in its own terminal:

```bash
npm run dev        # frontend  → http://localhost:5173
npm run api        # API       → http://localhost:3002
npm run ml-service # optional  → http://localhost:8000
```

Check the API came up:

```bash
curl http://localhost:3002/api/health     # {"ok":true}
```

### Demo logins

Seeded by `npm run db:seed`:

| Registration number | Password | Role |
| --- | --- | --- |
| `ADMIN01` | `admin` | admin |
| `INV01` | `invig` | invigilator |
| `STU001` | `student` | student |

The seed refuses to finish if the stored password hashes do not match these, so a
successful `db:seed` means the documented credentials work.

---

## Verifying an install

```bash
npm test              # 928 tests, frontend and backend
npx tsc --noEmit      # type check
npm run build         # production bundle
```

`npm test` runs the whole suite from the repository root, backend tests included: the
`.mjs` files under `backend/__tests__/` import Vitest, so `node --test` will not load
them.

There is a live check for the resit timetable, which runs against a started API
and a real database and removes everything it created afterwards:

```bash
npm run api            # in one terminal
node e2e-resit.mjs     # in another
```

It walks the office's own flow — import a roster including rows that cannot resolve,
re-import it, place the entries in a hall, try to overfill that hall, let the invigilator
mark the roll, try to mark a colleague's sitting — and checks the student only ever sees a
hall and never a seat.

---

## Deploying

1. `npm ci && npm run build` — the build runs `tsc --noEmit` first, so a type error
   fails the build instead of shipping.
2. Serve `dist/` from a static host and proxy `/api` to the Express process. The
   frontend uses a client-side router, so configure a **SPA fallback** that rewrites
   unknown paths to `index.html` (e.g. nginx `try_files $uri /index.html`,
   Netlify `_redirects: /* /index.html 200`, or Vercel's `rewrites`). `server.js` is
   API-only and does not serve the SPA.
3. Run the API with `NODE_ENV=production`. In production `JWT_SECRET` is required
   (the process refuses to start without it) and the rate limiters are enabled.
   Set `CLIENT_ORIGIN` to the deployed frontend origin and `APP_URL` to the public
   URL so emailed links resolve.
4. Set `VITE_API_URL` at build time if the API is on another origin; leave it as
   `/api` when the static host proxies to the API on the same origin.

---

## npm scripts

| Script | Does |
| --- | --- |
| `dev` | Vite dev server |
| `build` / `preview` | production build / serve the build |
| `api` | start the API |
| `db:migrate` | apply pending migrations |
| `db:migrate:status` | report applied vs pending |
| `db:schema` | regenerate `backend/schema.sql` from the migrations |
| `db:seed` | seed demo data |
| `db:setup` | `db:migrate` + `db:seed` |
| `test` / `test:watch` | run the test suite |
| `ml-service` / `ml-train` | crowding prediction service / retrain models |
| `host:phone` | expose the dev server on the local network for phone testing |

---

## Project layout

```
backend/
  server.js            Express app: routes, middleware, error handling
  db.js                Postgres pool
  migrate.js           versioned migration runner
  migrations/          numbered, idempotent SQL migrations
  schema.sql           generated from migrations/ — do not edit
  seed.js              demo users, courses, halls, enrolments
  controllers/         request handling
  services/            business logic
  middleware/          auth, validation, rate limiting
  __tests__/           API and schema tests
src/
  pages/               one file per screen
  components/          reusable UI
  lib/apiClient.ts     HTTP client for the API
  lib/mockApi.ts       browser data layer; falls back to localStorage
  lib/seedData.ts      demo data for the browser store
  lib/routeOrigin.ts   decides where a route starts (see Campus map)
  lib/campusPins.ts    pin validation and campus bounds
scripts/               operational helpers
ml-service/            optional Python crowding prediction service
```

---

## How data is stored

This matters when reading the code, because the application is **mid-migration** from a
browser-first design to a server-backed one.

- The API exposes **126 routes**. The browser data layer (`src/lib/mockApi.ts`) offers
  roughly **150 operations**, of which a handful are server-backed — the resit request
  queue, the resit timetable and notifications. The rest read and write `localStorage` and
  are visible only in that browser.
- So halls, courses, enrolments, scheduling, attendance, and venues are still
  browser-local. Signing in on a second device shows different data for those areas.
  Resit requests, allocations, and notifications are shared through the database.
- `src/lib/mockApi.ts` tries the API first and falls back to the browser store, so the
  app keeps working offline. That fallback is why the local-only areas are not obvious
  from the UI.

Planned work, in order: migrate halls, academic setup, users/enrolment, then scheduling
to the API; then add recycle bins for deleted records; then UI and accessibility cleanup.

---

## Known limitations

- **Indoor directions are generated, not surveyed.** `src/lib/indoorGraph.ts` builds a
  corridor/stairwell graph procedurally from the hall list, so routes follow a plausible
  layout rather than real surveyed floor plans. The `campus_nodes` and `campus_edges`
  tables exist in the schema for stored floor plans, but nothing reads or writes them yet.
- **The production bundle is a single ~2.1 MB chunk.** It works but would load faster
  split by route.
- **Notifications link to their resit application through `client_key`, not a foreign
  key** — `notifications.related_application_id` is currently always null.
- **Offline login ships demo credentials in the bundle.** `src/lib/seedData.ts` contains
  bcrypt hashes for `ADMIN01`, `INV01` and `STU001`, and they end up in the built
  JavaScript. When the API is unreachable, `mockApi.login` verifies against that local
  snapshot and issues an offline token. The server still rejects bad credentials with a
  401, which is not retried locally — but anyone who can read the bundle can log in as
  the seeded admin *while the API is down*. This is what makes the "works offline"
  feature work. Before exposing a real deployment, remove the seeded users from
  `MOCK_DATA` or gate the offline fallback behind a build flag.
- **The resit timetable is read-only in the UI.** Scheduling writes the paper, session,
  segment and placement, and the office, invigilator and student all read that back, but
  there is no drag-and-drop or "move this paper to another hall" screen. The browser
  mirror still has the older bulk generator, which edits localStorage directly.
- **Resit attendance is a roll call, not a scan.** A resit segment carries
  `supervisor_id` and its placements carry `attendance_status`, and the invigilator
  dashboard marks a student present, absent or for malpractice one button at a time or
  a whole segment at once. It is deliberately not the main exam `LiveSeatGrid` path: a
  resit placement has no numbered desk to scan, so a QR flow would have nothing to read.
- The database connection uses Supabase's session pooler. The pool handles idle
  disconnects, but very high concurrency would want the transaction pooler or direct
  connections.
