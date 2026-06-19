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
                max-width: 1400px;
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
                grid-template-columns: 1fr 1fr;
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
            
            .help-column h3 {
                color: #4a6fa5;
                margin: 20px 0 10px 0;
                font-size: 18px;
            }
            
            .help-column h3:first-of-type {
                margin-top: 0;
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
                <!-- Левая колонка - Работа с корпусом -->
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
                    <p>Внизу отображается общее количество найденных вхождений</p>
                    
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
                
                <!-- Правая колонка - Работа с синтаксическими деревьями -->
                <div class="help-column">
                    <h2>🌳 Синтаксические деревья</h2>
                    
                    <div class="note">
                        <strong>Двойной клик на контексте предложения</strong> в результатах поиска открывает синтаксическое дерево в новой вкладке.
                    </div>
                    
                    <!-- Дерево зависимостей -->
                    <h3>🔗 Дерево зависимостей (Dependency Tree)</h3>
                    <p>Показывает синтаксические связи между словами: подлежащее, сказуемое, дополнение и т.д.</p>
                    
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
                        <span>Панорамирование (движение по полю)</span>
                    </div>
                    
                    <div class="shortcut">
                        <span class="keyboard">колесико</span>
                        <span>Масштабирование</span>
                    </div>
                    
                    <div class="shortcut">
                        <span class="keyboard">кнопки +/-</span>
                        <span>Быстрое масштабирование</span>
                    </div>
                    
                    <div class="shortcut">
                        <span class="keyboard">⟲</span>
                        <span>Сброс вида</span>
                    </div>
                    
                    <h3>📝 Редактирование слова</h3>
                    <p>При клике на слово открывается панель редактирования:</p>
                    <ul>
                        <li>Изменение текста слова</li>
                        <li>Изменение леммы</li>
                        <li>Выбор части речи</li>
                        <li>Выбор члена предложения</li>
                    </ul>
                    
                    <h3>🔗 Работа со связями</h3>
                    <ul>
                        <li><strong>Создание:</strong> режим "Связь" → клик на первое слово → клик на второе</li>
                        <li><strong>Изменение типа:</strong> выпадающий список в панели связей</li>
                        <li><strong>Удаление:</strong> двойной клик по линии связи или кнопка 🗑</li>
                    </ul>
                    
                    <h3>💾 Сохранение изменений</h3>
                    <ul>
                        <li><strong>"Сохранить в БД"</strong> - сохраняет все изменения (слова и связи)</li>
                        <li><strong>"Экспорт HTML"</strong> - создает отдельный файл с интерактивным деревом</li>
                    </ul>
                    
                    <h3>📊 Панель связей</h3>
                    <p>Внизу отображается список всех связей между словами. Можно:</p>
                    <ul>
                        <li>Изменить тип связи через выпадающий список</li>
                        <li>Удалить связь кнопкой 🗑</li>
                    </ul>                   
                    
                    <h3>📌 Подсказки</h3>
                    <ul>
                        <li><strong>При наведении на слово</strong> - всплывающая подсказка с леммой и частью речи</li>
                        <li><strong>При клике на слово</strong> - панель редактирования</li>
                        <li><strong>Выделенное слово</strong> подсвечивается желтой рамкой</li>
                    </ul>
                    
                    <h3>📋 Авторасположение</h3>
                    <p>Кнопка "Авторасположение" возвращает узлы в исходное положение</p>

                    <hr style="margin: 25px 0; border: none; border-top: 1px solid #ddd;">
                    
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
            </div>
        </div>
    </body>
    </html>
    """