#pragma once
#include <iostream>
#include <vector>
#include <list>
#include <utility>
#include <stdexcept>
#include <algorithm>

using namespace std;


template<typename T>
class IncidentEdgeIterator {
protected:
    vector<pair<T, T>> edges;
    size_t index;

public:
    IncidentEdgeIterator(const vector<pair<T, T>>& all_edges, T vertex, size_t index)
        {
        for (const auto& edge : all_edges) {
            if (edge.first == vertex || edge.second == vertex) {
                edges.emplace_back(edge);
            }
        }

        if (index == -1) {
            this->index = edges.size();
        }
        else this->index = index;
    }

    const pair<T, T>& operator*() const {
        if (index < edges.size()) {
            return edges[index];
        }
        throw out_of_range("Dereferencing out of range");
    }

    const pair<T, T>* operator->() const {
        return &edges[index];
    }

    IncidentEdgeIterator& operator++() {
        if (index < edges.size()) {
            index++;
        }
        return *this;
    }

    IncidentEdgeIterator& operator--() {
        if (index > 0) {
            index--;
        }
        return *this;
    }

    bool operator!=(const IncidentEdgeIterator& other) const {
        return index != other.index;
    }
};