test_data = [
    {"premise": "Компания SpaceX успешно запустила ракету Falcon 9 в марте 2024 года.",
     "hypothesis": "SpaceX запустила ракету",
     "correct_label": "entailment"},

    {"premise": "Президент Франции Эммануэль Макрон посетил Украину с официальным визитом.",
     "hypothesis": "Макрон побывал в Украине",
     "correct_label": "entailment"},

    {"premise": "Центральный банк снизил ключевую ставку до 12%.",
     "hypothesis": "Центральный банк повысил ставку",
     "correct_label": "contradiction"},

    {"premise": "Компания Tesla отменила выпуск новой модели электромобиля.",
     "hypothesis": "Tesla выпустила новую модель",
     "correct_label": "contradiction"},

    {"premise": "В Токио прошёл международный кинофестиваль.",
     "hypothesis": "Курс доллара вырос на 3%",
     "correct_label": "neutral"},

    {"premise": "Учёные обнаружили новый вид бабочек в Амазонии.",
     "hypothesis": "Илон Маск объявил о новом проекте Neuralink",
     "correct_label": "neutral"},

    {"premise": "Илон Маск купил компанию Tesla в 2004 году.",
     "hypothesis": "Илон Маск купил Twitter",
     "correct_label": "neutral"},

    {"premise": "Google инвестировала 2 миллиарда долларов в стартап по ИИ.",
     "hypothesis": "Google купила стартап по ИИ",
     "correct_label": "neutral"},

    {"premise": "Правительство рассматривает законопроект о повышении налогов.",
     "hypothesis": "Правительство повысило налоги",
     "correct_label": "neutral"},

    {"premise": "Amazon уволила 10,000 сотрудников в 2023 году.",
     "hypothesis": "Amazon сократила штат",
     "correct_label": "entailment"},
]

new_test_data = [
    {"premise": "Apple представила новый iPhone 17 на презентации в сентябре 2026 года.",
     "hypothesis": "Apple выпустила новый iPhone",
     "correct_label": "entailment"},

    {"premise": "Сборная Франции по футболу выиграла финал чемпионата Европы.",
     "hypothesis": "Франция стала чемпионом Европы по футболу",
     "correct_label": "entailment"},

    {"premise": "Курс евро поднялся до 105 рублей впервые за полгода.",
     "hypothesis": "Евро подорожал по отношению к рублю",
     "correct_label": "entailment"},

    {"premise": "Microsoft закрыла сделку по покупке студии-разработчика игр за 3 миллиарда долларов.",
     "hypothesis": "Microsoft приобрела игровую студию",
     "correct_label": "entailment"},

    {"premise": "В результате землетрясения магнитудой 6.2 пострадали более 200 зданий.",
     "hypothesis": "Землетрясение вызвало разрушения",
     "correct_label": "entailment"},

    {"premise": "ВОЗ официально объявила о завершении вспышки заболевания в регионе.",
     "hypothesis": "Вспышка заболевания закончилась",
     "correct_label": "entailment"},

    {"premise": "Компания Boeing получила разрешение регулятора на возобновление полётов модели 737 MAX.",
     "hypothesis": "Boeing 737 MAX снова может летать",
     "correct_label": "entailment"},

    {"premise": "Верховный суд отклонил апелляцию и оставил приговор в силе.",
     "hypothesis": "Верховный суд отменил приговор",
     "correct_label": "contradiction"},

    {"premise": "Число безработных в стране сократилось до рекордного минимума за 10 лет.",
     "hypothesis": "Безработица достигла рекордного максимума",
     "correct_label": "contradiction"},

    {"premise": "Netflix объявил об отмене продолжения популярного сериала после одного сезона.",
     "hypothesis": "Netflix продлил сериал на второй сезон",
     "correct_label": "contradiction"},

    {"premise": "Компания перенесла запуск продукта на неопределённый срок из-за технических проблем.",
     "hypothesis": "Продукт был успешно запущен по плану",
     "correct_label": "contradiction"},

    {"premise": "Городские власти отказались от строительства нового моста после протестов жителей.",
     "hypothesis": "Строительство моста началось согласно плану",
     "correct_label": "contradiction"},

    {"premise": "Инфляция замедлилась третий месяц подряд, согласно данным Центробанка.",
     "hypothesis": "Инфляция продолжает ускоряться",
     "correct_label": "contradiction"},

    {"premise": "Авиакомпания восстановила все отменённые ранее рейсы.",
     "hypothesis": "Рейсы авиакомпании остаются отменёнными",
     "correct_label": "contradiction"},

    {"premise": "В Париже открылась выставка импрессионистов в Лувре.",
     "hypothesis": "Цены на нефть выросли на 2%",
     "correct_label": "neutral"},

    {"premise": "Ученые NASA обнаружили новую экзопланету в созвездии Лиры.",
     "hypothesis": "Сборная Бразилии выиграла Кубок Америки",
     "correct_label": "neutral"},

    {"premise": "В Германии прошли выборы в местные органы власти.",
     "hypothesis": "Компания Samsung представила новый смартфон",
     "correct_label": "neutral"},

    {"premise": "Amazon объявила о повышении зарплат складским работникам на 10%.",
     "hypothesis": "Amazon сократила штат складских работников",
     "correct_label": "neutral"},

    {"premise": "Tesla открыла новый завод по производству батарей в Германии.",
     "hypothesis": "Tesla закрыла завод в Китае",
     "correct_label": "neutral"},

    {"premise": "OpenAI выпустила обновление своей модели для корпоративных клиентов.",
     "hypothesis": "OpenAI объявила об IPO компании",
     "correct_label": "neutral"},

    {"premise": "Илон Маск заявил о планах строительства завода на Марсе в далёком будущем.",
     "hypothesis": "Илон Маск запустил ракету на Марс",
     "correct_label": "neutral"},

    {"premise": "Google представила новый алгоритм поиска, снижающий число спама в результатах.",
     "hypothesis": "Google приобрела компанию по кибербезопасности",
     "correct_label": "neutral"},

    {"premise": "Правительство Великобритании увеличило расходы на здравоохранение на 5 миллиардов фунтов.",
     "hypothesis": "Правительство Великобритании снизило налоги для бизнеса",
     "correct_label": "neutral"},

    {"premise": "Meta уволила 5% сотрудников в рамках реструктуризации.",
     "hypothesis": "Meta объявила о рекордной квартальной прибыли",
     "correct_label": "neutral"},
]

full_data = test_data + new_test_data

problem_data = [
    {"premise": "Учёные обнаружили новый вид бабочек в Амазонии.",
     "hypothesis": "Илон Маск объявил о новом проекте Neuralink",
     "correct_label": "neutral"},

    {"premise": "Илон Маск купил компанию Tesla в 2004 году.",
     "hypothesis": "Илон Маск купил Twitter",
     "correct_label": "neutral"},

    {"premise": "Google инвестировала 2 миллиарда долларов в стартап по ИИ.",
     "hypothesis": "Google купила стартап по ИИ",
     "correct_label": "neutral"},

    {"premise": "Правительство рассматривает законопроект о повышении налогов.",
     "hypothesis": "Правительство повысило налоги",
     "correct_label": "neutral"}
]