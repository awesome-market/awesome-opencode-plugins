# Digitale inclusie voor de lokale overheid

Een open skills-repo en kennisdatabank voor Vlaamse steden, gemeenten, OCMW's, bibliotheken, dienstencentra en lokale organisaties die digitale uitsluiting willen verminderen.

Tien skills, acht AI-consultants, zeventien kennisdocumenten en dertien werksjablonen. Alles in het Nederlands, afgestemd op de Vlaamse regelgeving, de Beleidstool Digitale Inclusie en de bronnen van Mediawijs.

> **Peildatum: november 2026.** Cijfers, decreten en subsidieoproepen veranderen. Controleer altijd de actuele bron voor je een beslissing neemt. De volledige bronnenlijst staat in [`kennis/14-bronnen.md`](kennis/14-bronnen.md).

---

## Welk probleem dit oplost

Lokale besturen worstelen zelden met het idee dat digitale inclusie belangrijk is. Ze worstelen met de uitvoering.

- **Je weet niet waar je staat.** Er is geen nulmeting, geen gedeelde definitie en geen zicht op wie je niet bereikt.
- **Je beleidsplan blijft een intentie.** Woorden als "digitale inclusie" staan in het meerjarenplan, maar zonder trekker, budgetlijn of indicator.
- **Een digipunt opstarten duurt maanden.** Locatie, bemensing, aanbod, toeleiding en kwaliteit worden ad hoc beslist.
- **Je digihelpers vallen uit.** Werving lukt, omkadering en opvolging niet.
- **Je moet een beslissing verdedigen** en hebt geen kostenraming, geen financieringsmix en geen meetplan.

Deze skills leveren per probleem een concreet, beslisbaar document — geen algemeen advies.

## Waarom een skill en geen losse prompt

- **Waarde:** Vlaamse context (decreet lokaal bestuur, meerjarenplan, VVSG, Mediawijs, Digibanken), vaste werkwijzen met stappen, outputs en kwaliteitschecks, en een kennisbasis die de skill verplicht raadpleegt.
- **Zonder de skill:** een model schrijft een generiek plan, verzint cijfers, slaat de Vlaamse financiering over en levert geen indicator of actor op.
- **Wat je wint:** elke skill eindigt met een vaste outputlijst, een kwaliteitscheck en een lijst veelgemaakte fouten.

---

## De tien skills

| Skill | Waarvoor | Wat je krijgt |
| :--- | :--- | :--- |
| [`digitale-inclusie-scan`](skills/digitale-inclusie-scan/SKILL.md) | Een snelle, onderbouwde nulmeting | Ingevulde scan, synthese van 1-2 pagina's, prioriteitenlijst, lijst ontbrekende data |
| [`beleidsplan-digitale-inclusie`](skills/beleidsplan-digitale-inclusie/SKILL.md) | Een beleidsnota en actieplan van visie tot indicatoren | Beleidsnota, actietabel, budgettabel, risico's, beslissingsvraag |
| [`meerjarenplan-analyse`](skills/meerjarenplan-analyse/SKILL.md) | Het MJP en de budgetten screenen op verankering | Screeningstabel, synthese, aanpassingsvoorstel, concept raadsvoorstel |
| [`digipunt-opzetten`](skills/digipunt-opzetten/SKILL.md) | Een digipunt of computerruimte ontwerpen en opstarten | Digipuntplan, kostenraming, draaiboek, kwaliteitschecklist |
| [`digihelper-werking`](skills/digihelper-werking/SKILL.md) | Digihelpers werven, opleiden en omkaderen | Profiel en mandaat, wervingsplan, opleidingsplan, afsprakennota, opvolging |
| [`doelgroepanalyse-en-outreach`](skills/doelgroepanalyse-en-outreach/SKILL.md) | Wie je niet bereikt, en hoe je hen wel bereikt | Doelgroepanalyse, vindplaatsen- en toeleiderskaart, persona's, outreachplan |
| [`communicatieplan-digitale-inclusie`](skills/communicatieplan-digitale-inclusie/SKILL.md) | Een communicatieplan dat mensen doet komen | Boodschappentabel, kanalenmix, planning, meetplan, voorbeeldmateriaal |
| [`e-inclusie-businesscase`](skills/e-inclusie-businesscase/SKILL.md) | Kosten, baten en financiering verdedigen | Businesscase, kostenraming, financieringsmix, verankerings- en exitstrategie |
| [`toegankelijkheidsaudit`](skills/toegankelijkheidsaudit/SKILL.md) | Website, formulier, app of loket testen op WCAG 2.2 AA | Auditrapport met bewijs, prioriteitenlijst, herstelplan, concept verklaring |
| [`okf-kennisbundel`](skills/okf-kennisbundel/SKILL.md) | De kennisbank uitbreiden zonder de structuur te breken | Concept met frontmatter, bronnen, bijgewerkte index en log, groene validatie |

