import psycopg2
from psycopg2.extras import DictCursor
from contextlib import contextmanager

class CorpusDatabase:
    
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None
    
    def connect(self):
        if not self.conn or self.conn.closed:
            self.conn = psycopg2.connect(**self.db_config, cursor_factory=DictCursor)
        return self.conn
    
    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()
    
    @contextmanager
    def cursor(self):
        """Контекстный менеджер для курсора (автоматически закрывает)"""
        conn = self.connect()
        cur = conn.cursor()
        try:
            yield cur
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
    
    # ----- ДОКУМЕНТЫ -----
    
    def add_document(self, filename, title=None, author=None, year=None, 
                     genre=None, subject_area=None):
        """
        Добавить документ в корпус.
        Возвращает ID документа.
        """
        with self.cursor() as cur:
            cur.execute("""
                INSERT INTO documents (filename, title, author, year, genre, subject_area)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (filename) DO UPDATE SET
                    title = EXCLUDED.title,
                    author = EXCLUDED.author,
                    year = EXCLUDED.year,
                    genre = EXCLUDED.genre,
                    subject_area = EXCLUDED.subject_area
                RETURNING id
            """, (filename, title, author, year, genre, subject_area))
            result = cur.fetchone()
            return result[0] if result else None
    

    def get_document_by_id(self, doc_id):
        """Получить информацию о документе по ID"""
        with self.cursor() as cur:
            cur.execute("""
                SELECT id, filename, title, author, year, genre, subject_area
                FROM documents WHERE id = %s
            """, (doc_id,))
            return cur.fetchone()
    

    def get_all_documents(self):
        """Список всех документов"""
        with self.cursor() as cur:
            cur.execute("""
                SELECT id, filename, title, author, year, genre, subject_area
                FROM documents ORDER BY filename
            """)
            return cur.fetchall()
    

    def delete_document(self, doc_id):
        """Удалить документ и все связанные данные"""
        with self.cursor() as cur:
            cur.execute("DELETE FROM documents WHERE id = %s", (doc_id,))
            return cur.rowcount > 0
    
    # ----- ПРЕДЛОЖЕНИЯ -----
    
    def add_sentence(self, doc_id, sentence_text):
        """
        Добавить предложение.
        Возвращает ID предложения.
        """
        with self.cursor() as cur:
            cur.execute("""
                INSERT INTO sentences (doc_id, sentence_text)
                VALUES (%s, %s) RETURNING id
            """, (doc_id, sentence_text))
            return cur.fetchone()[0]
    

    def get_sentences_by_doc(self, doc_id):
        """Все предложения документа"""
        with self.cursor() as cur:
            cur.execute("""
                SELECT id, sentence_text FROM sentences
                WHERE doc_id = %s ORDER BY id
            """, (doc_id,))
            return cur.fetchall()
    
    # ----- ТОКЕНЫ (СЛОВА) -----
    
    def add_token(self, sentence_id, token_data):
        with self.cursor() as cur:
            cur.execute("""
                INSERT INTO tokens 
                (sentence_id, token_text, lemma, pos_code, pos_ru, dep_code, member)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                sentence_id,
                token_data['token_text'],
                token_data['lemma'],
                token_data['pos_code'],
                token_data['pos_ru'],
                token_data['dep_code'],
                token_data['member']
            ))
    


    def add_tokens(self, sentence_id, tokens_list):
        """
        Добавить слова и их связи
        tokens_list - список токенов с полями position и head_position
        """
        with self.cursor() as cur:
            # Сначала вставляем все токены
            position_to_id = {}
            
            for token in tokens_list:
                cur.execute("""
                    INSERT INTO tokens 
                    (sentence_id, token_text, lemma, pos_code, pos_ru, dep_code, member)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    sentence_id,
                    token['token_text'],
                    token['lemma'],
                    token['pos_code'],
                    token['pos_ru'],
                    token['dep_code'],
                    token['member']
                ))
                token_id = cur.fetchone()[0]
                position_to_id[token['position']] = token_id
            
            # Теперь обновляем head_id для каждого токена
            for token in tokens_list:
                token_id = position_to_id[token['position']]
                head_position = token['head_position']
                
                if head_position != token['position']:  # не корень
                    head_id = position_to_id[head_position]
                    cur.execute("""
                        UPDATE tokens SET head_id = %s WHERE id = %s
                    """, (head_id, token_id))
                # корень оставляем head_id = NULL

                if token.get('word_sense'):  # .get() вместо прямого доступа
                    cur.execute("""
                        UPDATE tokens SET meaning = %s WHERE id = %s
                    """, (token['word_sense'], token_id))



    # ----- ПОИСК И ФИЛЬТРАЦИЯ (через VIEW concordance) -----
    
    def search_by_lemma(self, lemma, exact=True):
        """
        Поиск по лемме
        """
        with self.cursor() as cur:
            cur.execute("""
                SELECT 
                    token_id, token_text, lemma, pos_ru, member,
                    sentence_text, filename, title, author, year, genre
                FROM concordance
                WHERE lemma = %s
            """, (lemma.lower(),))
            return cur.fetchall()
    

    def filter_by_pos(self, pos_ru):
        """Фильтр по части речи"""
        with self.cursor() as cur:
            cur.execute("""
                SELECT 
                    token_id, token_text, lemma, pos_ru, member,
                    sentence_text, filename, title, author, year, genre
                FROM concordance
                WHERE pos_ru = %s
            """, (pos_ru,))
            return cur.fetchall()
    

    def filter_by_member(self, member):
        """Фильтр по члену предложения"""
        with self.cursor() as cur:
            cur.execute("""
                SELECT 
                    token_id, token_text, lemma, pos_ru, member,
                    sentence_text, filename, title, author, year, genre
                FROM concordance
                WHERE member = %s
            """, (member,))
            return cur.fetchall()
    

    def search_combined(self, lemma=None, pos=None, member=None):
        """Комбинированный поиск"""
        query = """
            SELECT 
                token_id, token_text, lemma, pos_ru, member,
                sentence_text, sentence_id, filename, title, author, year, genre
            FROM concordance
            WHERE 1=1
        """
        params = []
        
        if lemma:
            query += " AND lemma = %s"
            params.append(lemma.lower())
        if pos:
            query += " AND pos_ru = %s"
            params.append(pos)
        if member:
            query += " AND member = %s"
            params.append(member)
        
        with self.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()
    

    def update_token(self, token_id, **kwargs):
        """
        Обновить информацию о слове.
        kwargs могут содержать: token_text, lemma, pos_code, pos_ru, dep_code, member, head_id, meaning
        """
        if not kwargs:
            return False
        
        set_parts = []
        values = []
        for key, value in kwargs.items():
            if key in ['token_text', 'lemma', 'pos_code', 'pos_ru', 'dep_code', 'member', 'head_id', 'meaning']:
                set_parts.append(f"{key} = %s")
                values.append(value)
        
        if not set_parts:
            return False
        
        values.append(token_id)
        query = f"UPDATE tokens SET {', '.join(set_parts)} WHERE id = %s RETURNING id"
        
        with self.cursor() as cur:
            cur.execute(query, values)
            return cur.fetchone() is not None


    def delete_token(self, token_id):
        """Удалить слово"""
        with self.cursor() as cur:
            cur.execute("DELETE FROM tokens WHERE id = %s RETURNING id", (token_id,))
            return cur.fetchone() is not None

        
    def get_word_statistic(self, lemma):
        """Сколько раз слово встретилось в корпусе"""
        with self.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM tokens WHERE lemma = %s", (lemma.lower(),))
            result = cur.fetchone()
            return result[0]
        

    def get_sentence_tree(self, sentence_id):
        """Возвращает дерево предложения в формате для displaCy"""
        query = """
        SELECT 
            t.id,
            t.token_text,
            t.pos_ru,
            t.lemma,
            t.member,
            t.dep_code,
            t.head_id
        FROM tokens t
        WHERE t.sentence_id = %s
        ORDER BY t.id
        """
        
        with self.cursor() as cur:
            cur.execute(query, (sentence_id,))
            tokens = cur.fetchall()
            
            if not tokens:
                return None
            
            # Преобразуем DictRow в обычные dict для удобства
            tokens_list = []
            for token in tokens:
                tokens_list.append({
                    'id': token['id'],
                    'token_text': token['token_text'],
                    'pos_ru': token['pos_ru'],
                    'lemma': token['lemma'],
                    'member': token['member'],
                    'dep_code': token['dep_code'],
                    'head_id': token['head_id']
                })
            
            # Формат для displaCy
            words = []
            arcs = []
            
            # Слова
            for token in tokens_list:
                words.append({
                    'text': token['token_text'],
                    'tag': token['pos_ru'],
                    'data': [
                        ['id', token['id']],
                        ['lemma', token['lemma']],
                        ['member', token['member']]
                    ]
                })
            
            # Связи
            for idx, token in enumerate(tokens_list):
                if token['head_id'] and token['dep_code']:
                    # Ищем индекс родителя
                    parent_idx = next(
                        (i for i, t in enumerate(tokens_list) if t['id'] == token['head_id']),
                        None
                    )
                    if parent_idx is not None:
                        arcs.append({
                            'start': parent_idx,
                            'end': idx,
                            'label': token['dep_code']
                        })
            
            result = {'words': words, 'arcs': arcs}
            print("Данные для дерева:", result)  # Для отладки
            return result