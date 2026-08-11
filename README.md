[🇷🇺 Русская версия](README.ru.md)
# 🔍 FactCheck Bot — A Telegram Bot for News Verification

A Telegram bot that checks the credibility of news and claims using web search combined with a Natural Language Inference (NLI) model. The user sends a claim — the bot searches for sources, compares them against the claim, and returns a verdict with supporting links.

## 📌 Demo

> User: *"Elon Musk bought Twitter"*
> Bot: ✅ Claim is supported
> Sources: BBC News, The Washington Post

## 🎯 Motivation

Misinformation is one of the central challenges of the digital information environment. This project explores whether basic fact-checking can be automated using open-source NLP models, without relying on expensive proprietary solutions — and, more specifically, whether such models can be made to work reliably on non-English text.

## 🏗️ Architecture

```
User → Telegram bot
           ↓
    Source search (DuckDuckGo, bilingual RU + EN queries)
           ↓
    Filtering by a whitelist of trusted domains
           ↓
    Translation (RU → EN) + NLI analysis (facebook/bart-large-mnli)
           ↓
    Confidence threshold + majority voting across sources
           ↓
    Final verdict + source links → user
```

## 🧠 The ML Problem: What Was Investigated

A core challenge of this project was making an NLI model — originally trained on English-language data — perform reliably on Russian-language news claims. Two approaches were implemented and benchmarked:

| Approach | Accuracy (34-example test set) |
|---|---|
| Multilingual model used directly (`mDeBERTa-v3-base-mnli-xnli`) | 76.5% |
| Translation (RU→EN) + specialized English model (`bart-large-mnli`) | **85.3%** |

**Key finding**: both models showed a systematic weakness on the `neutral` class (unrelated claims) — they tended to misclassify "different facts on the same topic" as a logical contradiction. The initial hypothesis was that this was a language-related issue; this was tested and **disproved** — translating the text to English did not fix the neutral-class errors, indicating the problem is an inherent limitation of NLI model architecture/training rather than a language barrier.

**Solution**: a confidence threshold was introduced — if the model's confidence in its top prediction falls below 0.9, the result defaults to `neutral`. This raised accuracy from 60% to 85.3% on the test set.

## 🛠️ Tech Stack

- **Python 3.12+**
- `python-telegram-bot` — bot interface
- `duckduckgo-search` — source retrieval (bilingual RU + EN queries)
- `transformers` (Hugging Face) — NLI model
- `torch` (PyTorch) — model inference
- `deep-translator` — RU → EN translation
- `python-dotenv` — secure token storage

## 📂 Project Structure

```
├── bot.py                 # entry point, Telegram handlers
├── check_claim.py         # claim-checking logic (search + analysis + voting)
├── fact_checker.py        # low-level functions: model, translation, search, whitelist
├── test_data.py           # labeled test dataset (34 examples)
├── .env                   # tokens (not published, see .gitignore)
├── .gitignore
└── requirements.txt
```

## 🚀 Setup and Usage

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/factcheck-bot.git
cd factcheck-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```
TELEGRAM_BOT_TOKEN=your_botfather_token
```

4. Run the bot:
```bash
python bot.py
```

## 📊 Limitations and Future Work

- The source whitelist is manually curated; a trust-scoring system could be a more scalable alternative
- The test dataset currently contains 34 examples; expanding to 100+ would yield more statistically reliable metrics
- A promising direction is fine-tuning the NLI model on a custom dataset to specifically address the `neutral`-class weakness
- The bot currently runs locally; cloud deployment is planned for continuous availability

---
*Created by Alim*