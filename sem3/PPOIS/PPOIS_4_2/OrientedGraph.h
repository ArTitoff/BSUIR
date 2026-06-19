#pragma once
#include "VertexIterator.h"
#include "EdgeIterator.h"
#include "IncidentEdgeIterator.h"
#include "AdjacentVertexIterator.h"

template<typename T = std::string>
class OrientedGraph {
protected:
    vector<T> vertex;
    vector<pair<T, T>> edges;
    vector<vector<bool>> adjacency_matrix;

public:
    OrientedGraph() {}
    ~OrientedGraph() {}

    bool empty() const { return vertex.empty(); }

    void clear() {
        vertex.clear();
        edges.clear();
        adjacency_matrix.clear();
    }

    int Get_Vertex_Index(const T& value) {
        for (size_t i = 0; i < vertex.size(); i++) {
            if (value == vertex[i])
                return i;
        }
        return -1;
    }

    bool Edge_Valid(const int& index1, const int& index2) {
        if (index1 == -1 || index2 == -1) {
            cout << "One or both vertices not found" << endl;
            return false;
        }
        return true;
    }

    bool Vertex_Exist(const T& value) {
        return Get_Vertex_Index(value) != -1;
    }

    void Edge_Exist(const T& value1, const T& value2) {
        int index1 = Get_Vertex_Index(value1);
        int index2 = Get_Vertex_Index(value2);

        if (!Edge_Valid(index1, index2))
            return;

        cout << (adjacency_matrix[index1][index2] ? "Edge already exists" : "Edge does not exist") << endl;
    }

    void Add_Vertex(const T& value) {
        if (Vertex_Exist(value))
            return;
        vertex.emplace_back(value);
        adjacency_matrix.push_back(vector<bool>(vertex.size(), false));
        for (size_t i = 0; i < adjacency_matrix.size() - 1; i++)
            adjacency_matrix[i].push_back(false);
    }

    void Delete_Vertex(const T& value) {
        int index = Get_Vertex_Index(value);
        if (index == -1) {
            cout << "Vertex not found." << endl;
            return;
        }

        T vertex_to_remove = vertex[index];

        for (size_t i = 0; i < adjacency_matrix[index].size(); i++) {
            if (adjacency_matrix[index][i]) {
                Delete_Edge(vertex_to_remove, vertex[i]);
            }
        }

        for (size_t i = 0; i < adjacency_matrix.size(); i++) {
            if (adjacency_matrix[i][index]) {
                Delete_Edge(vertex[i], vertex_to_remove);
            }
        }

        adjacency_matrix.erase(adjacency_matrix.begin() + index);

        for (size_t i = 0; i < adjacency_matrix.size(); i++) {
            adjacency_matrix[i].erase(adjacency_matrix[i].begin() + index);
        }

        vertex.erase(vertex.begin() + index);
        cout << "Vertex " << vertex_to_remove << " deleted." << endl;
    }

    void Delete_Vertex(VertexIterator<T>& it) {
        size_t index = it.Get_Index();

        if (index >= vertex.size()) {
            cout << "Iterator is out of range." << endl;
            return;
        }

        T vertex_to_remove = vertex[index];

        for (size_t i = 0; i < adjacency_matrix[index].size(); i++) {
            if (adjacency_matrix[index][i]) {
                Delete_Edge(vertex_to_remove, vertex[i]);
            }
        }

        for (size_t i = 0; i < adjacency_matrix.size(); i++) {
            if (adjacency_matrix[i][index]) {
                Delete_Edge(vertex[i], vertex_to_remove);
            }
        }

        adjacency_matrix.erase(adjacency_matrix.begin() + index);

        for (size_t i = 0; i < adjacency_matrix.size(); i++) {
            adjacency_matrix[i].erase(adjacency_matrix[i].begin() + index);
        }


        vertex.erase(vertex.begin() + index);
        cout << "Vertex " << vertex_to_remove << " deleted." << endl;
    }

    void Add_Edge(const T& value1, const T& value2) {
        int index1 = Get_Vertex_Index(value1);
        int index2 = Get_Vertex_Index(value2);

        if (!Edge_Valid(index1, index2))
            return;

        if (!adjacency_matrix[index1][index2]) {
            edges.emplace_back(value1, value2);
            adjacency_matrix[index1][index2] = true;
            cout << "Edge added" << endl;
        }
        else {
            cout << "Edge already exists" << endl;
        }
    }

