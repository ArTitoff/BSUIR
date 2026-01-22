import networkx as nx
import matplotlib.pyplot as plt
import pickle  # Импортируем библиотеку для сериализации
import numpy as np  # Импортируем numpy для работы с матрицами

def save_graphs(graphs, filename, pos):
    """Сохраняет все графы и их позиции узлов в файл."""
    with open(filename, 'wb') as f:
        data_to_save = {
            'graphs': graphs,
            'positions': pos
        }
        pickle.dump(data_to_save, f)
    print(f"Graphs and positions saved to '{filename}'.")

def load_graphs(filename):
    """Загружает графы и их позиции из файла."""
    try:
        with open(filename, 'rb') as f:
            data_loaded = pickle.load(f)
            graphs = data_loaded['graphs']
            pos = data_loaded['positions']
        print(f"Graphs and positions loaded from '{filename}'.")
        return graphs, pos
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return {}, {}
    except Exception as e:
        print(f"Error loading graphs: {e}")
        return {}, {}
        
def incidence_matrix(graph):
    """Возвращает матрицу инцидентности графа."""
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    
    # Инициализация матрицы нулями
    matrix = np.zeros((num_nodes, num_edges), dtype=int)

    # Получаем список узлов
    nodes_list = list(graph.nodes())
    
    # Заполнение матрицы
    for i, (u, v) in enumerate(graph.edges()):
        matrix[nodes_list.index(u), i] = 1  # Увеличиваем инцидентность для вершины u
        matrix[nodes_list.index(v), i] = 1  # Увеличиваем инцидентность для вершины v
    
    return matrix

def is_complete_graph(graph):
    """Проверяет, является ли граф полным."""
    num_nodes = graph.number_of_nodes()
    if num_nodes < 2:
        return True  # Граф с 0 или 1 вершиной считается полным
    
    expected_edges = num_nodes * (num_nodes - 1) // 2
    actual_edges = graph.number_of_edges()
    
    return actual_edges == expected_edges

def show_graph_info(directed_graph, undirected_graph, graph_name):
    """Выводит информацию о графе: количество вершин, дуг, степени, матрицу инцидентности и полноту."""
    node_count = directed_graph.number_of_nodes()
    directed_edge_count = directed_graph.number_of_edges()
    undirected_edge_count = undirected_graph.number_of_edges()
    total_edge_count = directed_edge_count + undirected_edge_count
    
    print(f"Информация для графа '{graph_name}':")
    print(f"Количество вершин: {node_count}")
    print(f"Количество ориентированных дуг: {directed_edge_count}")
    print(f"Количество неориентированных дуг: {undirected_edge_count}")
    print(f"Общее количество дуг: {total_edge_count}")

    # Матрица инцидентности
    inc_matrix = incidence_matrix(undirected_graph)
    print("Матрица инцидентности:")
    print(inc_matrix)

    # Проверка на полноту
    if is_complete_graph(undirected_graph):
        print("Граф является полным.")
    else:
        print("Граф не является полным.")

    # Степени всех вершин
    print("Степени всех вершин:")
    for node in directed_graph.nodes():
        directed_degree = directed_graph.in_degree(node)
        undirected_degree = undirected_graph.degree(node)
        total_degree = directed_degree + undirected_degree
        print(f"Вершина {node}: степень (ориентированные + неориентированные) {total_degree} (ориентированные: {directed_degree}, неориентированные: {undirected_degree})")

def show_node_degree(directed_graph, undirected_graph, node_id):
    #Показывает степень для выбранной вершины."""
    if node_id in directed_graph or node_id in undirected_graph:
        directed_degree = directed_graph.in_degree(node_id) if node_id in directed_graph else 0
        undirected_degree = undirected_graph.degree(node_id)

        total_degree = directed_degree + undirected_degree
        print(f"Степень вершины {node_id}: {total_degree} (ориентированные: {directed_degree}, неориентированные: {undirected_degree})")
    else:
        print(f"Вершина {node_id} не найдена в графе.")

