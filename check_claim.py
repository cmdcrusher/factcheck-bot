import time
from fact_checker import search_news_bilingual, predict_nli, classify_source, safe_translate
from collections import Counter

MAX_UNRANKED = 5

def check_claim(user_text, max_results=5):
    results = search_news_bilingual(user_text, max_results=max_results)
    hypothesis_en = safe_translate(user_text)

    independent_verdicts = []
    state_verdicts = []
    unranked_verdicts = []

    for r in results:
        source_type = classify_source(r['href'])

        if source_type == "unranked":
            if len(unranked_verdicts) >= MAX_UNRANKED:
                continue

        predict = predict_nli(premise=r['body'], hypothesis_en=hypothesis_en)
        entry = {
            'label': predict,
            'url': r['href'],
            'source_text': r['body'],
            'source_type': source_type
        }

        if source_type == "independent":
            independent_verdicts.append(entry)
        elif source_type == "state_affiliated":
            state_verdicts.append(entry)
        else:
            unranked_verdicts.append(entry)

        time.sleep(1.5)

    if independent_verdicts:
        labels_only = [v['label'] for v in independent_verdicts]
        final_verdict = Counter(labels_only).most_common(1)[0][0]
        return final_verdict, independent_verdicts + state_verdicts, "independent"

    if state_verdicts:
        labels_only = [v['label'] for v in state_verdicts]
        final_verdict = Counter(labels_only).most_common(1)[0][0]
        return final_verdict, state_verdicts, "state_affiliated_fallback"

    if unranked_verdicts:
        labels_only = [v['label'] for v in unranked_verdicts]
        final_verdict = Counter(labels_only).most_common(1)[0][0]
        return final_verdict, unranked_verdicts, "unranked_fallback"

    return "unknown", [], "none"
