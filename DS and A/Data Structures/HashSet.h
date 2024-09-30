#pragma once

using namespace std;

template<class T>
class HashSet {
public:
    HashSet() : length(0), capacity(10){
        items = new T[capacity];
    }

    ~HashSet() {
        delete[] items;
    }

    bool insert(T item) {
        // implement insert here
        // return true if item was inserted, false if item was already in the set
        int index = hashing(item);
        if (contains(item)) {
            return false;
        }
        if (length == capacity) {
            resize();
        }
        items[index] = item;
        length++;
        return true;
    }

    bool remove(T item) {
        // implement remove here
        // return true if item was removed, false if item wasn't in the set
        int index = hashing(item);
        if (!contains(item)){
            return false;
        }
        items[index] = items[--length];
        return true;
    }

    bool contains(T item) const {
        // implement contains here
        // return true if item is in the set, false otherwise
        int index = hashing(item);
        return items[index] == item;
    }

    void clear() {
        // implement clear here
        // remove all elements from the set
        length = 0;
    }

    int size() const {
        // implement size here
        // return the number of elements in the set
        return length;
    }

    private:
        int length;
        int capacity;
        T* items;

    int hashing(T item) const{
        return  hash<T>()(item) % capacity;
    }

    void resize(){
        capacity *= 2;
        T* newItems = new T[capacity];
        for (int i = 0; i < length; ++i){
            int index = hashing(items[i]);
            newItems[index] = items[i];
        }
        delete[] items;
        items = newItems;
    }
};
