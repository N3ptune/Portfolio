#pragma once

using namespace std;

template<class T>
class BST {
public:

    struct Node {
        Node* left;
        Node* right;
        Node* parent;
        T value;

        Node(T v) : left(nullptr), right(nullptr), value(v) {}
    };

    BST() {
        // implement the contructor here
        root = nullptr;
    }

    ~BST() {
        // implement the destructor here
        clear();
    }

    const Node* getRootNode() const {
        // implement getRootNode here
        // return a pointer to the tree's root node
        return root;
    }



    bool insert(T item) {
        // implement insert here
        // return true if item was inserted, false if item was already in the tree
        Node* current = root;
        Node* parent = nullptr;
        while (current != nullptr) {
            parent = current;
            if (item < current->value) {
                current = current->left;
            } else if (item > current->value) {
                current = current->right;
            } else {
                return false;
            }
        }
        Node* newNode = new Node(item);
        if (parent == nullptr) {
            root = newNode;
        } else if (parent->value < item) {
            parent->right = newNode;
        } else {
            parent->left = newNode;
        }
        return true;
    }

    bool remove_help(Node*& next, T item) {
        if (next == nullptr) {
            return false;
        }

        if (item < next->value) {
            if (remove_help(next->left, item)){
            };
        } else if (item > next->value) {
            return remove_help(next->right, item);
        } else {
            // leaf node
            if (next->left == nullptr &&  next->right == nullptr) {
                delete next;
                next = nullptr;
                length--;
                return true;
            }
            // one child
            if (next->left == nullptr && next->right != nullptr) {
                Node* temp = next->right;
                delete next;
                next = temp;
                length--;
                return true;
            } else {
                Node* successor = next->left;
                while (successor->right != nullptr) {
                    successor = successor->right;
                }
                next->value = successor->value;
                return remove_help(next->left, successor->value);
            }
        }
    }

    bool remove(T item) {
        return remove_help(root, item);
    }

    bool contains_recur_help(Node* next, T item) const{
        if (next == nullptr){
            return false;
        }
        if (item  < next->value) {
            return contains_recur_help(next->left, item);
        }else if (item > next->value) {
            return contains_recur_help(next->right, item);
        }
        return true;
    }

    bool contains(T item) const {
        // implement contains here
        // return true if item is in the tree, false otherwise
        return contains_recur_help(root, item);
    }

    void clear_help(Node* next){
        if (next == nullptr){
            return;
        }
        clear_help(next->left);
        clear_help(next->right);
        delete next;
    }

    void clear() {
        clear_help(root);
        root = nullptr;


    //pass something in, clear left, clear right, clear myself, return.
    }

    int size() const {

    return length;
}

private:
    Node* root;
    int length;
};
