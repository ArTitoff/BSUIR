# rag_search.py
from text_processor import TextProcessor
from db import CorpusDatabase

class CorpusSearcher:
    """
    Ищет в корпусе предложения, похожие на вопрос пользователя
    """
    
    def __init__(self, db: CorpusDatabase):
        self.db = db
        self.processor = TextProcessor()
    
    def extract_keywords(self, question: str) -> list:
        """
        Извлекает ключевые слова из вопроса
        Пример: "Сколько стоит уборка квартиры?" -> ['стоить', 'уборка', 'квартира']
        """
        # Анализируем через spaCy
        doc = self.processor.nlp(question.lower())
        
        keywords = []
        for token in doc:
            # Берём только значимые части речи
            if token.pos_ in ['NOUN', 'VERB', 'ADJ', 'PROPN']:
                # Исключаем короткие и служебные слова
                if len(token.lemma_) > 2:
                    keywords.append(token.lemma_)
        
        # Убираем дубликаты
        return list(set(keywords))
    
    def search(self, question: str, top_k: int = 3) -> dict:
        """
        Главный метод поиска
        
        Returns:
            {
                'keywords': ['стоить', 'уборка'],
                'found_sentences': [{'sentence_text': '...', 'filename': '...'}, ...]
            }
        """
        # 1. Извлекаем ключевые слова
        keywords = self.extract_keywords(question)
        
        if not keywords:
            return {
                'keywords': [],
                'found_sentences': []
            }
        
        # 2. Ищем в БД
        found = self.db.find_sentences_by_keywords(keywords, limit=top_k)
        
        return {
            'keywords': keywords,
            'found_sentences': found
        }
    

    def format_context(self, search_result: dict) -> str:
        """English-only context"""
        sentences = search_result['found_sentences']
        
        if not sentences:
            return "No relevant information found."
        
        context_parts = []
        for i, s in enumerate(sentences, 1):
            context_parts.append(f"[Document {i}] {s['sentence_text']}")
        
        context = "\n".join(context_parts)
        return f"""
    {context}

    Based on THESE documents, answer the user's question.
    If the documents don't provide a precise answer, say so.
    Don't invent information that isn't in the documents.
    """