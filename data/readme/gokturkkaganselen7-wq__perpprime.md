# PerpPrime

### Agent-native perpetual futures desk — powered by CFOS

Kripto vadeli işlemler (perpetual futures) için **taşınabilir, ajan-native bir
trading workspace'i**. OpenCode, Claude Code ve Codex gibi kodlama ajanları MCP
üzerinden fiyat okur, analiz eder, plan kurar ve **emir açabilir**.

- **CCXT** tabanlı: Bybit, Binance USDⓈ-M, OKX, KuCoin Futures ve CCXT'nin
  desteklediği diğer venue'lar.
- **Paper varsayılan**: anahtar gerekmez, gerçek para riski yok.
- **Fail-closed risk kernel**: veri yoksa, state okunamıyorsa veya kill switch
  açıksa emir gitmez.
- **24 crypto-native skill**: CANSLIM/VCP/13F gibi hisse senedi kalıpları
  yerine funding, likidasyon, rejim, basis ve 7/24 execution odaklı.
- **Tek emir yolu**: market giriş + reduce-only stop + reduce-only TP.

> **Uyarı:** Kripto vadeli işlemler kaldıraçlıdır ve bakiyenin tamamını
> kaybettirebilir. Bu depo bir eğitim/otomasyon altyapısıdır, yatırım tavsiyesi
> değildir. Canlıya geçmeden `docs/LIVE_CHECKLIST.md` dosyasını eksiksiz
> doldurun.

---

## 60 saniye kurulum

```bash
cd cfos
uv venv .venv
uv pip install --python .venv/bin/python ccxt pytest
cp .env.example .env          # paper için düzenleme gerekmez
./bin/cfos doctor
./bin/cfos demo               # entry -> stop -> journal, tam paper döngüsü
```

`cfos demo` gerçek ağa çıkmaz; deterministik fiyatlarla çalışır ve
`data/demo/<zaman>/` altında kendi SQLite defterini üretir.

### Ortam değişkenleri

| Değişken | Varsayılan | Açıklama |
|---|---|---|
| `CFOS_MODE` | `paper` | `paper` \| `testnet` \| `live` |
| `CFOS_VENUE` | `bybit` | CCXT exchange id |
| `CFOS_EQUITY` | `10000` | Paper başlangıç bakiyesi |
| `CFOS_API_KEY` | — | Trade-only anahtar (çekim yetkisi yok) |
| `CFOS_API_SECRET` | — | Anahtar sırrı |
| `CFOS_LIVE_ACK` | — | Canlı için `I_UNDERSTAND_REAL_MONEY` |
| `CFOS_HOME` | repo kökü | `config/` içeren dizin |
| `CFOS_DATA_DIR` | `./data` | SQLite + paper state |
| `CFOS_KILL_FILE` | `data/KILL` | Kill switch dosyası |

---

## Ajanlara bağlama

Üç ajan da aynı MCP sunucusunu konuşur: `python -m cfos mcp` (stdio).

### OpenCode

`opencode.json` hazır. Proje kökünde `opencode` başlatın; `cfos` araçları
otomatik görünür. Yollar taşınırsa dosyadaki mutlak yolları güncelleyin.

### Claude Code

`.mcp.json` hazır; `.claude/skills -> ../skills` bağlantısı kurulu.

```bash
claude mcp list
claude mcp get cfos
```

### Codex

`~/.codex/config.toml` içine ekleyin (yolları kendi checkout'unuza göre
düzeltin):

```toml
[mcp_servers.cfos]
command = "/home/gokturkkaganselen7/opencodetrading/cfos/.venv/bin/python"
args = ["-m", "cfos", "mcp"]
env = { PYTHONPATH = "/home/gokturkkaganselen7/opencodetrading/cfos/src", CFOS_HOME = "/home/gokturkkaganselen7/opencodetrading/cfos", CFOS_MODE = "paper" }
```

Codex talimatları proje kökündeki `AGENTS.md` üzerinden okur.

### Doğrulama

