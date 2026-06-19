#include "OrientedGraph.h"



int main() {
    OrientedGraph<string> graph;
    graph.Add_Vertex("A");
    graph.Add_Vertex("B");
    graph.Add_Vertex("C");

    graph.Add_Edge("A", "B");
    graph.Add_Edge("A", "B");
    graph.Add_Edge("A", "A");
    graph.Add_Edge("B", "A");
    graph.Add_Edge("B", "C");
    VertexIterator<string> it1 = graph.vertices_begin();
    VertexIterator<string> it2 = graph.vertices_begin();
    EdgeIterator<string> it_edge = graph.edges_begin();

    if (it2 == it1) {
        cout << "Rabotaet ==\n";
    }

    ++it2; 
    ++it2;
    if (it2 != it1) {
        cout << "Rabotaet !=\n"; 
    }

    graph.Print_Vertices();
    graph.Print_Edges();
    graph.Print_Incident_Edges("A");
    graph.Print_Adjacent_Vertex("A");
    graph.Delete_Edge("A", "A");
    graph.Print_Edges();
    graph.Delete_Edge(it_edge);
    graph.Print_Edges();
    VertexIterator<string> it = graph.vertices_begin();
    cout << "Current vertex: " << *it << endl; // Выводит "A"

    ++it;
    cout << "Next vertex after increment: " << *it << endl; // Выводит "B"
    --it; 
    cout << "Current vertex after dicriment: " << *it << endl; // Выводит "A"
    ++(++it2);
    cout << *it2 << endl; 

    graph.Delete_Vertex(it);
    graph.Print_Vertices();
    graph.Print_Edges();

    // Используем перегруженный оператор вывода
    cout << graph << endl;
    if (++it1 >= it) {
        cout << "Rabotaet\n";
    }
    return 0;
}