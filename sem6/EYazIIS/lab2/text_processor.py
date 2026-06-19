"""
Модуль для обработки текстовых файлов и лингвистического анализа.
Извлекает текст, разбивает на предложения, анализирует через spaCy.
"""
import PyPDF2
import spacy
import re
from typing import List, Dict, Any


try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    # Если модель не установлена
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_md"])
    nlp = spacy.load("en_core_web_md")


POS_RU = {
    'NOUN': 'существительное',
    'PROPN': 'имя собственное', 
    'VERB': 'глагол',
    'AUX': 'вспомогательный глагол',
    'ADJ': 'прилагательное',
    'ADV': 'наречие',
    'ADP': 'предлог',
    'DET': 'артикль',
    'CCONJ': 'сочинительный союз',
    'SCONJ': 'подчинительный союз',
    'PART': 'частица',
    'PRON': 'местоимение',
    'INTJ': 'междометие',
    'NUM': 'числительное',
    'SYM': 'символ',
    'PUNCT': 'знак пунктуации',
    'SPACE': 'пробел',
    'X': 'другое'
}

def get_sentence_member(dep: str, pos: str) -> str: # Определяет член предложения по зависимости и части речи
    # Главные члены предложения
    if dep in ['nsubj', 'nsubjpass']:
        return 'подлежащее'
    
    if (dep == 'ROOT' and (pos == 'VERB' or pos == 'AUX')) or dep == 'xcomp' or dep == 'cop':
        return 'сказуемое'
    
    # Второстепенные члены
    if dep in ['dobj', 'iobj', 'obj', 'attr']:
        return 'дополнение'
    
    if dep in ['amod', 'nummod', 'det', 'poss', 'acomp']:
        return 'определение'
    
    if dep in ['advmod', 'advcl', 'npadvmod', 'pobj']:
        return 'обстоятельство'
    
    return '-'


def split_sentences(text: str) -> List[str]:
    """
    Разбивает текст на предложения.
    Учитывает . ! ? и переносы строк.
    """
    # Заменяем переносы строк на пробелы
    text = text.replace('\n', ' ').replace('\r', ' ')
    
    # Разбиваем по .!? с сохранением разделителей
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Очищаем и фильтруем пустые
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 3]
    
    return sentences


import os
import PyPDF2
from docx import Document  
import subprocess

def extract_text_from_file(filepath: str) -> str:
    """Универсальное извлечение текста из файла"""
    ext = os.path.splitext(filepath)[1].lower()
    
    # TXT
    if ext == '.txt':
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    # PDF
    elif ext == '.pdf':
        text = ""
        with open(filepath, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            for page in pdf.pages:
                if page_text := page.extract_text():
                    text += page_text + " "
        return text.strip()
    
    # DOCX
    elif ext == '.docx':
        doc = Document(filepath)
        return ' '.join([p.text for p in doc.paragraphs])
    
    # DOC (старый)
    elif ext == '.doc':
        try:
            result = subprocess.run(['antiword', filepath], 
                                  capture_output=True, text=True)
            return result.stdout
        except:
            return "[ОШИБКА: не удалось прочитать .doc файл]"
    
    # RTF
    elif ext == '.rtf':
        # Пробуем прочитать как текст
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    else:
        return f"[Неподдерживаемый формат: {ext}]"


class TextProcessor:
    """Класс для обработки текстов"""
    
    def __init__(self):
        self.nlp = nlp
        self.pos_dict = POS_RU
    
    def process_file(self, filepath: str) -> Dict[str, Any]:
        # Извлекаем текст
        raw_text = extract_text_from_file(filepath)
        if not raw_text:
            raise ValueError("Файл не содержит текста или текст не извлекается")
        
        # Разбиваем на предложения
        sentences = split_sentences(raw_text)
        
        result = {
            'raw_text': raw_text,
            'sentences': []
        }
        
        for sent_text in sentences:
            # Анализ через spaCy
            doc = self.nlp(sent_text)
            
            tokens = []
            for token in doc:
                if token.is_punct or token.is_space:
                    continue
                
                tokens.append({
                    'token_text': token.text,
                    'lemma': token.lemma_.lower(),
                    'pos_code': token.pos_,
                    'pos_ru': self.pos_dict.get(token.pos_, token.pos_),
                    'dep_code': token.dep_,
                    'member': get_sentence_member(token.dep_, token.pos_)
                })
            
            result['sentences'].append({
                'text': sent_text,
                'tokens': tokens
            })
        
        return result
    