def convert_to_complete_graph(graph):
    """Приводит произвольный граф к полному графу."""
    nodes = list(graph.nodes())
    num_nodes = len(nodes)

    # Получаем все возможные рёбра между вершинами
    complete_edges = {(nodes[i], nodes[j]) for i in range(num_nodes) for j in range(i + 1, num_nodes)}

    # Получаем существующие рёбра
    existing_edges = set(graph.edges())

    # Находим недостающие рёбра
    missing_edges = complete_edges - existing_edges

    # Добавляем недостающие рёбра в граф
    for edge in missing_edges:
        graph.add_edge(edge[0], edge[1])  # Для неориентированного графа

    print(f"Граф преобразован в полный граф с {graph.number_of_edges()} рёбрами.")

def is_eulerian_combined(directed_graph, undirected_graph):
    """Проверяет, является ли граф эйлеровым, учитывая и направленные, и ненаправленные рёбра."""
    # Проверка направленного графа
    for node in directed_graph.nodes():
        if directed_graph.in_degree(node) != directed_graph.out_degree(node):
            return False
    # Проверка ненаправленного графа
    for node in undirected_graph.nodes():
        if undirected_graph.degree(node) % 2 != 0:
            return False
    # Проверка на связанность ненаправленного графа
    return nx.is_connected(undirected_graph)

def find_eulerian_cycle_combined(directed_graph, undirected_graph):
    """Находит эйлеров цикл в графе с одновременно направленными и ненаправленными рёбрами."""
    if not is_eulerian_combined(directed_graph, undirected_graph):
        print("Граф не имеет эйлерова цикла.")
        return None

    # Создаем копию графа для работы
    combined_graph = nx.MultiGraph()  # Используем MultiGraph, чтобы учитывать все рёбра
    combined_graph.add_nodes_from(directed_graph.nodes())
    combined_graph.add_edges_from(directed_graph.edges())
    
    # Добавляем ненаправленные рёбра, рассматривая их как направленные в обе стороны
    for u, v in undirected_graph.edges():
        combined_graph.add_edge(u, v)
        combined_graph.add_edge(v, u)

    start_node = next(iter(combined_graph.nodes()))
    cycle = []
    stack = [start_node]

    while stack:
        current_node = stack[-1]
        if combined_graph.degree(current_node) > 0:
            # Берем первый сосед и удаляем его
            for neighbor in list(combined_graph.neighbors(current_node)):
                stack.append(neighbor)
                combined_graph.remove_edge(current_node, neighbor)
                break
        else:
            cycle.append(stack.pop())

    return cycle[::-1]  # Возвращаем цикл в правильном порядке

def find_shortest_path_combined(directed_graph, undirected_graph, start_node, end_node):
    """Находит кратчайший путь в графе с одновременно направленными и ненаправленными рёбрами."""
    # Создаем комбинированный граф
    combined_graph = nx.Graph()
    
    # Добавляем ориентированные рёбра
    combined_graph.add_edges_from(directed_graph.edges())
    
    # Добавляем ненаправленные рёбра (в обе стороны)
    for u, v in undirected_graph.edges():
        combined_graph.add_edge(u, v)
        combined_graph.add_edge(v, u)

    # Поиск кратчайшего пути в комбинированном графе
    try:
        return nx.shortest_path(combined_graph, source=start_node, target=end_node)
    except nx.NetworkXNoPath:
        return None
    except nx.NetworkXError as e:
        print(f"Ошибка: {e}")
        return None

def find_all_paths_combined(directed_graph, undirected_graph, start_node, end_node):
    """Находит все простые пути в графе с одновременно направленными и ненаправленными рёбрами."""
    # Создаем комбинированный граф
    combined_graph = nx.Graph()
    
    # Добавляем ориентированные рёбра
    combined_graph.add_edges_from(directed_graph.edges())
    
    # Добавляем ненаправленные рёбра (в обе стороны)
    for u, v in undirected_graph.edges():
        combined_graph.add_edge(u, v)
        combined_graph.add_edge(v, u)

    # Поиск всех путей
    return list(nx.all_simple_paths(combined_graph, source=start_node, target=end_node)) 
  
