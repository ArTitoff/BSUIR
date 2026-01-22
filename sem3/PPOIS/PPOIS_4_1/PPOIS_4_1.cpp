#include <iostream>
#include <vector>
#include <iterator>

template<typename T>
void Coctail_Sort(T& container, const size_t& size) {
    bool swapped = true;
    size_t start = 0;
    size_t end = size - 1;

    while (swapped) {
        swapped = false;

        // Проход справа налево
        for (size_t i = end; i > start; --i) {
            if (container[i] < container[i - 1]) {
                std::swap(container[i], container[i - 1]);
                swapped = true;
            }
        }
        ++start;

        if (!swapped) break;

        swapped = false;

        // Проход слева направо
        for (size_t i = start; i <= end; ++i) {
            if (container[i] < container[i - 1]) {
                std::swap(container[i], container[i - 1]);
                swapped = true;
            }
        }
        --end;
    }
}

template<typename T> 
void Comb_Sort(T& arr, const size_t& size) {
    const double shrinkFactor = 1.3; // Фактор сжатия
    size_t n = size;
    size_t gap = n;
    bool swapped = true;

    while (gap > 1 || swapped) {
        gap = static_cast<size_t>(gap / shrinkFactor);
        if (gap < 1) gap = 1;

        swapped = false;

        for (size_t i = 0; i + gap < n; ++i) {
            if (arr[i] > arr[i + gap]) {
                std::swap(arr[i], arr[i + gap]);
                swapped = true;
            }
        }
    }
}



class Test {
	int value;
public:
    Test(int value) : value(value){}

	int Get_Value() const {
		return value;
	}

	bool operator <(Test& param) {
		return value < param.Get_Value() ? true : false;
	}

	friend std::ostream& operator<<(std::ostream& os, const Test& param) {
		os << param.Get_Value();
		return os;               
	}

};

int main() {
	std::vector<int> arr = {3, 7, 8, 4, 1};
    Comb_Sort(arr, arr.size());
	for (int i = 0; i < arr.size(); i++) {
		std::cout << arr[i] << " ";
	}
	
    std::cout << std::endl;

    Test arr1[5] = {Test(5), Test(3), Test(8), Test(1), Test(2)};
    int size = sizeof(arr1) / sizeof(arr1[0]);
    Coctail_Sort(arr1, size);

    std::cout << "Sorted array of MyClass: ";
    for (size_t i = 0; i < size; ++i) {
        std::cout << arr1[i] << " ";
    }
    std::cout << std::endl;


	return 0;
}