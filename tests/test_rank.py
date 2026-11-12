"""Unit tests for scripts/rank.py — pure board/window math.

Synthetic fixtures only; no network, no repo data. Run:
    python -m unittest discover -s tests -v
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import rank  # noqa: E402


def row(stars, forks=10, watchers=5, created="2020-01-01T00:00:00Z",
        lang="Python", is_fork=0, is_arch=0):
    """Minimal 11-col snapshot row (name col unused inside rank helpers)."""
    return ("o/r", stars, forks, watchers, 0, 0, 0, created, lang, is_fork, is_arch)


def mk_ridx(series):
    """{name: [(day, row), ...]} -> rank.py ridx {name: (days, tuples)}"""
    out = {}
    for name, seq in series.items():
        out[name] = ([d for d, _ in seq], [r for _, r in seq])
    return out


D1, D2, D3, D8 = "2026-01-01", "2026-01-02", "2026-01-03", "2026-01-08"
DAYS = [D1, D2, D3, D8]
DAY_INDEX = {d: i for i, d in enumerate(DAYS)}


class TestClosestDay(unittest.TestCase):
    def test_exact_and_before(self):
        self.assertEqual(rank.closest_day(DAYS, D3), D3)
        self.assertEqual(rank.closest_day(DAYS, "2026-01-05"), D3)
        self.assertEqual(rank.closest_day(DAYS, "2025-12-31"), D1)  # clamps to first
        self.assertEqual(rank.closest_day(DAYS, D8, before=D8), D3)
        self.assertEqual(rank.closest_day(DAYS, "2026-01-04", before=D8), D3)


class TestBoardBaseDay(unittest.TestCase):
    def test_nominal_hit_and_fallback(self):
        # daily nominal = day-1 → D8-1 = 2026-01-07 missing → closest < day is D3
        b, w, approx = rank.board_base_day(DAYS, D8, 1)
        self.assertEqual((b, w), (D3, 5))
        self.assertFalse(approx)                   # 5d window ≥ nominal → not approx
        b, w, approx = rank.board_base_day(DAYS, D3, 1)
        self.assertEqual((b, w), (D2, 1))
        self.assertFalse(approx)

    def test_short_window_is_approx(self):
        # monthly at D8: target 2025-12-09 → before all days → fallback to days[0]
        b, w, approx = rank.board_base_day(DAYS, D8, 30)
        self.assertEqual((b, w), (D1, 7))
        self.assertTrue(approx)                    # 7d < nominal 30d → approx

    def test_first_day_falls_back_to_itself(self):
        # no valid base before the first day → base = days[0], 0-day window
        b, w, approx = rank.board_base_day(DAYS, D1, 1)
        self.assertEqual((b, w), (D1, 0))
        self.assertTrue(approx)


class TestRepoBaseNear(unittest.TestCase):
    def test_nearest_in_window(self):
        # repo day closest to base_day, restricted to repo-days < day
        ridx = mk_ridx({"a/b": [(D1, row(10)), (D2, row(20)), (D8, row(50))]})
        got = rank.repo_base_near(ridx, "a/b", D1, D8)
        self.assertEqual(got[0], D1)               # D1 is closest to base D1
        self.assertEqual(rank.repo_base_near(ridx, "a/b", D3, D8)[0], D2)
        self.assertIsNone(rank.repo_base_near(ridx, "a/b", D2, D1))


class TestComputeBoards(unittest.TestCase):
    def setUp(self):
        self.ridx = mk_ridx({
            # stars AND forks/watchers grow every snapshot
            "a/grow": [(D1, row(100, forks=10, watchers=5)),
                       (D2, row(150, forks=12, watchers=6)),
                       (D3, row(200, forks=15, watchers=8)),
                       (D8, row(400, forks=30, watchers=20))],
            # flat — no growth boards
            "a/flat": [(D1, row(500)), (D8, row(500))],
            # fork — excluded everywhere
            "a/fork": [(D1, row(10, is_fork=1)), (D8, row(9999, is_fork=1))],
            # new repo, appears only at D8
            "a/new":  [(D8, row(120, created="2026-01-05T00:00:00Z"))],
            # dead — last seen 2025-12-15, >14d before D8 → out of the pool
            "a/dead": [("2025-12-15", row(300))],
        })
        self.meta = {n: {} for n in self.ridx}

    def boards(self, day):
        return rank.compute_boards(day, DAYS, self.ridx, self.meta, DAY_INDEX)

    def test_daily_growth(self):
        b = self.boards(D8)
        names = [e["full_name"] for e in b["daily"]["items"]]
        self.assertEqual(names, ["a/grow"])
        e = b["daily"]["items"][0]
        self.assertEqual(e["growth"], 200)         # 400-200 over D3→D8
        self.assertFalse(e["approx"])              # repo base hit board base exactly

    def test_ineligible_and_stale(self):
        b = self.boards(D8)
        all_names = {e["full_name"] for v in b.values() for e in v["items"]}
        self.assertNotIn("a/fork", all_names)      # fork excluded
        self.assertNotIn("a/dead", all_names)      # past stale grace

    def test_new_board(self):
        b = self.boards(D8)
        names = [e["full_name"] for e in b["new"]["items"]]
        self.assertIn("a/new", names)              # created within 90d, >=20★
        self.assertNotIn("a/grow", names)          # created 2020 — too old
        self.assertNotIn("a/flat", names)          # created 2020

    def test_metric_boards(self):
        b = self.boards(D8)
        self.assertEqual([e["full_name"] for e in b["daily_downloads"]["items"]],
                         ["a/grow"])               # 10→30 forks over the window
        self.assertEqual(b["daily_downloads"]["items"][0]["growth"], 15)
        self.assertEqual([e["full_name"] for e in b["daily_dl_yday"]["items"]],
                         ["a/grow"])

    def test_lang_filter(self):
        ridx = dict(self.ridx)
        ridx["a/go"] = ([D1, D8], [row(50, lang="Go"), row(90, lang="Go")])
        meta = dict(self.meta, **{"a/go": {}})
        b = rank.compute_boards(D8, DAYS, ridx, meta, DAY_INDEX, lang="Go")
        all_names = {e["full_name"] for v in b.values() for e in v["items"]}
        self.assertEqual(all_names, {"a/go"})

    def test_total_board(self):
        b = self.boards(D8)
        names = [e["full_name"] for e in b["total"]["items"]]
        self.assertEqual(names[0], "a/flat")       # 500★ top despite 0 growth


class TestDebutBoard(unittest.TestCase):
    RIDX = mk_ridx({
        "a/grow": [(D1, row(100)), (D8, row(400))],
        "x/new":  [(D8, row(80))],
    })
    META = {"a/grow": {}, "x/new": {}}

    def test_first_appearance_ranked(self):
        items = rank.compute_debut_board({"x/new", "a/grow"}, D8, DAYS,
                                         self.RIDX, self.META, DAY_INDEX)["items"]
        self.assertEqual(items[0]["full_name"], "a/grow")   # growth → first
        self.assertEqual(items[-1]["full_name"], "x/new")   # no base → tail
        self.assertIsNone(items[-1]["growth"])

    def test_empty_seen(self):
        self.assertEqual(rank.compute_debut_board(set(), D8, DAYS, self.RIDX,
                                                  self.META, DAY_INDEX),
                         {"items": []})


class TestLangSlug(unittest.TestCase):
    def test_specials(self):
        self.assertEqual(rank.lang_slug("C++"), "cpp")
        self.assertEqual(rank.lang_slug("C#"), "csharp")
        self.assertEqual(rank.lang_slug("Jupyter Notebook"), "jupyter-notebook")
        self.assertEqual(rank.lang_slug("Python"), "python")
        self.assertEqual(rank.lang_slug("Objective-C"), "objc")


if __name__ == "__main__":
    unittest.main()
