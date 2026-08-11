from transformers import AutoTokenizer, AutoModelForSequenceClassification
from deep_translator import GoogleTranslator
from ddgs import DDGS
import torch
import time

model_name = 'facebook/bart-large-mnli'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def safe_translate(text, retries=3):
    for attempt in range(retries):
        try:
            return GoogleTranslator(source='ru', target='en').translate(text)
        except Exception as e:
            print(f"Попытка {attempt + 1} не удалась: {e}")
            time.sleep(1)
    return None

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

def predict_nli(premise, hypothesis, threshold=0.9):
    premise_en = safe_translate(premise)
    hypothesis_en = safe_translate(hypothesis)

    inputs = tokenizer(premise_en, hypothesis_en, return_tensors='pt', truncation=True)
    outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=1)[0]

    probs_dict = {}
    for i, p in enumerate(probs):
        label = model.config.id2label[i]
        probs_dict[label] = p.item()

    best_label = max(probs_dict, key=probs_dict.get)
    best_score = probs_dict[best_label]

    if best_score < threshold:
        return "neutral"
    return best_label


TRUSTED_DOMAINS = [
    # Международные информагентства
    "reuters.com",
    "apnews.com",
    "afp.com",
    "bbc.com",
    "bbc.co.uk",

    # Крупные международные издания
    "theguardian.com",
    "forbes.com",
    "bloomberg.com",
    "nytimes.com",
    "washingtonpost.com",
    "wsj.com",
    "economist.com",
    "ft.com",  # Financial Times

    # Немецкие/европейские с международной репутацией
    "dw.com",  # Deutsche Welle, есть русская редакция

    # Технологические издания
    "techcrunch.com",
    "theverge.com",
    "wired.com",

    # Научные/официальные источники
    "nature.com",
    "who.int",
]

def is_trusted_source(url):
    return any(domain in url for domain in TRUSTED_DOMAINS)

def format_response(verdict, sources):
    if not sources:
        return "🤷 Не удалось найти источники для проверки этого утверждения."

    verdict_dict = {
        "entailment": "✅ Утверждение подтверждается",
        "contradiction": "❌ Утверждение опровергается",
        "neutral": "⚠️ Не удалось точно определить",
        "unknown": "🤷 Источники не найдены"
    }

    header = verdict_dict[verdict]

    sources_lines = []
    for i, source in enumerate(sources, start=1):
        line = f"{i}. {source['url']}"
        sources_lines.append(line)

    sources_text = "\n".join(sources_lines)

    final_text = f"{header}\n\n{sources[0]['source_text']}\n\nИсточники:\n{sources_text}"

    return final_text

