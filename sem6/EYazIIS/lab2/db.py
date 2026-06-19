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
        Добавить несколько слов за один раз
        """
        with self.cursor() as cur:
            args_str = ','.join(
                cur.mogrify(
                    "(%s, %s, %s, %s, %s, %s, %s)", 
                    (sentence_id, 
                     t['token_text'], t['lemma'], t['pos_code'], 
                     t['pos_ru'], t['dep_code'], t['member'])
                ).decode('utf-8')
                for t in tokens_list
            )
            cur.execute("""
                INSERT INTO tokens 
                (sentence_id, token_text, lemma, pos_code, pos_ru, dep_code, member)
                VALUES """ + args_str
            )
    
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
                sentence_text, filename, title, author, year, genre
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
        kwargs могут содержать: token_text, lemma, pos_code, pos_ru, dep_code, member
        """
        if not kwargs:
            return False
        
        set_parts = []
        values = []
        for key, value in kwargs.items():
            if key in ['token_text', 'lemma', 'pos_code', 'pos_ru', 'dep_code', 'member']:
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