Elke skill volgt dezelfde opbouw: wanneer gebruiken, welke inputs je nodig hebt, de stappen, de output, een kwaliteitscheck en de veelgemaakte fouten.

## Wanneer gebruik je deze repo

- "Waar staat onze gemeente op het vlak van digitale inclusie?"
- "Schrijf een beleidsnota digitale inclusie voor 20.000 inwoners."
- "Staat digitale inclusie in ons meerjarenplan?"
- "We willen een digipunt in de bibliotheek. Wat kost dat?"
- "Hoe werven en begeleiden we digihelpers?"
- "Onze campagne bereikt de juiste mensen niet."
- "Is ons aanvraagformulier toegankelijk?"
- "Inwoners haken af bij hun verhuis. Waar loopt het mis?"

## Verwachte output

Elke skill levert een document dat je kan indienen, bespreken of verdedigen: een nota, een plan, een draaiboek, een auditrapport of een raadsvoorstel. Steeds met actor, timing, budgetindicatie en minstens één meetbare indicator.

## Wat je zelf aanlevert

De skills verzinnen niets. Ze hebben context nodig:

- Type bestuur of organisatie en aantal inwoners of bereik.
- Bestaande werking: digipunt, digihelpers, beleid, budget.
- Doelgroepen en hun kenmerken.
- Gewenste output en deadline.
- Documenten die je al hebt: meerjarenplan, beleidsnota's, cijfers van je loketten.

Ontbreekt die context, dan werkt de skill met expliciete aannames en markeert ze die.

## Voorbeeldprompts

```text
"Doe een digitale-inclusie-scan voor een gemeente van 18.000 inwoners zonder digipunt. Ik heb alleen een lijst van bestaande initiatieven."
"Screen het meerjarenplan 2026-2031 van onze stad op digitale inclusie en maak een raadsvoorstel voor de wijziging 2027."
"Maak een businesscase voor een digipunt in de hoofdbibliotheek: 12 uur per week, twee vrijwilligers, eenmalige investering in toestellen."
"Ons bereik bij 65-plussers blijft laag. Maak een doelgroepanalyse en een outreachplan met drie kanalen."
"Audit ons formulier 'aanvraag premie' op WCAG 2.2 AA en geef een herstelplan met eigenaars."
```

---

## Installatie

### OpenCode (aanbevolen)

```bash
git clone https://github.com/HansF/digitale-inclusie-lokale-overheid.git
cd digitale-inclusie-lokale-overheid
opencode
```

De repo bevat een `opencode.json` dat `skills/` als skillbron registreert, en de acht consultants in `.opencode/agents/` worden automatisch geladen. Je kan de skills ook expliciet laden met `@digitale-inclusie-scan` of door een consultant bij naam te vragen.

### Claude Code en andere Agent Skills-tools

Kopieer of link de skills naar je persoonlijke map:

```bash
git clone https://github.com/HansF/digitale-inclusie-lokale-overheid.git
cp -r digitale-inclusie-lokale-overheid/skills/* ~/.claude/skills/
```

Of houd ze in de repo en verwijs ernaar vanuit je project. Elke map met een `SKILL.md` is één skill; de mapnaam is het ID.

### skills.sh

```bash
npx skills add https://github.com/HansF/digitale-inclusie-lokale-overheid
```

### Zelf inzetten in je eigen project

Wil je de kennisbasis lokaal houden maar de skills elders gebruiken? Kopieer `skills/` én `kennis/` en `materiaal/` samen: de skills verwijzen naar de kennisdocumenten en de sjablonen met een pad vanaf de repo-root.

---

## De kennisdatabank

De skills zijn het speelveld; de kennisbank is de ondergrond. De skills verwijzen expliciet naar deze documenten in plaats van zelf cijfers te verzinnen.

Begin bij [`kennis/index.md`](kennis/index.md) of bij [`materiaal/index.md`](materiaal/index.md): dat zijn de vaste ingangen van de twee OKF-bundels.

### Kennis

