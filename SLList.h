#pragma once

using namespace std;

template <class T>
class SLList {
public:
    struct Node {
        Node* next;
        T value;

        Node(T v) : next(nullptr), value(v) {}
    };


Node* head;


    SLList() : head(nullptr){
        //initialize an empty list
    }

    ~SLList() {
        //clears the list
        clear();
    }

    const Node* get_head() const {
        // implement get_head here
        // returns a pointer to the head node
        return head;
    }

    void push_back(T item) {
        // implement push_back here
        // adds a new node with the given item to the end of the list
        if (!head) {
            head = new Node(item);
        } else {
            Node* current = head;
            while (current->next) {
                current = current->next;
            }
            current->next = new Node(item);
        }
    }

    void pop_back() {
        // implement pop_back here
        // removes the last node in the list
        if (!head){
            cout << "Nothing to pop back"  << endl;
            return;
        }
        if (!head->next) {
            delete head;
            head = nullptr;
            return;
        }

        Node *temp = head;
        while(temp->next->next) {
            temp = temp->next;
        }
        delete temp->next;
        temp->next = nullptr;
    }

    const T& front() const {
        // implement front here
        // returns a const reference to the value of the head node
        return head->value;
    }

    int size() const {
        // implement size here
        // returns the size of the list
        int size = 0;
        Node* current = head;
        while(current) {
            size++;
            current = current->next;
        }
        return size;
    }

    void clear() {
        // implement clear here
        // removes all nodes from the list
        Node* current = head;
        while (head) {
            Node* temp =  head;
            head = head->next;
            delete temp;
    }
    }
};