# opencode-skill-assemblea

**Assemblea V5 — Intelligent Hybrid Debate Engine**

Multi-agente asimmetrico per dibattiti strutturati tra modelli AI su OpenCode. Convoca 4-6 personaggi con modelli e ruoli diversi, genera proposte parallele, le sottopone a critica con l'Avvocato del Diavolo, e produce un verbale finale con decisione architettu­rale.

---

## Indice

- [Quick Start](#quick-start)
- [Il Cast](#il-cast)
- [Come Funziona](#come-funziona)
- [Triage e Modalità](#triage-e-modalità)
- [Moduli Specialistici](#moduli-specialistici)
- [Memoria Storica](#memoria-storica-rag)
- [Metriche di Chiusura](#metriche-di-chiusura)
- [Quando Usarla](#quando-usarla)
- [Esempi](#esempi)
- [Fallback Python](#fallback-python)
- [Requisiti](#requisiti)
- [Limitazioni](#limitazioni)

---

## Quick Start

Invocazione su OpenCode (OhMyOpenCode):

```
Assemblea: progetta un'architettura per il nuovo sistema di logging
```
```
Dibattito: usiamo PostgreSQL o MongoDB per la nuova piattaforma?
```
```
Brainstorming: come riscrivere da zero il sistema di routing?
```

L'Assemblea analizza automaticamente la complessità del problema, seleziona la modalità appropriata (Light/Standard/Full/Esplorazione), convoca i personaggi necessari e produce un verbale strutturato.

---

## Il Cast

| Ruolo | Modello | Categoria | Competenza |
|-------|---------|-----------|------------|
| **Presidente** | deepseek-v4-flash | — | Moderatore, orchestra il dibattito |
| **L'Hacker** | kimi-k2.7-code | `quick` | Proposte concrete, coding |
| **Il Contabile** | minimax-m3 | `deep` | Numeri, costi, ROI |
| **L'Utente** | minimax-m3 | `deep` | Voce del cliente, semplicità |
| **L'Avvocato del Diavolo** | deepseek-v4-flash | `ultrabrain` | Critica puntuale, anti-sycophancy |
| **Lead Architect** | deepseek-v4-flash | `ultrabrain` | Sintesi finale e verbale |

### Mappa Modelli

| Modello | Contesto | Assegnato a |
|---------|----------|-------------|
| kimi-k2.7-code | 256K token | Hacker — coding specialist |
| minimax-m3 | 1M token | Contabile, Utente — analitico |
| deepseek-v4-flash | 1M token | Avvocato, Lead Architect |
| deepseek-v4-pro | 1M token | ❌ **MAI in assemblea** (cold start 5-10s) |

### Regole Ferree

- **MAI** delegare modelli locali a dibattiti — non sanno farlo
- **MAI** usare deepseek-v4-pro nell'Assemblea
- **SEMPRE** Avvocato per ultimo nel dibattito (antisycophancy)
- **SEMPRE** registrare obiezioni non risolte nel verbale

---

## Come Funziona

### Flusso di Esecuzione

```
Triage → Calcolo Complessità → Selezione Modalità
    ↓
Convocazione (OdG + Task Plan)
    ↓
┌─ Hacker ─┐
├─ Contabile ┤── PARALLELO → Avvocato (asincrono: parte al primo risultato)
└─ Utente ──┘
    ↓
Dibattito (sequenziale, max 2 giri + controreplica Avvocato)
    ↓
Moduli Specialistici (se attivati)
    ↓
Lead Architect → Verbale Finale
```

### Fasi nel Dettaglio

1. **Triage** — Calcolo complessità del problema, selezione automatica della modalità
2. **Convocazione** — Stampa dell'Ordine del Giorno e Task Plan
3. **Proposte Parallele** — Hacker, Contabile e Utente generano proposte indipendentemente. L'Avvocato parte **asincrono** non appena il primo risultato arriva
4. **Dibattito** — 2 giri sequenziali di replica, Avvocato ultimo
5. **Moduli Specialistici** — Attivati solo se i trigger matchano (vedi sotto)
6. **Lead Architect** — Sintesi finale, verbale, decisione, allegato tecnico

### Avvocato Asincrono

Feature chiave dell'Assemblea V5: invece di attendere TUTTE le 3 proposte parallele, l'Avvocato inizia a criticare SUBITO dopo il PRIMO risultato, accumulando gli altri via continuation session (`ses_...`). Questo riduce i tempi morti del 20-30%.

---

## Triage e Modalità

### Formula di Complessità

```
Base:     min(parole_input × 0.3, 2.0)
Segnali:  count(keyword_match) × 0.5
Tech:     count(API, SQL, GPU, CPU, DB, Cloud, deploy) × 0.3
Numeri:   count(digits) × 0.2
Totale:   min(Base + Segnali + Tech + Numeri, 10.0)
```

### Soglie

| Punteggio | Modalità | Partecipanti | Timeout |
|-----------|----------|-------------|---------|
| < 4 | **Light** | Hacker + Utente + Lead | 60s |
| 4-6 | **Standard** | Hacker + Contabile + Utente + Avvocato + Lead | 90s |
| 6-8 | **Full** | Tutti e 6 + moduli specialistici | 120s |
| > 8 | **Full + Esteso** | Tutti + moduli + analisi supplementare | 150s |
| Trigger condizionale | **Esplorazione** | Design divergente, Hacker unbound | 120s |

### Modalità Esplorazione

Attivata da **segnali di divergenza** (brainstorming, esplora, pensiero laterale, blue sky) **E assenza di urgenza** (nessun crash, budget, deadline, failure).

In questa modalità:
- **Hacker** genera idee senza limiti di lunghezza, organizzate per categoria e numerate
- **Avvocato** applica solo un **survival filter**: elimina le idee matematicamente/fisicamente/economica­mente impossibili (FATAL FLAW)
- **Lead Architect** clusterizza le idee sopravvissute per strategia (basso rischio, sperimentali, alta complessità/alta resa)

---

## Moduli Specialistici

Attivazione automatica basata su segnali nel problema + soglia di complessità:

| Modulo | Trigger | Funzione |
|--------|---------|----------|
| **The Infiltrator** | ≥ 2 segnali security E complessità ≥ 5 | Identifica 3 bias cognitivi o difetti argomentativi nel dibattito |
| **The Time Traveler** | ≥ 2 segnali scalabilità E complessità ≥ 6 | Proietta l'impatto delle decisioni a 12-24 mesi, valuta reversibilità |
| **Chaos Simulator** | "failure/mission-critical" E complessità ≥ 7 | Introduce 2 guasti forzati e obbliga un piano B documentato |

Se attivati, i moduli sono **bloccanti**: il Lead Architect non produce il verbale senza i loro output.

---

## Memoria Storica (RAG)

Prima di ogni assemblea, il Presidente cerca verbali di assemblee precedenti su argomenti simili tramite la skill `knowledge` (`explore` agent su pattern `verbale`/`assemblea`).

Se trova risultati, li inietta nel prompt dell'Avvocato e del Lead Architect come:

```
--- DECISIONI PRECEDENTI (da verbali archiviati) ---
<risultati_ricerca>
--- FINE DECISIONI PRECEDENTI ---
```

Questo evita di dibattere soluzioni già scartate o ripetere errori già discussi.

---

## Metriche di Chiusura

| Metrica | Descrizione |
|---------|-------------|
| Durata stimata | Tempo totale in minuti |
| Turni totali | Numero di interventi |
| Voci attive / totali | Partecipanti che hanno effettivamente parlato |
| Obiezioni sollevate | Critiche dell'Avvocato |
| Obiezioni non risolte | Critiche rimaste senza risposta |
| Decisioni precedenti trovate | Memoria storica attivata |
| Decisione finale | Accettata / Rimandata |

**Quality Gate**: se l'Avvocato solleva < 3 obiezioni → anti-sycophancy check ("Sei sicuro? Non c'è niente da criticare?"). Se obiezioni non risolte > 50% → la decisione è fragile, raccomanda rimandare.

---

## Quando Usarla

| Scenario | Assemblea V5 | Assemblea Complessa |
|----------|-------------|---------------------|
| Decisione veloce (< 2 minuti) | ✅ | ❌ |
| Problema con dati numerici | ✅ | ✅ |
| Brainstorming creativo | ✅ (modalità Esplorazione) | ❌ |
| Scelta tecnologica | ✅ | ✅ (più approfondita) |
| Decisione con rischio medio-alto | ✅ | ✅✅ |
| Piano di migrazione | ✅ | ✅✅ |
| Tracciabilità delle decisioni | ✅ | ✅✅ (mappa RRC) |

> Per decisioni che richiedono **iterazione profonda** e meccanismo **Recalibrate/Reject/Concede**, usa [Assemblea Complessa](https://github.com/motusakapeppo/opencode-skill-assemblea-complessa).

---

## Esempi

### Esempio 1: Problema Tecnico Complesso (Full)

```
Utente: "Fai un'assemblea per progettare l'architettura del nuovo
microservizio di autenticazione con JWT, refresh token rotation,
e supporto multi-tenant su Kubernetes"

Output: 3 proposte Hacker, analisi costi Contabile, critiche Avvocato,
decisione architetturale finale con allegato tecnico.
```

### Esempio 2: Decisione di Design (Standard)

```
Utente: "Dibattito: usiamo PostgreSQL o MongoDB per il nuovo
sistema di logging?"

Output: Confronto costi/benefici, critica delle assunzioni, decisione motivata.
```

### Esempio 3: Esplorazione (Modalità Divergente)

```
Utente: "Brainstorming senza limiti: come potremmo riscrivere
da zero l'intero sistema di routing dei messaggi?"

Output: Decine di idee categorizzate, filtrate per impossibilità,
clusterizzate per strategia strategica.
```

---

## Fallback Python

`debate_orchestrator.py` è uno script Python standalone per ambienti **senza OpenCode**. Esegue l'Assemblea via chiamate dirette API cloud. **Non supporta** parallelismo reale né la modalità Esplorazione.

```bash
# Prerequisito
export OLLAMA_API_KEY="la-tua-chiave"

# Uso base
python debate_orchestrator.py "Progetta un sistema di caching distribuito"

# Con timeout personalizzato
python debate_orchestrator.py "Refactoring del modulo auth" --timeout 90

# Con contesto di codice (auto-slimming)
python debate_orchestrator.py "Analizza il codice" --code src/auth/service.py
```

---

## Struttura del Repository

```
opencode-skill-assemblea/
├── README.md                               # Documentazione
├── SKILL.md                                # Skill definition OpenCode
├── debate_orchestrator.py                  # Fallback Python standalone
├── proiezione_24mesi_time_traveler.md      # Esempio di output Time Traveler
└── .gitignore
```

---

## Requisiti

- **OpenCode** (OhMyOpenCode) — per l'uso principale via sub-agenti cloud
- **Python 3.10+** — solo per il fallback standalone
- **Variabile d'ambiente** `OLLAMA_API_KEY` — solo per il fallback standalone
- **Modelli cloud**: kimi-k2.7-code, minimax-m3, deepseek-v4-flash

---

## Limitazioni

1. **Fallback Python sequenziale** — i 3 personaggi partono uno dopo l'altro, non in parallelo. 2-3× più lento dell'esecuzione OpenCode nativa.
2. **Modalità Esplorazione solo su OpenCode** — non disponibile nel fallback Python.
3. **deepseek-v4-pro escluso** — cold start 5-10s, distruttivo per l'interattività.
4. **Niente modelli locali** — i modelli locali (Qwen, Gemma, Llama) non producono dibattiti di qualità. Usare solo cloud.

---

## Licenza

Apache 2.0