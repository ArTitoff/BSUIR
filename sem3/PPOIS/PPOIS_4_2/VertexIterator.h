#pragma once
#include <iostream>
#include <vector>
#include <utility>

using namespace std;

template<typename T>
class VertexIterator {
protected:
    const vector<T>& vertices;
    size_t index;

public:
    VertexIterator(const vector<T>& vertices, size_t idx) :
        vertices(vertices), index(idx) {}

    VertexIterator& operator++() {
        if (index < vertices.size()) {
            index++;
        }
        return *this;
    }

    const T& operator*() const {
        if (index < vertices.size()) {
            return vertices[index]; // Прямой возврат ссылки
        }
        cout << "You call a lot of ++, so we've return only last elem ";
        return vertices[vertices.size() - 1];
    }


    VertexIterator& operator--() {
        if (index > 0) {
            index--;
        }
        return *this;
    }

    size_t Get_Index() const {
        return index;
    }

    bool operator!=(const VertexIterator& other) const { return index != other.index; }
    bool operator==(const VertexIterator& other) const { return index == other.index; }

    bool operator>(const VertexIterator& other) const {
        return vertices[index] > other.vertices[other.index];

    }

    bool operator<(const VertexIterator& other) const {
        return vertices[index] < other.vertices[other.index];

    }

    bool operator>=(const VertexIterator& other) const {
        return vertices[index] >= other.vertices[other.index]; 

    }

    bool operator<=(const VertexIterator& other) const {
        return vertices[index] <= other.vertices[other.index]; 

    }

};