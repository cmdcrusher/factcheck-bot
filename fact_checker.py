from deep_translator import GoogleTranslator
from ddgs import DDGS
import time
import os
import requests


API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
headers = {"Authorization": "Bearer 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"}


def safe_translate(text, retries=2):
    for attempt in range(retries):
        try:
            return GoogleTranslator(source='ru', target='en').translate(text)
        except Exception as e:
            print(f"Попытка {attempt + 1} не удалась: {e}")
            time.sleep(2 ** attempt)
    return text

def search_news(query, max_results=5):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    return results

def search_news_bilingual(query, max_results=5):
    query_en = safe_translate(query)

    results_ru = search_news(query, max_results=max_results)
    results_en = search_news(query_en, max_results=max_results)

    combined = results_ru + results_en

    return combined

def predict_nli(premise, hypothesis_en, high_threshold=0.9, low_threshold=0.6):
    premise_en = safe_translate(premise)

    payload = {
        "inputs": premise_en,
        "parameters": {
            "candidate_labels": [hypothesis_en],
            "hypothesis_template": "{}",
            "multi_label": True
        },
        "options": {"wait_for_model": True}
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    result = response.json()

    if isinstance(result, list) and len(result) > 0 and "score" in result[0]:
        entailment_score = result[0]["score"]
    elif isinstance(result, dict) and "scores" in result:
        entailment_score = result["scores"][0]
    else:
        print(f"Ошибка API: {result}")
        return "neutral"

    if entailment_score >= high_threshold:
        return "entailment"
    elif entailment_score >= low_threshold:
        return "leaning_entailment"
    elif entailment_score <= (1 - high_threshold):
        return "contradiction"
    elif entailment_score <= (1 - low_threshold):
        return "leaning_contradiction"
    else:
        return "neutral"

TRUSTED_DOMAINS = [
    "reuters.com", "apnews.com", "afp.com", "bbc.com", "bbc.co.uk",
    "theguardian.com", "forbes.com", "bloomberg.com", "nytimes.com",
    "washingtonpost.com", "wsj.com", "economist.com", "ft.com",
    "dw.com", "techcrunch.com", "theverge.com", "wired.com",
    "nature.com", "who.int", "kommersant.ru",
]

STATE_AFFILIATED_DOMAINS = [
    "ria.ru",
    "tass.ru",
    "sputniknews.com",
]

def classify_source(url):
    if any(domain in url for domain in TRUSTED_DOMAINS):
        return "independent"
    if any(domain in url for domain in STATE_AFFILIATED_DOMAINS):
        return "state_affiliated"
    return "unranked"

def format_response(verdict, sources, verdict_basis="independent"):
    verdict_dict = {
        "entailment": "✅ Утверждение подтверждается",
        "leaning_entailment": "🟢 Скорее подтверждается (не полная уверенность модели)",
        "contradiction": "❌ Утверждение опровергается",
        "leaning_contradiction": "🟠 Скорее опровергается (не полная уверенность модели)",
        "neutral": "⚠️ Не удалось точно определить",
        "unknown": "🤷 Источники не найдены"
    }

    if not sources:
        return "🤷 Не удалось найти источники для проверки этого утверждения."

    header = verdict_dict[verdict]

    if verdict_basis == "state_affiliated_fallback":
        header += "\n(ℹ️ источники из основного списка не найдены; вердикт основан на государственных информационных агентствах)"
    elif verdict_basis == "unranked_fallback":
        header += "\n(⚠️ надёжные и государственно-аффилированные источники не найдены; вердикт основан на источниках, не прошедших классификацию по редакционной принадлежности — рекомендуется дополнительная проверка)"

    sources_lines = []
    for i, source in enumerate(sources, start=1):
        if source.get('source_type') == "state_affiliated":
            marker = " [гос. СМИ]"
        elif source.get('source_type') == "unranked":
            marker = " [источник не классифицирован]"
        else:
            marker = ""
        line = f"{i}. {source['url']}{marker}"
        sources_lines.append(line)

    sources_text = "\n".join(sources_lines)
    final_text = f"{header}\n\n{sources[0]['source_text']}\n\nИсточники:\n{sources_text}"
    return final_text
