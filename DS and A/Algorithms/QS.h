#pragma once

#include <vector>
#include <string>
using namespace std;

template<class T>
int medianOfThree(std::vector<T>& array, int left, int right) {
    // implement medianOfThree here
    int middle = ((left + right)/2);
    return middle;
}

template<class T>
int partition(std::vector<T>& array, int left, int right) {
    // implement partition here
    int middle = medianOfThree(array, left, right);
    swap(array[middle], array[left]);
    int up = left + 1;
    int down = right;
    for (int i = 0; i < array.size(); i++){
        while (array[up] <= array[left] && up  < right){
            up++;
        }
        while (array[down]  >= array[left]  &&  down > left ){
            down--;
        }
    }
    if (up < down){
        swap(array[up] , array[down]);
    }
    swap(array[left] , array[down]);
    return down;
}
template<class T>
void sort_helper(vector<T>& array, int left, int right){
    if (left < right){
        int pivot_point = partition(array, left, right);
        sort_helper(array, left, pivot_point -1);
        sort_helper(array, pivot_point + 1, right);
    }
}

template<class T>
void sort(std::vector<T>& array) {
    // implement sort here
    // hint: you'll probably want to make a recursive sort_helper function
    sort_helper(array, 0, array.size()-1);
}