Ajanın ilk çağrısı `cfos_doctor` olmalı; `status: OK` veya `WARN` dönmeli.
Ardından `cfos_status` ile equity ve kill switch kontrol edilir.

---

## Komutlar

```bash
cfos doctor                     # ortam ve güvenlik kontrolleri
cfos status --json              # equity, drawdown, heat, kill switch
cfos route --text "kırılım"     # niyet -> skill zinciri + kapılar
cfos market BTC/USDT:USDT --json
cfos regime BTC/USDT:USDT --tf 4h --json
cfos candles BTC/USDT:USDT --tf 1h --limit 120 --json

cfos size --symbol BTC/USDT:USDT --side long --entry 65000 --stop 64000 --json
cfos plan --symbol BTC/USDT:USDT --side long --entry 65000 --stop 64000 \
  --tp 67000 --tp 68500 --intent trend --out /tmp/plan.json --json

cfos execute --plan /tmp/plan.json --dry-run --json   # kapıları gör
cfos execute --plan /tmp/plan.json --json             # paper emir

cfos positions --json
cfos close BTC/USDT:USDT --qty 0.025 --json
cfos tick BTC/USDT:USDT 64000 --json                  # paper stop/TP tetikle
cfos kill --reason "manual" | cfos kill --release
cfos journal --limit 50 --json
cfos review --limit 100 --json
cfos mcp                                              # MCP stdio sunucusu
```

### MCP araçları (15)

| Araç | İş |
|---|---|
| `cfos_status` | Hesap, pozisyon, kill switch, performans |
| `cfos_doctor` | Kurulum ve güvenlik kontrolü |
| `cfos_market` | Fiyat, funding, OI, hacim, spread |
| `cfos_regime` | Trend/range/squeeze/chaos sınıflandırması |
| `cfos_route` | Niyet → zincir + kapılar |
| `cfos_size` | Risk bazlı miktar (emir yok) |
| `cfos_plan` | Bracket planı (emir yok) |
| `cfos_execute` | Kapılardan geçerse bracket emir |
| `cfos_positions` | Açık pozisyonlar |
| `cfos_close` | Reduce-only kapatma |
| `cfos_tick` | Paper fiyat tick'i + senkron |
| `cfos_kill` | Kill switch aç |
| `cfos_unkill` | Kill switch kapat |
| `cfos_journal` | İşlem günlüğü |
| `cfos_review` | Performans özeti |

---

## 24 skill

| Katman | Skill'ler |
|---|---|
| **T0 — Kapı ve durum** | `cfos-router`, `cfos-risk-gate`, `cfos-portfolio-state`, `cfos-data-quality` |
| **T1 — Rejim ve veri** | `cfos-regime`, `cfos-derivatives-sentiment`, `cfos-liquidation-map`, `cfos-macro-calendar` |
| **T2 — Setup** | `cfos-trend`, `cfos-breakout`, `cfos-mean-reversion`, `cfos-funding-carry`, `cfos-liquidation-reversal`, `cfos-grid`, `cfos-news-catalyst` |
| **T3 — Doğrulama** | `cfos-backtest`, `cfos-walk-forward`, `cfos-edge-review` |
| **T4 — Uygulama** | `cfos-sizing`, `cfos-execution`, `cfos-exit-management` |
| **T5 — Geri bildirim** | `cfos-journal`, `cfos-postmortem` |
| **TR — Operasyon** | `cfos-ops` |

Her skill `skills/<ad>/SKILL.md`; router registry'si `skills/cfos-router/SKILL.md`
içinde ve `make audit` ile denetlenir.

---

## Risk modeli

`config/risk.toml` tek doğruluk kaynağıdır. Varsayılanlar:

| Limit | Değer |
|---|---|
| İşlem başına risk | %0.50 equity |
| Günlük zarar durdurucu | %2.00 |
| Haftalık zarar durdurucu | %5.00 |
| Maksimum drawdown | %10.00 |
| Kaldıraç (pozisyon ve portföy) | 3.0x |
| Açık pozisyon | 3 |
| Sembol başına | 1 |
| Portföy heat | %3.00 |
| Küme başına pozisyon | 2 |
| Günlük işlem | 6 |
| Minimum R:R | 2.0 |
| Veri tazeliği | 120 sn |
| Spread | 8 bps (16 bps BLOCK) |

