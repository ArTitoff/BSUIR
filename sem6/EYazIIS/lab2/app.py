from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import tempfile
from werkzeug.utils import secure_filename
from db import CorpusDatabase
from text_processor import TextProcessor
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'


app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc', 'rtf'}


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


DB_CONFIG = {
            'dbname': 'yazis_2',
            'user': 'postgres',
            'password': 'asd123',
            'host': '127.0.0.1',
            'port': '5432'
}

db = CorpusDatabase(DB_CONFIG)
processor = TextProcessor()


POS_OPTIONS = [
    'существительное',
    'глагол',
    'прилагательное',
    'наречие',
    'местоимение',
    'предлог',
    'союз',
    'междометие',
    'артикль',
    'числительное',
    'имя собственное',
    'вспомогательный глагол'
]


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html', pos_options=POS_OPTIONS)


@app.route('/api/search', methods=['POST'])
def search():
    """Поиск слов с комбинацией фильтров"""
    data = request.json
    lemma = data.get('lemma', '').strip()
    pos = data.get('pos')
    member = data.get('member')
    
    # Используем комбинированный поиск
    # Если лемма пустая, ищем только по фильтрам
    results = db.search_combined(
        lemma=lemma if lemma else None,
        pos=pos if pos else None,
        member=member if member else None
    )
    
    # Если есть лемма, получаем статистику
    count = db.get_word_statistic(lemma) if lemma else 0
    
    return jsonify({
        'results': [dict(r) for r in results],
        'count': count,
        'lemma': lemma
    })


@app.route('/api/update_token', methods=['POST'])
def update_token():
    """Обновление данных слова"""
    data = request.json
    token_id = data.get('token_id')
    updates = data.get('updates', {})
    
    if not token_id:
        return jsonify({'error': 'Нет ID токена'}), 400
    
    success = db.update_token(token_id, **updates)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Не удалось обновить'}), 500


@app.route('/api/delete_token', methods=['POST'])
def delete_token():
    """Удаление слова"""
    data = request.json
    token_id = data.get('token_id')
    
    if not token_id:
        return jsonify({'error': 'Нет ID токена'}), 400
    
    success = db.delete_token(token_id)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Не удалось удалить'}), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Загрузка и анализ файла"""
    if 'file' not in request.files:
        return jsonify({'error': 'Нет файла'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Нет выбранного файла'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Неподдерживаемый формат файла'}), 400
    
    # Получаем метаданные из формы
    title = request.form.get('title', '')
    author = request.form.get('author', '')
    year = request.form.get('year')
    genre = request.form.get('genre', '')
    subject_area = request.form.get('subject_area', 'Услуги')
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        analysis = processor.process_file(filepath)
        
        doc_id = db.add_document(
            filename=filename,
            title=title if title else None,
            author=author if author else None,
            year=int(year) if year else None,
            genre=genre if genre else None,
            subject_area=subject_area
        )
        
        # Сохраняем предложения и слова
        for sent_data in analysis['sentences']:
            sent_id = db.add_sentence(doc_id, sent_data['text'])
            db.add_tokens(sent_id, sent_data['tokens'])
        
        stats = {
            'sentences': len(analysis['sentences']),
            'tokens': sum(len(s['tokens']) for s in analysis['sentences'])
        }
        
        # Удаляем временный файл
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'doc_id': doc_id,
            'stats': stats,
            'message': f'Файл успешно загружен. Добавлено {stats["sentences"]} предложений, {stats["tokens"]} слов.'
        })
        
    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': str(e)}), 500


@app.route('/api/documents', methods=['GET'])
def get_documents():
    """Список всех документов"""
    docs = db.get_all_documents()
    return jsonify({'documents': [dict(d) for d in docs]})


