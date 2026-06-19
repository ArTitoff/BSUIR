import spacy
from spacy_glossbert import has_glossbert_wsd, get_synset_info

# Загружаем вашу текущую модель (можно md или lg, которые вы используете)
nlp = spacy.load("en_core_web_md")

# Добавляем компонент WSD в конец пайплайна
nlp.add_pipe("glossbert_wsd", last=True, config={
    "pos_filter": ["NOUN", "VERB", "ADJ"],  # обрабатываем только эти части речи
    "model_name": "kanishka/GlossBERT"      # предобученная модель[citation:3]
})

text = " The river bank was covered with grass."
doc = nlp(text)

# Вся старая функциональность остается!
for token in doc:
    print(f"{token.text}: лемма={token.lemma_}, POS={token.pos_}, DEP={token.dep_}")

# Дополнительно получаем семантический анализ (WSD)
if has_glossbert_wsd(doc):
    for token in doc:
        synset = token._.glossbert_synset
        if synset:
            print(f"\nСлово: {token.text}")
            print(f"Контекст: ...{doc.text[max(0, token.idx-30):min(len(doc.text), token.idx+len(token.text)+30)]}...")
            print(f"Смысл: {synset.definition()}")
            print(f"Синсет ID: {synset.name()}")