| Document | Inhoud |
| :--- | :--- |
| [`00-startHier.md`](kennis/00-startHier.md) | Leeswijzer en routekaart door de kennisbank |
| [`01-wat-is-digitale-inclusie.md`](kennis/01-wat-is-digitale-inclusie.md) | Begrippen, definities en de vier voorwaarden |
| [`02-cijfers-en-onderzoek.md`](kennis/02-cijfers-en-onderzoek.md) | Cijfers met bron en peildatum |
| [`03-doelgroepen.md`](kennis/03-doelgroepen.md) | Wie dreigt uitgesloten te worden en waarom |
| [`04-beleid-en-regelgeving.md`](kennis/04-beleid-en-regelgeving.md) | Decreten, meerjarenplan, Vlaams en lokaal beleid |
| [`05-lokale-regierol.md`](kennis/05-lokale-regierol.md) | Regie, netwerk, mandaat en verankering |
| [`06-vier-voorwaarden-en-bouwstenen.md`](kennis/06-vier-voorwaarden-en-bouwstenen.md) | Het denkkader: vier voorwaarden, vijf bouwstenen |
| [`07-digipunten.md`](kennis/07-digipunten.md) | Soorten digipunten, locatie, bemensing, kwaliteit |
| [`08-digihelpers.md`](kennis/08-digihelpers.md) | Vrijwillig, professioneel en doelgroepgericht helpen |
| [`09-toegankelijke-dienstverlening.md`](kennis/09-toegankelijke-dienstverlening.md) | WCAG, klare taal, click-call-connect |
| [`10-financiering-en-subsidies.md`](kennis/10-financiering-en-subsidies.md) | Financieringsmix en subsidielogica's |
| [`11-monitoring-en-impact.md`](kennis/11-monitoring-en-impact.md) | Indicatoren, meting en bijsturing |
| [`12-organisaties-en-partners.md`](kennis/12-organisaties-en-partners.md) | Wie doet wat in Vlaanderen |
| [`13-ai-en-digitale-inclusie.md`](kennis/13-ai-en-digitale-inclusie.md) | AI als nieuwe kloof en als hulpmiddel |
| [`14-bronnen.md`](kennis/14-bronnen.md) | Alle bronnen met URL |
| [`15-instrumenten-en-campagnes.md`](kennis/15-instrumenten-en-campagnes.md) | Beleidstool, toolbox mensgericht ontwerpen, DigiCheck, databank, huisstijl en Digitale Week |
| [`16-levensgebeurtenissen.md`](kennis/16-levensgebeurtenissen.md) | Dienstverlening herontwerpen rond momenten als verhuizen, geboorte en jobverlies |

### Materiaal

| Sjabloon | Waarvoor |
| :--- | :--- |
| [`00-meting-digitale-inclusie.md`](materiaal/00-meting-digitale-inclusie.md) | Nulmeting en zelfevaluatie |
| [`beleids-en-actieplan-template.md`](materiaal/beleids-en-actieplan-template.md) | Beleidsnota en actietabel |
| [`bouwstenen-canvas.md`](materiaal/bouwstenen-canvas.md) | Canvas op de vijf bouwstenen |
| [`stakeholder-en-netwerkanalyse.md`](materiaal/stakeholder-en-netwerkanalyse.md) | Stakeholders en toeleiders in kaart |
| [`digipunt-draaiboek.md`](materiaal/digipunt-draaiboek.md) | Draaiboek voor een digipunt |
| [`communicatieplan-digistarters.md`](materiaal/communicatieplan-digistarters.md) | Communicatieplanformat |
| [`toegankelijkheidschecklist.md`](materiaal/toegankelijkheidschecklist.md) | Checklist voor een audit |
| [`kpi-en-monitoringskader.md`](materiaal/kpi-en-monitoringskader.md) | Indicatoren en opvolging |
| [`raadsvoorstel-template.md`](materiaal/raadsvoorstel-template.md) | Raadsvoorstel of collegebesluit |
| [`digihelper-profiel-en-vacature.md`](materiaal/digihelper-profiel-en-vacature.md) | Profiel, vacature en selectie |
| [`uitleendienst-reglement-en-contract.md`](materiaal/uitleendienst-reglement-en-contract.md) | Uitleen van toestellen |
| [`leveranciers-en-partners.md`](materiaal/leveranciers-en-partners.md) | Leveranciers en partners vergelijken |
| [`klantreis-canvas.md`](materiaal/klantreis-canvas.md) | Invulblad om één levensgebeurtenis te doorlichten: keten, reis, breekpunten, herontwerp, meting |

## De consultants