    void Delete_Edge(EdgeIterator<T>& it) {
        size_t index = it.Get_Index();

        if (index >= edges.size()) {
            cout << "Iterator is out of range." << endl;
            return;
        }

        const auto& edge_to_remove = edges[index];
        int index1 = Get_Vertex_Index(edge_to_remove.first);
        int index2 = Get_Vertex_Index(edge_to_remove.second);

        if (!Edge_Valid(index1, index2)) {
            cout << "Edge doesn't exist" << endl;
            return;
        }

        edges.erase(edges.begin() + index);
        adjacency_matrix[index1][index2] = false;

        cout << "Edge (" << vertex[index1] << ", " << vertex[index2] << ") deleted." << endl;
    }
    void Delete_Edge(const T& value1, const T& value2) {
        int index1 = Get_Vertex_Index(value1);
        int index2 = Get_Vertex_Index(value2);

        if (!Edge_Valid(index1, index2))
            return;
        if (adjacency_matrix[index1][index2]) {
            edges.erase(remove_if(edges.begin(), edges.end(),
                [&value1, &value2](const pair<T, T>& edge) {
                    return edge.first == value1 && edge.second == value2;
                }),
                edges.end());
            adjacency_matrix[index1][index2] = false;
            cout << "Edge (" << value1 << ", " << value2 << ") deleted" << endl;
        }
        else {
            cout << "Edge doesn't exist" << endl;
        }
    }

    int Get_Vertex_Amount() {
        return vertex.size();
    }

    int Get_Edges_Amount() {
        int amount = 0;
        for (size_t i = 0; i < adjacency_matrix.size(); i++) {
            for (size_t j = 0; j < adjacency_matrix[i].size(); j++) {
                if (adjacency_matrix[i][j])
                    amount++;
            }
        }
        return amount;
    }

    int Vertex_Degree(const T& value) {
        int index = Get_Vertex_Index(value);
        if (!Vertex_Exist(value))
            return 0;
        int amount = 0;
        for (size_t j = 0; j < adjacency_matrix[index].size(); j++) {
            if (adjacency_matrix[index][j])
                amount++;
        }
        return amount;
    }

    int Vertex_Degree(const T& value1, const T& value2) {
        int index1 = Get_Vertex_Index(value1);
        int index2 = Get_Vertex_Index(value2);

        if (!Edge_Valid(index1, index2))
            return 0;

        return (index1 == index2) ? 1 : 2;
    }

    VertexIterator<T> vertices_begin() const { return VertexIterator<T>(vertex, 0); }
    VertexIterator<T> vertices_end() const { return VertexIterator<T>(vertex, vertex.size()); }

    EdgeIterator<T> edges_begin() const { return EdgeIterator<T>(edges, 0); }
    EdgeIterator<T> edges_end() const { return EdgeIterator<T>(edges, edges.size()); }


    void Print_Vertices() {
        cout << "Vertices: ";
        for (auto it = vertices_begin(); it != vertices_end(); ++it) {
            cout << *it << "  ";
        }
        cout << endl << endl;
    }

    void Print_Edges() {
        cout << "Edges: ";
        for (auto it = edges_begin(); it != edges_end(); ++it) {
            cout << "(" << it->first << ", " << it->second << ") ";
        }
        cout << endl << endl;
    }

    IncidentEdgeIterator<T> incident_edges_begin(const T& vertex) {
        return IncidentEdgeIterator<T>(edges, vertex, 0);
    }

    IncidentEdgeIterator<T> incident_edges_end(const T& vertex) {
        return IncidentEdgeIterator<T>(edges, vertex, -1);
    }

    void Print_Incident_Edges(const T& vertex) {
        IncidentEdgeIterator<T> it = incident_edges_begin(vertex);
        IncidentEdgeIterator<T> end_it = incident_edges_end(vertex);
        cout << "Incident Edges: ";

        while (it != end_it) { 
            const auto& edge = *it; 
            cout << "(" << edge.first << ", " << edge.second << ") "; 
            ++it; 
        }
        cout << endl << endl;
    }

    AdjacentVertexIterator<T>  adjacent_edges_begin(const vector<T>& vertices, const vector<vector<bool>>& adjacency_matrix, const T& vertex) {
        return AdjacentVertexIterator<T>(vertices, adjacency_matrix, vertex, 0);
    }

    AdjacentVertexIterator<T>  adjacent_edges_end(const vector<T>& vertices, const vector<vector<bool>>& adjacency_matrix, const T& vertex) {
        return AdjacentVertexIterator<T>(vertices, adjacency_matrix, vertex, -1);
    }

    void Print_Adjacent_Vertex(const T& vertex) {
        AdjacentVertexIterator<T> it = adjacent_edges_begin(this->vertex, this->adjacency_matrix, vertex);
        AdjacentVertexIterator<T> end_it = adjacent_edges_end(this->vertex, this->adjacency_matrix, vertex);
        cout << "Adjacent Vertex: ";
        while (it != end_it) { // Проверка на конец итерации через is_end()
            cout << *it << "  ";
            ++it;
        }
        cout << endl << endl;
    }

    friend ostream& operator<<(ostream& os, const OrientedGraph<T>& graph) {
        os << "Vertices: ";
        std::for_each(graph.vertices_begin(), graph.vertices_end(), [&os](const T& vertex) {
            os << vertex << " ";
            });

        os << "\nEdges: ";
        std::for_each(graph.edges_begin(), graph.edges_end(), [&os](const pair<T, T>& edge) {
            os << "(" << edge.first << ", " << edge.second << ") ";
            });

        return os;
    }
};