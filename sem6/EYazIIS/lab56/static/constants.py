HELP_TEXT = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Помощь - Корпусный менеджер</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #f0f0f0;
                padding: 20px;
            }
            
            .container {
                max-width: 1600px;
                margin: 0 auto;
            }
            
            .header {
                background-color: #4a6fa5;
                color: white;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .header h1 {
                margin: 0;
                font-size: 24px;
            }
            
            .header a {
                color: white;
                text-decoration: none;
                background-color: #6c757d;
                padding: 10px 20px;
                border-radius: 4px;
                transition: background-color 0.2s;
            }
            
            .header a:hover {
                background-color: #5a6268;
            }
            
            .help-grid {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr 1fr;
                gap: 20px;
            }
            
            .help-column {
                background-color: white;
                padding: 25px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .help-column h2 {
                color: #4a6fa5;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #4a6fa5;
                font-size: 22px;
            }
            
            .help-column h2.semantic {
                border-bottom-color: #28a745;
                color: #28a745;
            }
            
            .help-column h2.chat {
                border-bottom-color: #4a6fa5;
                color: #4a6fa5;
            }
            
            .help-column h3 {
                color: #4a6fa5;
                margin: 20px 0 10px 0;
                font-size: 18px;
            }
            
            .help-column h3.semantic {
                color: #28a745;
            }
            
            .help-column h3.chat {
                color: #4a6fa5;
            }
            
            .help-column ul, .help-column ol {
                margin: 10px 0 20px 25px;
            }
            
            .help-column li {
                margin: 5px 0;
                line-height: 1.5;
            }
            
            .help-column p {
                margin: 10px 0;
                line-height: 1.6;
            }
            
            .help-column strong {
                color: #4a6fa5;
            }
            
            .help-column strong.semantic {
                color: #28a745;
            }
            
            .help-column em {
                color: #666;
                font-style: italic;
            }
            
            .help-column .note {
                background-color: #e8f4f8;
                padding: 15px;
                border-radius: 4px;
                border-left: 4px solid #4a6fa5;
                margin: 20px 0;
            }
            
            .help-column .note.semantic {
                background-color: #e8f5e9;
                border-left-color: #28a745;
            }
            
            .help-column .note.chat {
                background-color: #e8f4f8;
                border-left-color: #4a6fa5;
            }
            
            .help-column .keyboard {
                display: inline-block;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 2px 8px;
                font-family: monospace;
                font-size: 14px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }
            
            .feature-list {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin: 15px 0;
            }
            
            .feature-item {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 4px;
                border-left: 3px solid #4a6fa5;
            }
            
            .feature-item strong {
                display: block;
                margin-bottom: 5px;
                color: #4a6fa5;
            }
            
            .mode-badge {
                display: inline-block;
                background-color: #4a6fa5;
                color: white;
                padding: 4px 10px;
                border-radius: 4px;
                font-size: 12px;
                margin-right: 5px;
            }
            
            .shortcut {
                display: flex;
                align-items: center;
                gap: 10px;
                margin: 10px 0;
            }
            
            .example-box {
                background-color: #f8f9fa;
                padding: 12px;
                border-radius: 6px;
                margin: 10px 0;
                font-family: monospace;
                font-size: 13px;
                border-left: 3px solid #28a745;
            }
            
            @media (max-width: 1400px) {
                .help-grid {
                    grid-template-columns: 1fr 1fr;
                }
            }
            
            @media (max-width: 768px) {
                .help-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📚 Корпусный менеджер - Помощь</h1>
                <a href="/">← На главную</a>
            </div>
            
            <div class="help-grid">
                <!-- Колонка 1: Работа с корпусом -->
                <div class="help-column">
                    <h2>📁 Работа с корпусом</h2>
                    
                    <h3>Загрузка файлов</h3>
                    <p>Поддерживаемые форматы: <strong>TXT, PDF, DOCX, DOC, RTF</strong></p>
                    <p>При загрузке можно указать метаданные:</p>
                    <ul>
                        <li>Название (необязательно)</li>
                        <li>Автор (необязательно)</li>
                        <li>Год издания (необязательно)</li>
                        <li>Жанр (необязательно)</li>
                        <li>Предметная область (по умолчанию "Услуги")</li>
                    </ul>
                    
                    <h3>Поиск и фильтрация</h3>
                    <p><strong>Поиск по слову</strong> - точное совпадение леммы (найдет все формы слова)</p>
                    <p><strong>Фильтр по части речи</strong> - выбор из списка</p>
                    <p><strong>Фильтр по члену предложения</strong> - подлежащее, сказуемое и т.д.</p>
                    <p class="note">💡 Все фильтры работают независимо. Можно искать без слова - только по фильтрам.</p>
                    
                    <h3>Результаты поиска</h3>
                    <p>Для каждого слова показывается:</p>
                    <ul>
                        <li>Слово (исходная форма)</li>
                        <li>Лемма</li>
                        <li>Часть речи</li>
                        <li>Член предложения</li>
                        <li>Контекст (предложение)</li>
                        <li>Информация об источнике</li>
                    </ul>
                    
                    <h3>Редактирование в таблице</h3>
                    <p><strong>Двойной клик по ячейке</strong> позволяет редактировать:</p>
                    <ul>
                        <li>Слово</li>
                        <li>Лемму</li>
                        <li>Часть речи</li>
                        <li>Член предложения</li>
                    </ul>
                    
                    <h3>Управление документами</h3>
                    <ul>
                        <li><strong>Клик по полю</strong> - редактирование метаданных</li>
                        <li><strong>Кнопка 🗑</strong> - удаление документа</li>
                    </ul>
                    
                    <h3>Экспорт</h3>
                    <p>Кнопка "Экспорт JSON" сохраняет текущие результаты поиска в JSON файл</p>
                </div>
                
                <!-- Колонка 2: Синтаксическое дерево -->
                <div class="help-column">
                    <h2>🌳 Синтаксическое дерево</h2>
                    
                    <div class="note">
                        <strong>Двойной клик на контексте предложения</strong> в результатах поиска открывает синтаксическое дерево в новой вкладке.
                    </div>
                    
                    <h3>🎮 Режимы работы</h3>
                    <div class="feature-list">
                        <div class="feature-item">
                            <strong>👆 Выбор</strong>
                            <span>Клик для редактирования слова</span>
                        </div>
                        <div class="feature-item">
                            <strong>✋ Перемещение</strong>
                            <span>Свободное перемещение узлов</span>
                        </div>
                        <div class="feature-item">
                            <strong>🔗 Связь</strong>
                            <span>Создание связей между словами</span>
                        </div>
                    </div>
                    
                    <h3>⌨️ Управление</h3>
                    <div class="shortcut">
                        <span class="keyboard">Ctrl</span> + <span class="keyboard">мышь</span>
                        <span>Панорамирование</span>
                    </div>
                    <div class="shortcut">
                        <span class="keyboard">колесико</span>
                        <span>Масштабирование</span>
                    </div>
                    <div class="shortcut">
                        <span class="keyboard">⟲</span>
                        <span>Сброс вида</span>
                    </div>
                    
                    <h3>📝 Редактирование слова</h3>
                    <p>При клике на слово открывается панель редактирования</p>
                    
                    <h3>🔗 Работа со связями</h3>
                    <ul>
                        <li><strong>Создание:</strong> режим "Связь" → клик на первое слово → клик на второе</li>
                        <li><strong>Изменение типа:</strong> выпадающий список в панели связей</li>
                        <li><strong>Удаление:</strong> двойной клик по линии связи</li>
                    </ul>
                    
                      <!-- Дерево составляющих -->
                    <h3>🌿 Дерево составляющих (Constituency Tree)</h3>
                    <p>Показывает иерархическую структуру предложения: как слова объединяются в фразы (NP, VP, PP и т.д.).</p>
                    
                    <div class="note" style="margin: 15px 0;">
                        <strong>✨ Как открыть:</strong> В окне дерева зависимостей нажмите кнопку 
                        <strong style="background: #28a745; color: white; padding: 4px 10px; border-radius: 4px; font-size: 13px;">🌿 Дерево составляющих</strong> 
                        — дерево откроется в новой вкладке.
                    </div>
                    
                    <ul>
                        <li><strong>Дерево составляющих</strong> строится библиотекой <strong>Stanza</strong> (Stanford NLP) на лету</li>
                        <li>Отображается в виде <strong>горизонтальной ASCII-структуры</strong> с ветками (├── └──)</li>
                        <li>Внизу страницы есть <strong>легенда с расшифровкой всех меток</strong> (S, NP, VP, DT, NN и т.д.)</li>
                        <li><strong>💾 Экспорт в TXT:</strong> кнопка <strong>"Экспорт в TXT"</strong> сохраняет дерево в текстовый файл</li>
                        <li>Дерево составляющих <strong>доступно только для чтения</strong></li>
                    </ul>
                </div>
                
                <!-- Колонка 3: Семантический анализ -->
                <div class="help-column">
                    <h2 class="semantic">🧠 Семантический анализ</h2>
                    
                    <div class="note semantic">
                        <strong>Что это?</strong> Определение точного значения слова в контексте. Отвечает на вопрос <strong>"Что это значит?"</strong>
                    </div>
                    
                    <h3 class="semantic">🤖 Как это работает</h3>
                    <p>Используется <strong>GlossBERT</strong> + <strong>WordNet</strong>:</p>
                    <ol>
                        <li>Анализируется контекст вокруг слова</li>
                        <li>Сравнивается с определениями из WordNet</li>
                        <li>Выбирается наиболее подходящее значение</li>
                    </ol>
                    
                    <div class="example-box">
                        <strong>📖 Пример: слово "bank"</strong><br>
                        • "I went to the <strong>bank</strong> to deposit money" → финансовое учреждение<br>
                        • "The river <strong>bank</strong> was covered with grass" → берег реки
                    </div>
                    
                    <h3 class="semantic">✏️ Редактирование</h3>
                    <p><strong>Клик на ячейку со значением</strong> позволяет исправить или добавить значение вручную.</p>
                    
                    <h3 class="semantic">💾 Экспорт</h3>
                    <p>Доступны форматы <strong>TXT</strong> и <strong>JSON</strong></p>
                </div>
                
                <!-- Колонка 4:  Чат-бот  -->
                <div class="help-column">
                    <h2 class="chat">💬 Чат-бот</h2>
                    
                    <div class="note chat">
                        <strong>🤖 Что это?</strong> Интеллектуальный помощник, который отвечает на вопросы, используя <strong>ваши документы</strong> из корпуса. Работает на технологии RAG (Retrieval-Augmented Generation).
                    </div>
                    
                    <h3 class="chat">🎯 Как это работает</h3>
                    <ol>
                        <li>Вы задаёте вопрос на английском</li>
                        <li>Система ищет <strong>релевантные предложения</strong> в загруженных документах</li>
                        <li>LLM (локальная модель Qwen) <strong>генерирует ответ</strong> только на основе найденных документов</li>
                        <li>Вы получаете <strong>точный ответ с указанием источников</strong></li>
                    </ol>
                    
                    <h3 class="chat">💬 Управление диалогом</h3>
                    <ul>
                        <li><strong>Слева</strong> — список всех чатов (название = первому вопросу)</li>
                        <li><strong>Клик на чат</strong> — открыть историю</li>
                        <li><strong>New Chat</strong> — начать новый диалог</li>
                        <li><strong>🗑 на чате</strong> — удалить всю сессию</li>
                    </ul>
                    
                    <h3 class="chat">✏️ Редактирование сообщений</h3>
                    <p><strong>Наведите на сообщение</strong> — появятся кнопки:</p>
                    <ul>
                        <li><strong>✏️ Edit</strong> — изменить текст сообщения</li>
                        <li><strong>🗑 Delete</strong> — удалить сообщение</li>
                    </ul>
                    <p class="note chat">💡 Можно редактировать и свои сообщения, и ответы бота. История синхронизируется с БД.</p>
                    
                    <h3 class="chat">💾 Сохранение чата</h3>
                    <p>Кнопка <strong>"💾 Save Chat"</strong> вверху страницы сохраняет весь диалог в TXT файл с указанием:</p>
                    <ul>
                        <li>Времени каждого сообщения</li>
                        <li>Роли (User/Assistant)</li>
                        <li>Источников ответов</li>
                    </ul>
                    
                    <h3 class="chat">🔍 Особенности</h3>
                    <ul>
                        <li><strong>Только английский</strong> — модель отвечает на английском (документы на английском)</li>
                        <li><strong>Ответы по фактам</strong> — LLM не выдумывает информацию, только из документов</li>
                        <li><strong>Указание источников</strong> — видно, из какого файла взят ответ</li>
                        <li><strong>Локальная работа</strong> — не требует интернета после загрузки модели</li>
                    </ul>
                    
                    <div class="example-box">
                        <strong>📋 Пример вопроса:</strong><br>
                        User: "What does the document say about teenagers?"<br>
                        Bot: "The teenager spent his entire weekend listening to loud rock music with his headphones, annoying his parents who preferred classical."<br>
                        <span style="font-size: 11px; color: #888;">📄 Sources: document1.txt</span>
                    </div>
                    
                    <h3 class="chat">⚠️ Важно</h3>
                    <ul>
                        <li>Для работы нужна загруженная модель Qwen (~1.5GB, скачивается при первом запуске)</li>
                        <li>Чат работает только с английскими документами</li>
                        <li>Если ответа нет в документах, бот честно сообщит об этом</li>
                    </ul>
                </div>
            </div>
        </div>
    </body>
    </html>
    """