Acht subagents voor OpenCode, in [`.opencode/agents/`](.opencode/agents/). Ze werken met dezelfde kennisbank en dezelfde werkafspraken, en hebben elk een eigen rol en toon.

| Consultant | Waarvoor |
| :--- | :--- |
| `programmamanager-e-inclusie` | Een integraal programma leiden, governance, netwerkregie en verankering |
| `beleidsadviseur-digitale-inclusie` | Beleidsnota's, actieplannen, MJP-analyses en bestuurlijke adviezen |
| `digipunt-architect` | Een digipunt, computerruimte of uitleendienst ontwerpen |
| `toegankelijkheidsauditor` | WCAG-audits, klare taal, formulierentests, inclusief ontwerp |
| `doelgroep-en-outreach-strateeg` | Doelgroepen prioriteren en digistarters bereiken |
| `digihelper-coach` | Digihelpers werven, opleiden, omkaderen en evalueren |
| `financiering-en-subsidies` | Kostenramingen, businesscases en financieringsmix |
| `communicatieadviseur` | Communicatieplannen, kanalenkeuze en toegankelijke communicatie |

De consultants zijn OpenCode-specifiek. De skills zijn overdraagbaar naar elke tool die de Agent Skills-standaard volgt.

---

## Structuur

```text
digitale-inclusie-lokale-overheid/
├── README.md                     ← je bent hier
├── AGENTS.md                     ← werkafspraken voor AI-consultants
├── LICENSE                       ← CC BY-NC-SA 4.0
├── okf-base.yaml                 ← bundelmanifest voor okflint
├── opencode.json                 ← registreert skills/ als skillbron
├── skills/                       ← tien skills, elk met een SKILL.md
│   ├── digitale-inclusie-scan/
│   ├── beleidsplan-digitale-inclusie/
│   ├── meerjarenplan-analyse/
│   ├── digipunt-opzetten/
│   ├── digihelper-werking/
│   ├── doelgroepanalyse-en-outreach/
│   ├── communicatieplan-digitale-inclusie/
│   ├── e-inclusie-businesscase/
│   ├── toegankelijkheidsaudit/
│   └── okf-kennisbundel/
├── templates/
│   └── skill-template/           ← vertrekpunt voor een nieuwe skill
├── tests/
│   ├── validate_skills.py        ← controle op frontmatter, naam en links
│   └── validate_okf.py           ← OKF-conformiteit van de kennisbank
├── kennis/                      ← OKF-bundel: zeventien kennisdocumenten
│   ├── index.md                  ← begin hier
│   ├── log.md                    ← wijzigingen, nieuwste eerst
│   └── 00-startHier.md … 16-levensgebeurtenissen.md
├── materiaal/                   ← OKF-bundel: dertien sjablonen en checklists
│   ├── index.md
│   ├── log.md
│   └── …
├── .github/
│   ├── workflows/                ← validatie bij elke push en pull request
│   └── ISSUE_TEMPLATE/           ← meld een fout of stel een skill voor
└── .opencode/
    └── agents/                   ← acht consultants
```

### Waarom staat de kennisbank naast de skills en niet erin?

Een skill is één werkwijze; de kennisbank is gedeelde inhoud. `kennis/` en `materiaal/` staan daarom één keer in de repo en de skills verwijzen ernaar met een pad vanaf de repo-root. Zo staat elk cijfer op één plaats en veroudert het niet in negen kopieën.

### Open Knowledge Format

