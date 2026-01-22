#pragma once
#include <iostream>
#include <vector>
#include <list>
#include <utility>
#include <stdexcept>
#include <algorithm>

using namespace std;

template<typename T>
class EdgeIterator {
protected:
    const vector<pair<T, T>>& edges;
    size_t index;

public:
    EdgeIterator(const vector<pair<T, T>>& edges, size_t index) : edges(edges), index(index) {}

    const pair<T, T>& operator*() const {
        if (index < edges.size()) {
            return edges[index];
        }
        cout << "You call a lot of ++, so we've return only last pair ";
        return edges[edges.size() - 1];
    }

    const pair<T, T>* operator->() const {
        return &edges[index]; // Возвращаем указатель на текущую пару
    }

    EdgeIterator& operator++() {
        if (index < edges.size()) {
            index++;
        }
        return *this;
    }

    EdgeIterator& operator--() {
        if (index > 0) {
            index--;
        }
        return *this;
    }

    size_t Get_Index() const {
        return index;
    }

    bool operator!=(const EdgeIterator& other) const {
        return index != other.index;
    }

    bool operator==(const EdgeIterator& other) const {
        return index == other.index;
    }
};