#pragma once
#include <iostream>
#include <vector>
#include <list>
#include <utility>
#include <stdexcept>
#include <algorithm>

using namespace std;

template<typename T>
class AdjacentVertexIterator {
protected:
    vector<T> vertices;
    size_t index;

    bool Vertex_Already_Exist(const T& vertex) {
        for (size_t i = 0; i < vertices.size(); i++) {
            if (vertices[i] == vertex)
                return true;
        }
        return false;
    }
public:
    AdjacentVertexIterator(const vector<T>& vertices, const vector<vector<bool>>& adjacency_matrix, const T& vertex, size_t index)
         {
        size_t vertex_index;
        for (size_t i = 0; i < vertices.size(); i++) {
            if (vertices[i] == vertex) {
                vertex_index = i;
                break;
            }
        }
        for (size_t j = 0; j < adjacency_matrix[vertex_index].size(); j++) {
            if (adjacency_matrix[vertex_index][j] && !Vertex_Already_Exist(vertices[j]))
                this->vertices.emplace_back(vertices[j]);
            if (adjacency_matrix[j][vertex_index] && !Vertex_Already_Exist(vertices[j]))
                this->vertices.emplace_back(vertices[j]);
        }
        
        if (index == -1) {
            this->index = this->vertices.size();
        }
        else this->index = index;
    }


    AdjacentVertexIterator& operator++() {
        if (index < vertices.size()) {
            index++;
        }
        return *this;
    }

    const T& operator*() const {
        if (index < vertices.size()) {
            return vertices[index];
        }
        cout << "You call a lot of ++, so we've return only last elem ";
        return vertices[vertices.size() - 1];
    }


    AdjacentVertexIterator& operator--() {
        if (index > 0) {
            index--;
        }
        return *this;
    }

    bool operator!=(const AdjacentVertexIterator& other) const { return index != other.index; }

};