def calculate_combined_distance(directed_graph, undirected_graph, node1, node2):
    """Вычисляет расстояние между двумя узлами в комбинированном графе."""
    # Создаем комбинированный граф
    combined_graph = nx.Graph()
    
    # Добавляем ориентированные ребра
    combined_graph.add_edges_from(directed_graph.edges())
    
    # Добавляем ненаправленные ребра (в обе стороны)
    for u, v in undirected_graph.edges():
        combined_graph.add_edge(u, v)
        combined_graph.add_edge(v, u)

    # Вычисляем расстояние
    try:
        distance = nx.shortest_path_length(combined_graph, source=node1, target=node2)
        return distance
    except nx.NetworkXNoPath:
        print(f"Нет пути между узлами {node1} и {node2}.")
        return None
    except Exception as e:
        print(f"Ошибка при вычислении расстояния: {e}")
        return None

def add_node_content(graph, node_id, text_content, file_link):
    """Добавляет текстовое содержимое и ссылку на файл к узлу."""
    if node_id in graph:
        graph.nodes[node_id]['text_content'] = text_content
        graph.nodes[node_id]['file_link'] = file_link
        print(f"Содержимое узла '{node_id}' обновлено.")
    else:
        print(f"Узел '{node_id}' не найден в графе.")

def remove_node_content(graph, node_id):
    """Удаляет содержимое узла (текст и ссылка на файл)."""
    if node_id in graph:
        if 'text_content' in graph.nodes[node_id]:
            del graph.nodes[node_id]['text_content']
        if 'file_link' in graph.nodes[node_id]:
            del graph.nodes[node_id]['file_link']
        print(f"Содержимое узла '{node_id}' удалено.")
    else:
        print(f"Узел '{node_id}' не найден в графе.")           

def edit_node_content(graph, node_id, new_text_content=None, new_file_link=None):
    """Редактирует текстовое содержимое и ссылку на файл узла."""
    if node_id in graph:
        if new_text_content is not None:
            graph.nodes[node_id]['text_content'] = new_text_content
        if new_file_link is not None:
            graph.nodes[node_id]['file_link'] = new_file_link
        print(f"Содержимое узла '{node_id}' обновлено.")
    else:
        print(f"Узел '{node_id}' не найден в графе.")

def view_node_content(graph, node_id):
    """Просматривает содержимое узла (текст и ссылка на файл)."""
    if node_id in graph:
        text_content = graph.nodes[node_id].get('text_content', 'Нет текстового содержимого.')
        file_link = graph.nodes[node_id].get('file_link', 'Нет ссылки на файл.')
        print(f"Содержимое узла '{node_id}':")
        print(f"Текст: {text_content}")
        print(f"Ссылка на файл: {file_link}")
    else:
        print(f"Узел '{node_id}' не найден в графе.")

def display_menu():
    print("\n--- Меню Редактора Графов ---")
    print("1. Создать новый граф")
    print("2. Переключить граф")
    print("3. Добавить узел")
    print("4. Удалить узел")
    print("5. Добавить направленное ребро")
    print("6. Добавить ненаправленное ребро")
    print("7. Удалить направленное ребро")
    print("8. Удалить ненаправленное ребро")
    print("9. Показать информацию о графе")
    print("10. Визуализировать граф")
    print("11. Переименовать узел")
    print("12. Переместить узел")
    print("13. Установить цвет узла")
    print("14. Установить цвет ребра")
    print("15. Установить форму узла")
    print("16. Сохранить графы")
    print("17. Загрузить графы")
    print("18. Привести граф к полному")
    print("19. Проверить наличие эйлерова цикла")
    print("20. Поиск всех путей")
    print("21. Поиск кратчайшего пути")
    print("22. Вычислить расстояние между узлами")
    print("23. Добавить содержимое к узлу")
    print("24. Удалить содержимое узла")
    print("25. Редактировать содержимое узла")
    print("26. Просмотреть содержимое узла")
    print("27. Выход")
    print("-------------------------")

