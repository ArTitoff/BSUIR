# rag_system.py
from rag_search import CorpusSearcher
from llm_client import LocalLLM
from db import CorpusDatabase

class RAGSystem:
    """
    RAG система: поиск по корпусу + генерация ответа через LLM
    """
    
    def __init__(self, db: CorpusDatabase):
        self.searcher = CorpusSearcher(db)
        self.llm = None  # Пока не загружаем, загрузим при первом вопросе
        
    def ask(self, question: str) -> dict:
        """
        Задать вопрос системе
        
        Returns:
            {
                'question': вопрос пользователя,
                'answer': ответ системы,
                'keywords': какие слова нашли,
                'sources': откуда взяли информацию,
                'context': какой контекст отправили в LLM
            }
        """
        
        print(f"\n{'='*50}")
        print(f" Вопрос пользователя: {question}")
        
        # ШАГ 1: Ищем в корпусе
        print(" Ищу в корпусе...")
        search_result = self.searcher.search(question, top_k=3)
        
        print(f" Найдено предложений: {len(search_result['keywords'])}")
        print(f" Ключевые слова: {search_result['keywords']}")
        
        
        # ШАГ 2: Форматируем контекст
        context = self.searcher.format_context(search_result)
        
        # ШАГ 3: Загружаем LLM (при первом вопросе)
        if self.llm is None:
            print("Загружаю LLM (первый раз может быть долго)...")
            self.llm = LocalLLM()
        
        # ШАГ 4: Генерируем ответ
        print(" Генерирую ответ...")
        answer = self.llm.generate_answer(question, context)
        
        # ШАГ 5: Собираем источники
        sources = list(set([s['filename'] for s in search_result['found_sentences']]))
        
        print(f" Ответ сгенерирован")
        print(f" Источники: {sources}")
        
        return {
            'question': question,
            'answer': answer,
            'keywords': search_result['keywords'],
            'sources': sources,
            'context': context,
            'success': True
        }