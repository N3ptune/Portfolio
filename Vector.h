#pragma once

#include <iostream>
#include <string>

using namespace std;

template<class T>
class Vector {
    int length;
    int capacity;
    T* data;

    void resize() {
        capacity  *= 2;
        T* newData = new T[capacity];
        // copy(data, data + size, newData)
        for (int i = 0; i < length; i++){
            newData[i] = data[i];
        }
        delete[] data;
        data = newData;
    }

public:
// Constructors

    Vector() : length(0), capacity(0), data(new T[capacity]) {} // Default constructor

    ~Vector()  {
        delete[] data;
    }  		      // Destructor


    void push_back(T item) {
        // implement push_back here
        // Append an item to the end of the vector
    if (length == capacity){
        if (capacity == 0){
            capacity = 1;
        }
        resize();
    }
    data[length++] = item;
    }


    void insert(T item, int position) {
        // implement insert here
        //Insert an item at the given position, shifting all elements  after it one place to the right.
        if (position < 0 || position > length){
            throw out_of_range("Index out of range");
        }
        if (length == capacity){
            resize();
        }
        for (int i = length; i > position; i--){
            data[i] = data[i-1];
        }
        data[position] = item;
        length++;
    }

    void remove(int position) {
        // implement remove here
        // remove element at position, moving elements to left
        if (position < 0 || position > length){
            throw out_of_range("Index out of range");
        }
        for (int i = position; i < length-1; i++){
            data[i] = data[i+1];
        }
        length--;
    }

    T& operator[](int index) {
        // implement operator[] here
        if  (index < 0 || index >= length){
            throw out_of_range("Index out of range");
        }
        return  data[index];
    }

    int size() const {
        // implement size here
        //return size
        // int size = 0;
        // while  (data[size]){
        //     size++;
        // }
        return length;
    }

    void clear() {
        // implement clear here
        //clear the vector
        length = 0;
    }
};
