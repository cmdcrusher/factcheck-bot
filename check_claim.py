from fact_checker import predict_nli, is_trusted_source, search_news_bilingual, format_response
from collections import Counter

def check_claim(user_text, max_results=5):
    results = search_news_bilingual(user_text, max_results=max_results)

    verdicts = []

    for r in results:
        if not is_trusted_source(r['href']):
            continue  # пропускаем этот результат, идём к следующему

        predict = predict_nli(premise=r['body'], hypothesis=user_text)

        verdicts.append({
            'label': predict,
            'url': r['href'],
            'source_text': r['body']
        })

    if not verdicts:
        return "unknown", []  # если после фильтрации не осталось источников

    labels_only = [v['label'] for v in verdicts]
    final_verdict = Counter(labels_only).most_common(1)[0][0]

    return final_verdict, verdicts