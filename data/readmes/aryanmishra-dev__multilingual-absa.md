---
title: Multilingual ABSA
emoji: 🎯
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.14.0
app_file: app.py
suggested_hardware: cpu-basic
pinned: false
license: mit
---

# Multilingual ABSA

Real-time aspect-based sentiment analysis for English, Hindi, Hinglish product reviews.

🔗 **[Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/Aryanmdev/multilingual-absa)**
📦 [GitHub repo](https://github.com/Aryanmishra-dev/Multilingual-Absa)

## Run Locally

```bash
git clone https://github.com/Aryanmishra-dev/Multilingual-Absa
cd Multilingual-Absa
pip install -r requirements.txt
python app.py
```

Open http://localhost:7860

## What it does

Extracts **aspects** (e.g. "battery", "camera") and their **sentiment** (positive/negative/neutral) from product reviews in 3 languages.

| Language | F1 | Latency p95 |
|----------|:--:|:-----------:|
| English  | 78.1% | 185 ms |
| Hindi    | 67.8% | 185 ms |

ONNX INT8 quantized → FP32 → rule-based fallback.

## Stack

- Gradio 4.44 (UI)
- ONNX Runtime (inference)
- XLM-RoBERTa (multilingual backbone)
- SQLite (prediction history)

## License

MIT