def draw_nodes_with_shapes(graph, pos, node_colors, node_shapes):
    for node in graph.nodes():
        x, y = pos.get(node, (0, 0))
        color = node_colors.get(node, 'lightblue')
        shape = node_shapes.get(node, 'o')  # Форма по умолчанию (круг)

        if shape == 'o':
            plt.scatter(x, y, s=700, color=color, edgecolor='black', alpha=0.7)
        elif shape == 's':
            plt.scatter(x, y, s=700, color=color, marker='s', edgecolor='black', alpha=0.7)
        elif shape == '^':
            plt.scatter(x, y, s=700, color=color, marker='^', edgecolor='black', alpha=0.7)
        elif shape == 'D':
            plt.scatter(x, y, s=700, color=color, marker='D', edgecolor='black', alpha=0.7)
        elif shape == 'p':
            plt.scatter(x, y, s=700, color=color, marker='p', edgecolor='black', alpha=0.7)

def main():
    graphs = {}
    current_graph_name = None
    pos = {}  # Словарь для хранения позиций узлов
    node_colors = {}  # Цвета узлов
    edge_colors = {}  # Цвета ребер
    node_shapes = {}  # Формы узлов

    while True:
        display_menu()
        choice = input("Выберите пункт: ")

        if choice == '1':
            graph_name = input("Введите название нового графа: ")
            if graph_name not in graphs:
                graphs[graph_name] = {
                    'directed': nx.DiGraph(),  # Ориентированный граф
                    'undirected': nx.Graph()    # Неориентированный граф
                }
                print(f"Граф '{graph_name}' создан.")
            else:
                print(f"Граф '{graph_name}' уже существует.")

        elif choice == '2':
            graph_name = input("Введите имя графа, на который хотите переключиться: ")
            if graph_name in graphs:
                current_graph_name = graph_name
                print(f"Переключились на граф '{current_graph_name}'.")
            else:
                print(f"Граф '{graph_name}' не существует.")

        elif choice == '3':
            if current_graph_name:
                node_id = input("Введите ID узла для добавления: ")
                graphs[current_graph_name]['directed'].add_node(node_id)
                graphs[current_graph_name]['undirected'].add_node(node_id)
                pos[node_id] = (0, 0)  # Инициализация позиции узла
                node_colors[node_id] = 'lightblue'  # Цвет по умолчанию
                node_shapes[node_id] = 'o'  # Форма по умолчанию (круг)
                print(f"Узел '{node_id}' добавлен в граф '{current_graph_name}'.")
            else:
                print("Граф не выбран.")

        elif choice == '4':
            if current_graph_name:
                node_id = input("Введите ID узла для удаления: ")
                if node_id in graphs[current_graph_name]['directed']:
                    graphs[current_graph_name]['directed'].remove_node(node_id)
                if node_id in graphs[current_graph_name]['undirected']:
                    graphs[current_graph_name]['undirected'].remove_node(node_id)
                if node_id in pos:
                    del pos[node_id]  # Удаляем позицию узла
                if node_id in node_colors:
                    del node_colors[node_id]  # Удаляем цвет узла
                if node_id in node_shapes:
                    del node_shapes[node_id]  # Удаляем форму узла
                print(f"Узел '{node_id}' удалён из графа '{current_graph_name}'.")
            else:
                print("Граф не выбран.")

        elif choice == '5':
            if current_graph_name:
                from_node = input("Введите ID начального узла (направленное): ")
                to_node = input("Введите ID конечного узла (направленное): ")
                if from_node in graphs[current_graph_name]['directed'] and to_node in graphs[current_graph_name]['directed']:
                    graphs[current_graph_name]['directed'].add_edge(from_node, to_node)
                    # Установка цвета по умолчанию для ребра
                    edge_colors[(from_node, to_node)] = 'black'
                    print(f"Направленное ребро от '{from_node}' к '{to_node}' добавлено в граф '{current_graph_name}'.")
                else:
                    print("Один или оба узла не существуют в направленном графе.")
            else:
                print("Граф не выбран.")

        elif choice == '6':
            if current_graph_name:
                node1 = input("Введите ID первого узла (ненаправленное): ")
                node2 = input("Введите ID второго узла (ненаправленное): ")
                if node1 in graphs[current_graph_name]['undirected'] and node2 in graphs[current_graph_name]['undirected']:
                    graphs[current_graph_name]['undirected'].add_edge(node1, node2)
                    edge_colors[(node1, node2)] = 'black'  # Установка цвета по умолчанию для ребра
                    print(f"Ненаправленное ребро между '{node1}' и '{node2}' добавлено в граф '{current_graph_name}'.")
                else:
                    print("Один или оба узла не существуют в ненаправленном графе.")
            else:
                print("Граф не выбран.")

        elif choice == '7':
            if current_graph_name:
                from_node = input("Введите ID начального узла (направленное): ")
                to_node = input("Введите ID конечного узла (направленное): ")
                if (from_node, to_node) in graphs[current_graph_name]['directed'].edges():
                    graphs[current_graph_name]['directed'].remove_edge(from_node, to_node)
                    edge_key = (from_node, to_node)
                    if edge_key in edge_colors:
                        del edge_colors[edge_key]  # Удаляем цвет ребра
                    else:
                        print(f"Цвет ребра для {edge_key} не существует, пропускаем удаление.")
                    print(f"Направленное ребро от '{from_node}' к '{to_node}' удалено из графа '{current_graph_name}'.")
                else:
                    print("Направленное ребро не существует в текущем графе.")
            else:
                print("Граф не выбран.")

        elif choice == '8':
            if current_graph_name:
                node1 = input("Введите ID первого узла (ненаправленное): ")
                node2 = input("Введите ID второго узла (ненаправленное): ")
                if (node1, node2) in graphs[current_graph_name]['undirected'].edges() or (node2, node1) in graphs[current_graph_name]['undirected'].edges():
                    graphs[current_graph_name]['undirected'].remove_edge(node1, node2)
                    edge_key = (node1, node2)
                    if edge_key in edge_colors:
                        del edge_colors[edge_key]  # Удаляем цвет ребра
                    else:
                        print(f"Цвет ребра для {edge_key} не существует, пропускаем удаление.")
                    print(f"Ненаправленное ребро между '{node1}' и '{node2}' удалено из графа '{current_graph_name}'.")
                else:
                    print("Ненаправленное ребро не существует в текущем графе.")
            else:
                print("Граф не выбран.")

        elif choice == '9':
            if current_graph_name:
                directed_graph = graphs[current_graph_name]['directed']
                undirected_graph = graphs[current_graph_name]['undirected']
                
                show_graph_info(directed_graph, undirected_graph, current_graph_name)
                
                # Запрос степени для выбранной вершины
                node_id = input("Введите ID вершины для получения её степени (или нажмите Enter, чтобы пропустить): ")
                if node_id:
                    show_node_degree(directed_graph, undirected_graph, node_id)
            else:
                print("Граф не выбран.")
        elif choice == '10':
            if current_graph_name:
                plt.figure(figsize=(8, 6))
                
                directed_graph = graphs[current_graph_name]['directed']
                undirected_graph = graphs[current_graph_name]['undirected']
                
                # Получаем все узлы
                all_nodes = set(directed_graph.nodes()).union(set(undirected_graph.nodes()))
                
                pos = {node: pos.get(node, (0, 0)) for node in all_nodes}  # Установить (0, 0) для отсутствующих узлов

                # Визуализация рёбер ненаправленного графа
                nx.draw_networkx_edges(undirected_graph, pos, 
                                        edge_color=[edge_colors.get((u, v), 'black') for u, v in undirected_graph.edges()])
                
                # Визуализация рёбер направленного графа
                nx.draw_networkx_edges(directed_graph, pos, 
                                        arrowstyle='-|>', arrowsize=20, 
                                        edge_color=[edge_colors.get((u, v), 'black') for u, v in directed_graph.edges()])
                
                # Визуализация узлов
                draw_nodes_with_shapes(directed_graph, pos, node_colors, node_shapes)
                
                # Визуализация меток узлов
                nx.draw_networkx_labels(directed_graph, pos)
                
                plt.title(f"Graph Visualization: {current_graph_name}")
                plt.axis('equal')  # Сохраняем равные масштабы по обеим осям
                plt.show()
                print("Нажмите Enter для возвращния в меню...")
                input()  # Ждем, пока пользователь нажмет Enter
            else:
                print("Граф не выбран.")
   
        elif choice == '11':
            if current_graph_name:
                choose_node = input("Введите ID узла, который хотите переименовать: ")
                change_node = input("Введите новое имя: ")

                if choose_node in graphs[current_graph_name]['directed']:
                    mapping = {choose_node: change_node}
                    graphs[current_graph_name]['directed'] = nx.relabel_nodes(graphs[current_graph_name]['directed'], mapping)
                    graphs[current_graph_name]['undirected'] = nx.relabel_nodes(graphs[current_graph_name]['undirected'], mapping)
                    if choose_node in pos:
                        pos[change_node] = pos.pop(choose_node)  # Обновляем позицию узла
                    if choose_node in node_colors:
                        node_colors[change_node] = node_colors.pop(choose_node)  # Обновляем цвет узла
                    if choose_node in node_shapes:
                        node_shapes[change_node] = node_shapes.pop(choose_node)  # Обновляем форму узла
                    print(f"Узел {choose_node} переименован в {change_node}.")
                else:
                    print(f"Узел {choose_node} не найден в графе.")
            else:
                print("Граф не выбран.")

        elif choice == '12':
            if current_graph_name:
                choose_node = input("Введите ID узла, который хотите переместить: ")

                if choose_node in graphs[current_graph_name]['directed']:
                    try:
                        position1 = float(input("Введите координату X: "))
                        position2 = float(input("Введите координату Y: "))
                        new_position = (position1, position2)

                        # Обновляем координаты узла
                        pos[choose_node] = new_position  
                        print(f"Узел {choose_node} перемещён в новую позицию {new_position}.")
                    except ValueError:
                        print("Ошибка: координаты должны быть числовыми значениями.")
                else:
                    print(f"Узел {choose_node} не найден в графе.")                
            else:
                print("Граф не выбран.")

        elif choice == '13':
            if current_graph_name:
                node_id = input("Введите ID узла, цвет которого хотите изменить: ")
                new_color = input("Введите новый цвет (например, 'red', 'blue', '#FF5733'): ")
                if node_id in node_colors:
                    node_colors[node_id] = new_color
                    print(f"Цвет узла '{node_id}' изменен на '{new_color}'.")
                else:
                    print(f"Узел '{node_id}' не найден.")
            else:
                print("Граф не выбран.")

        elif choice == '14':
            if current_graph_name:
                from_node = input("Введите ID начального узла: ")
                to_node = input("Введите ID конечного узла: ")
                new_color = input("Введите новый цвет для ребра (например, 'red', 'blue', '#FF5733'): ")

                # Проверяем, является ли ребро направленным
                if (from_node, to_node) in graphs[current_graph_name]['directed'].edges():
                    edge_colors[(from_node, to_node)] = new_color
                    print(f"Цвет направленного ребра от '{from_node}' к '{to_node}' изменен на '{new_color}'.")
                
                # Проверяем, является ли ребро ненаправленным
                elif (to_node, from_node) in graphs[current_graph_name]['undirected'].edges():
                    edge_colors[(to_node, from_node)] = new_color
                    print(f"Цвет ненаправленного ребра между '{from_node}' и '{to_node}' изменен на '{new_color}'.")
                
                else:
                    print("Такое ребро не существует.")
            else:
                print("Граф не выбран.")

        elif choice == '15':
            if current_graph_name:
                node_id = input("Введите ID узла, форму которого хотите изменить (доступные: 'o', 's', '^', 'D', 'p'): ")
                new_shape = input("Введите новую форму (например, 'o' для круга, 's' для квадрата): ")
                if node_id in node_shapes:
                    node_shapes[node_id] = new_shape
                    print(f"Форма узла '{node_id}' изменена на '{new_shape}'.")
                else:
                    print(f"Узел '{node_id}' не найден.")
            else:
                print("Граф не выбран.")

        elif choice == '16':
            filename = input("Введите название файла, в который сохраните графы: ")
            save_graphs(graphs, filename, pos)

        elif choice == '17':
            filename = input("Введите название файла, из которого загрузите графы: ")
            loaded_graphs, loaded_pos = load_graphs(filename)  # Загружаем и графы, и позиции
            if loaded_graphs:
                graphs = loaded_graphs
                pos = loaded_pos  # Обновляем позиции узлов
                current_graph_name = list(graphs.keys())[0]

        elif choice == '18':  
            if current_graph_name:
                undirected_graph = graphs[current_graph_name]['undirected']
                convert_to_complete_graph(undirected_graph)
            else:
                print("Граф не выбран.")

        elif choice == '19':
            if current_graph_name:
                directed_graph = graphs[current_graph_name]['directed']
                undirected_graph = graphs[current_graph_name]['undirected']
                
                # Проверка наличия эйлерова цикла
                if is_eulerian_combined(directed_graph, undirected_graph):
                    print("Эйлеров цикл в графе с направленными и ненаправленными рёбрами:")
                    cycle = find_eulerian_cycle_combined(directed_graph, undirected_graph)
                    if cycle:
                        print(cycle)
                else:
                    print("Граф не имеет эйлерова цикла.")
        elif choice == '20':  # Поиск всех путей в комбинированном графе
            if current_graph_name:
                start_node = input("Введите ID начального узла: ")
                end_node = input("Введите ID конечного узла: ")
                all_paths = find_all_paths_combined(
                    graphs[current_graph_name]['directed'], 
                    graphs[current_graph_name]['undirected'], 
                    start_node, 
                    end_node
                )
                if all_paths:
                    print(f"Все пути от '{start_node}' до '{end_node}':")
                    for path in all_paths:
                        print(path)
                else:
                    print(f"Нет путей от '{start_node}' до '{end_node}'.")
            else:
                print("Граф не выбран.")

        elif choice == '21':  # Поиск кратчайшего пути в комбинированном графе
            if current_graph_name:
                start_node = input("Введите ID начального узла: ")
                end_node = input("Введите ID конечного узла: ")
                shortest_path = find_shortest_path_combined(
                    graphs[current_graph_name]['directed'], 
                    graphs[current_graph_name]['undirected'], 
                    start_node, 
                    end_node
                )
                if shortest_path:
                    print(f"Кратчайший путь от '{start_node}' до '{end_node}': {shortest_path}")
                else:
                    print(f"Нет пути от '{start_node}' до '{end_node}'.")
            else:
                print("Граф не выбран.")
        elif choice == '22':
            if current_graph_name:
                node1 = input("Введите ID первого узла: ")
                node2 = input("Введите ID второго узла: ")
                directed_graph = graphs[current_graph_name]['directed']
                undirected_graph = graphs[current_graph_name]['undirected']
                
                # Вычисляем расстояние в комбинированном графе
                distance = calculate_combined_distance(directed_graph, undirected_graph, node1, node2)
                if distance is not None:
                    print(f"Расстояние между узлами {node1} и {node2} в комбинированном графе: {distance}")
            else:
                print("Граф не выбран.")
        elif choice == '23':
            if current_graph_name:
                node_id = input("Введите ID узла: ")
                text_content = input("Введите текстовое содержимое: ")
                file_link = input("Введите ссылку на файл: ")
                directed_graph = graphs[current_graph_name]['directed']
                add_node_content(directed_graph, node_id, text_content, file_link)
            else:
                print("Граф не выбран.")

        elif choice == '24':
            if current_graph_name:
                node_id = input("Введите ID узла для удаления содержимого: ")
                directed_graph = graphs[current_graph_name]['directed']
                remove_node_content(directed_graph, node_id)
            else:
                print("Граф не выбран.")

        elif choice == '25':
            if current_graph_name:
                node_id = input("Введите ID узла для редактирования содержимого: ")
                new_text_content = input("Введите новое текстовое содержимое (или оставьте пустым для пропуска): ")
                new_file_link = input("Введите новую ссылку на файл (или оставьте пустым для пропуска): ")
                directed_graph = graphs[current_graph_name]['directed']
                edit_node_content(directed_graph, node_id, new_text_content or None, new_file_link or None)
            else:
                print("Граф не выбран.")

        elif choice == '26':
            if current_graph_name:
                node_id = input("Введите ID узла для просмотра содержимого: ")
                directed_graph = graphs[current_graph_name]['directed']
                view_node_content(directed_graph, node_id)
            else:
                print("Граф не выбран.")
        elif choice == '27':
            print("Exiting the Graph Editor.")
            break

        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()