@app.route('/api/update_document', methods=['POST'])
def update_document():
    """Обновление информации о документе"""
    data = request.json
    doc_id = data.get('doc_id')
    
    if not doc_id:
        return jsonify({'error': 'Нет ID документа'}), 400
    
    updates = {}
    if 'title' in data:
        updates['title'] = data['title']
    if 'author' in data:
        updates['author'] = data['author']
    if 'year' in data:
        updates['year'] = int(data['year']) if data['year'] else None
    if 'genre' in data:
        updates['genre'] = data['genre']
    if 'subject_area' in data:
        updates['subject_area'] = data['subject_area']
    
    if not updates:
        return jsonify({'error': 'Нет данных для обновления'}), 400
    
    # Обновляем документ
    with db.cursor() as cur:
        set_clause = ', '.join([f"{k} = %s" for k in updates.keys()])
        values = list(updates.values()) + [doc_id]
        cur.execute(f"""
            UPDATE documents 
            SET {set_clause}
            WHERE id = %s
            RETURNING id
        """, values)
        success = cur.fetchone() is not None
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Не удалось обновить'}), 500


@app.route('/api/delete_document', methods=['POST'])
def delete_document():
    """Удаление документа"""
    data = request.json
    doc_id = data.get('doc_id')
    
    if not doc_id:
        return jsonify({'error': 'Нет ID документа'}), 400
    
    success = db.delete_document(doc_id)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Не удалось удалить'}), 500


@app.route('/api/export_json', methods=['POST'])
def export_json():
    """Экспорт результатов в JSON с выбором места сохранения"""
    data = request.json
    results = data.get('results', [])
    filename = data.get('filename', '').strip()
    
    if not results:
        return jsonify({'error': 'Нет данных для экспорта'}), 400
    
    # Если имя файла не указано, генерируем автоматически
    if not filename:
        filename = f'corpus_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    # Добавляем расширение .json, если его нет
    if not filename.endswith('.json'):
        filename += '.json'
    
    # Создаем временный файл
    fd, temp_path = tempfile.mkstemp(suffix='.json')
    
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump({
                'export_date': datetime.now().isoformat(),
                'total_results': len(results),
                'data': results
            }, f, ensure_ascii=False, indent=2)
        
        # Отправляем файл с указанным именем
        return send_file(
            temp_path,
            as_attachment=True,           # ← заставляет браузер скачивать
            download_name=filename,        # ← имя файла для сохранения
            mimetype='application/json'
        )
    finally:
        # Удаляем временный файл после отправки
        try:
            os.unlink(temp_path)
        except:
            pass


@app.route('/help')
def help_page():
    """Страница помощи"""
    help_text = """
    <h2>Корпусный менеджер - помощь</h2>
    
    <h3>📁 Загрузка файлов</h3>
    <p>Поддерживаемые форматы: TXT, PDF, DOCX, DOC, RTF</p>
    <p>При загрузке можно указать метаданные (название, автор, год, жанр) - все поля необязательные</p>
    
    <h3>🔍 Поиск и фильтрация</h3>
    <p><strong>Поиск по слову</strong> - точное совпадение леммы (найдет все формы слова)</p>
    <p><strong>Фильтр по части речи</strong> - можно выбрать из списка</p>
    <p><strong>Фильтр по члену предложения</strong> - подлежащее, сказуемое и т.д.</p>
    <p><em>Все фильтры работают независимо. Можно искать без слова - только по фильтрам.</em></p>
    
    <h3>📊 Результаты</h3>
    <p>Для каждого слова показывается:</p>
    <ul>
        <li>Слово (исходная форма)</li>
        <li>Лемма</li>
        <li>Часть речи</li>
        <li>Член предложения</li>
        <li>Контекст (предложение)</li>
        <li>Информация об источнике</li>
    </ul>
    <p>Внизу отображается общее количество найденных вхождений</p>
    
    <h3>✏️ Редактирование</h3>
    <p><strong>Двойной клик по ячейке</strong> позволяет редактировать:</p>
    <ul>
        <li>Слово</li>
        <li>Лемму</li>
        <li>Часть речи</li>
        <li>Член предложения</li>
    </ul>
    <p>Размер ячеек фиксирован, редактирование не ломает таблицу</p>
    
    <h3>📋 Документы</h3>
    <p>В списке документов можно:</p>
    <ul>
        <li>Просматривать загруженные документы</li>
        <li><strong>Редактировать метаданные</strong> (название, автор, год, жанр)</li>
        <li>Удалять документы</li>
    </ul>
    
    <h3>💾 Экспорт</h3>
    <p>Кнопка "Экспорт JSON" сохраняет текущие результаты поиска в JSON файл</p>
    """
    return help_text

if __name__ == '__main__':
    app.run(debug=True)