De kennisbank volgt de [Open Knowledge Format-specificatie (OKF v0.2)](https://github.com/GoogleCloudPlatform/open-knowledge-format). OKF is een open, leverancieronafhankelijke manier om kennis als markdown met YAML-frontmatter te publiceren: geen SDK, geen database, alleen bestanden die je met `cat` kan lezen.

`kennis/` en `materiaal/` zijn elk een **bundel** met een vaste ingang (`index.md`) en een wijzigingslog (`log.md`). Elk document is één **concept**:

```yaml
---
type: kennisdocument
title: "Digipunten"
description: "Een digipunt opzetten of verbeteren: locatie, aanbod, …"
tags: [digipunt, toegang, fysieke-dienstverlening]
stale_after: 2027-06-30T00:00:00Z
sources:
  - resource: "https://www.mediawijs.be/nl/artikels/hoe-organiseer-je-een-digipunt"
---
```

Wat dat oplevert:

| Veld | Waarom het er staat |
| :--- | :--- |
| `type` | Het enige verplichte veld. Maakt onderscheid tussen kennisdocument, sjabloon, canvas, checklist en draaiboek. |
| `title`, `description` | Wat een agent of lezer ziet voor hij het document opent. |
| `tags` | Cross-cutting categorieën, zodat je over thema's heen kan filteren. |
| `sources` | De bronnen waarop het document steunt. Elke URL komt uit de tekst zelf; er is niets bijverzonnen. |
| `stale_after` | Vanaf wanneer de inhoud als verouderd geldt. Staat op de cijfer-, beleids-, financierings- en bronnendocumenten. |

Twee dingen zijn bewust **niet** ingevuld: `generated` en `verified`. We weten van de bestaande documenten de oorspronkelijke auteur en datum niet, en een reviewer heeft ze niet een voor een gevalideerd. Die velden invullen zou schijnzekerheid geven. Wie een document vandaag reviewt, kan ze toevoegen:

```yaml
verified: { by: human:hans, at: 2026-11-13T10:00:00Z }
```

De verwijzingen tussen documenten zijn gewone markdown-links, zodat de kennisbank één navigeerbaar netwerk is in plaats van losse bestanden.

**Conformiteit controleren:**

```bash
python3 tests/validate_okf.py
```

Die controle kijkt of elk concept een `type` heeft, of `index.md` en `log.md` de juiste structuur hebben, of er geen links stuk zijn, en waarschuwt wanneer een document verouderd is volgens `stale_after`. De controle faalt op fouten, niet op waarschuwingen.

## Een skill toevoegen

1. Kopieer `templates/skill-template/` naar `skills/<nieuwe-skill>/`.
2. Geef de map een kebab-case naam; die naam wordt het skill-ID en moet gelijk zijn aan `name` in de frontmatter.
3. Schrijf de beschrijving als een trigger: welk probleem, en wanneer moet een agent de skill laden.
4. Houd de vaste secties aan: wanneer gebruiken, inputs, stappen, output, kwaliteitscheck, veelgemaakte fouten.
5. Voer de validatie uit en open een pull request.

```bash
python3 tests/validate_skills.py
```

Dezelfde controle draait in GitHub Actions bij elke push en pull request.


## Kwaliteitsprincipes

1. **Vertrek bij de burger, niet bij de dienst.** Betrek digistarters en hun netwerk bij onderzoek, ontwerp en evaluatie.
2. **Digitaal waar het kan, menselijk waar het moet.** Blijf click-call-connect aanbieden: digitaal, telefonisch en face-to-face.
3. **Werk transversaal.** Digitale inclusie raakt welzijn, burgerzaken, communicatie, ICT, personeel, cultuur, onderwijs en economie.
4. **Denk in ecosystemen.** Een lokaal bestuur alleen kan het niet: bibliotheken, OCMW, Ligo, SAAMO, Digibanken, verenigingen en vrijwilligers.
5. **Meet en stuur bij.** Zonder nulmeting en opvolging blijft beleid een intentie.

## Wat deze repo niet doet

- **Geen verzonnen cijfers, subsidies, wetten of contactgegevens.** Ontbreekt een cijfer, dan zegt de skill dat en verwijst ze naar de bron.
- **Geen juridisch bindend advies.** Voor aanbestedingen, GDPR, staatssteun en subsidievoorwaarden ga je naar je jurist, financiële dienst of subsidiegever.
- **Geen beslissing over individuele burgers.** Verwijs door naar de juiste dienst.
- **Geen politieke kleur.** Opties komen met voor- en nadelen, niet met één ideologisch voorkeursmodel.

## Bijdragen

Verbeteringen zijn welkom: een verouderd cijfer, een ontbrekende bron, een skill die een stap mist, een sjabloon dat in de praktijk niet werkt. Open een issue via de templates of een pull request met wat je wijzigt en waarom. Voeg bij cijfers altijd de bron en de peildatum toe, en voer beide controles uit voor je indient:

```bash
python3 tests/validate_skills.py
python3 tests/validate_okf.py
```

## Licentie

De inhoud valt onder [CC BY-NC-SA 4.0](LICENSE): hergebruik met naamsvermelding, niet-commercieel, en deel afgeleiden onder dezelfde voorwaarden. Dat sluit aan bij de licentie van de Mediawijs-bronnen waarop de kennisbank steunt.

Bij hergebruik verwijs je naar de oorspronkelijke bronnen in [`kennis/14-bronnen.md`](kennis/14-bronnen.md), niet naar deze repo als bron van de cijfers.