Emir akışı her zaman bracket'tır: market giriş → reduce-only stop → reduce-only
take-profit merdiveni. TP seviyeleri, gerçek dolu miktarı venue minimumuna ve
adımına göre dilimlere böler (TP1 yarısı, TP2 kalanı). Market emri yanıtı
`status`/`filled` taşımıyorsa `confirm_entry` emri sorgular; kısmi fill'de
bracket dolu miktar üzerine kurulur ve rapor uyarı taşır. Fill doğrulanamazsa
`ERROR` döner ve venue'da pozisyon varsa savunmacı kapatma denenir; bracket
kurulamazsa acil kapatma emri otomatik gönderilir.

Detay: `docs/SAFETY.md`.

---

## Testler

```bash
make test          # pytest, ağ erişimi yok
make audit         # skill registry drift denetimi
make demo          # paper lifecycle
make doctor        # ortam kontrolü
```

Testler `paper` moduna ve geçici veri dizinine zorlanır; hiçbir test gerçek
emir göndermez.

---

## Backtest

`scripts/backtest_trend.py` trend kurallarını gerçek Bybit perpetual verisinde
test eder: funding maliyeti, 5.5 bps taker + 2 bps kayma, look-ahead yok
(sinyal kapanışta, fill sonraki bar açılışında), walk-forward ve ablasyon.

```bash
PYTHONPATH=src .venv/bin/python scripts/backtest_trend.py --mode single \
  --symbols BTC/USDT:USDT ETH/USDT:USDT SOL/USDT:USDT --timeframes 1h \
  --start 2025-11-14 --end 2026-11-14 --warmup-days 75

PYTHONPATH=src .venv/bin/python scripts/backtest_trend.py --mode walkforward \
  --symbols BTC/USDT:USDT --start 2025-11-01 --end 2026-11-14 \
  --train-days 90 --test-days 30 --step-days 30
```

Sonuçlar, karşılaştırmalar ve ölçülmeyen riskler:
**[docs/BACKTEST.md](docs/BACKTEST.md)**.

---

## Depo düzeni

```
cfos/
├── AGENTS.md, CLAUDE.md          # ajan talimatları
├── opencode.json, .mcp.json      # MCP bağlantıları
├── bin/cfos                      # başlatıcı (PYTHONPATH ayarlı)
├── config/                       # risk.toml, universe.toml
├── scripts/                      # backtest_trend.py (funding + walk-forward)
├── skills/                       # 24 SKILL.md + registry audit
├── src/cfos/                     # Python çekirdeği
├── tests/                        # pytest
├── docs/                         # SAFETY, LIVE_CHECKLIST, ARCHITECTURE, BACKTEST
└── data/                         # SQLite + paper state (git dışı)
```

---

## v1 sınırları (dürüst liste)

- Yerleşik `cfos backtest` komutu **yok**; sayı üretmek için
  `scripts/backtest_trend.py` kullanılır. `cfos-backtest`/`cfos-walk-forward`
  skill'leri bu script olmadan sonuç uydurmaz.
- Execution tek sembol ve tek yön (one-way mode) varsayar; hedge mode yok.
- Funding/OI **tarihsel serisi** yok; yalnızca anlık snapshot.
- Grid otomasyonu yok; grid planı seviye seviye manuel/agent emri gerektirir.
- Spot bacağı ayrı yönetilir; carry stratejisi delta-neutral otomatik değildir.
- Orderbook derinliği sınırlı (5 seviye) okunur; market impact modeli yok.
- `paper` doldurmaları deterministiktir, gerçek slippage dağılımını taklit
  etmez.

Bu sınırlar bilinçli: v1 güvenli, denetlenebilir ve taşınabilir olmayı
hedefler; kapsam genişliğini değil.
