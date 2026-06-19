import networkx as nx
import matplotlib.pyplot as plt

# Создаем пустой граф
print("Выберите тип графа:")
print("1. Неориентированный граф")
print("2. Ориентированный граф")
graph_type = int(input('Ваш выбор (1 или 2): '))
graph = nx.DiGraph() if graph_type == 2 else nx.Graph()

def show_graph(g):
    nx.draw(g, with_labels=True, node_color='lightblue', edge_color='gray')
    plt.show()

def add_node(g):
    node_name = input('Введите название нового узла: ')
    g.add_node(node_name)
    print(f"Узел {node_name} добавлен.")

def add_edge(g):
    node1 = input('Введите первый узел: ')
    node2 = input('Введите второй узел: ')
    g.add_edge(node1, node2)
    print(f"Ребро между {node1} и {node2} добавлено.")

def connect_components(g):
    if nx.is_connected(g):
        print("Граф уже связный.")
    else:
        components = list(nx.connected_components(g))
        for i in range(len(components) - 1):
            g.add_edge(list(components[i])[0], list(components[i + 1])[0])
        print("Граф приведен к связному.")

def hamiltonian_cycles(g):
    cycles = list(nx.simple_cycles(g.to_directed()))
    print("Гамильтоновы циклы:", cycles if cycles else "Циклов нет.")

def calculate_graph_properties(g):
    if nx.is_connected(g):
        print(f"Диаметр графа: {nx.diameter(g)}")
        print(f"Радиус графа: {nx.radius(g)}")
        print(f"Центр графа: {nx.center(g)}")
    else:
        print("Граф не связный, невозможно вычислить диаметр, радиус и центр.")

def graph_products():
    G1 = nx.Graph()
    G1.add_edges_from([(1, 2), (2, 3)])
    G2 = nx.Graph()
    G2.add_edges_from([(4, 5), (5, 6)])
    tensor_prod = nx.tensor_product(G1, G2)
    cartesian_prod = nx.cartesian_product(G1, G2)
    print("Тензорное произведение:", list(tensor_prod.edges()))
    print("Декартово произведение:", list(cartesian_prod.edges()))

def adjacency_matrix(g):
    matrix = nx.adjacency_matrix(g).toarray()
    print("Матрица смежности графа:")
    print(matrix)
    connected = nx.is_connected(g)
    print("Граф связный:", connected)

# Основное меню
while True:
    if plt.fignum_exists(1):
        plt.close(1)
    
    print("\n--- Меню ---")
    print("1. Отобразить граф")
    print("2. Добавить узел")
    print("3. Добавить ребро")
    print("4. Приведение графа к связному")
    print("5. Нахождение гамильтоновых циклов")
    print("6. Диаметр, радиус, центр графа")
    print("7. Тензорное и декартово произведение графов")
    print("8. Матрица смежности и проверка связности")
    print("9. Выход")
    choice = input("Ваш выбор: ")

    if choice == '1':
        show_graph(graph)
    elif choice == '2':
        add_node(graph)
    elif choice == '3':
        add_edge(graph)
    elif choice == '4':
        connect_components(graph)
    elif choice == '5':
        hamiltonian_cycles(graph)
    elif choice == '6':
        calculate_graph_properties(graph)
    elif choice == '7':
        graph_products()
    elif choice == '8':
        adjacency_matrix(graph)
    elif choice == '9':
        print("Выход из программы.")
        break
    else:
        print("Неверный ввод, попробуйте снова.")