#pragma once
#include <iostream>
using namespace std;

template<class T>
class AVL {
public:
    struct Node {
        Node* left;
        Node* right;
        T value;
        int height;

        Node(T v) : left(nullptr), right(nullptr), value(v), height(1) {}
    };

    AVL() {
        // implement the contructor here
        root = nullptr;
    }

    ~AVL() {
        // implement the destructor here
        clear();
    }

    const Node* getRootNode() const {
        // implement getRootNode here
        // return a pointer to the tree's root node
        return root;
    }

    bool insert_help(Node*& next, T item){
        if (next == nullptr){
            next = new Node(item);
            update_height(next);
            rebalance(next);
            return true;
        }
        if (item < next->value)
            if (insert_help(next->left, item)){
                update_height(next);
                rebalance(next);
                return true;
            }
        if (item > next->value){
            if (insert_help(next->right, item)){
                update_height(next);
                rebalance(next);
                return true;
            }
        }
        return false;
    }

    bool insert(T item) {
        // implement insert here
        // return true if item was inserted, false if item was already in the tree
        if (insert_help(root, item)){
            length++;
            return true;
        }
        return false;
    }

    bool remove_help(Node*& next, T item) {
            if (next == nullptr) {
                return false;
            }

            if (item < next->value) {
                if (remove_help(next->left, item)){
                    update_height(next);
                    rebalance(next);
                    return true;
                };
            } else if (item > next->value) {
                if (remove_help(next->right, item)){
                    update_height(next);
                    rebalance(next);
                    return true;
                }
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
                    if (remove_help(next->left, successor->value)){
                        update_height(next);
                        rebalance(next);
                        return true;
                    }
                }
            }
        }

    bool remove(T item) {
        // implement remove here
        // return true if item was removed, false if item wasn't in the tree
        if (remove_help(root, item)){
            return true;
        };
        return false;
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
        // implement clear here
        // remove all nodes from the tree
        clear_help(root);
        root = nullptr;
        length = 0;
    }

    int size() const {
        // implement size here
        // return the number of nodes in the tree
        return length;
    }

    private:
    Node* root;
    int length;

    int get_height(Node* node){
        if (node == nullptr){
            return 0;
        }
        else{
            return node->height;
        }
    }

    void update_height(Node* node){
        if (node == nullptr){
            return;
        }
        update_height(node->left);
        update_height(node->right);
        int LH = get_height(node->left);
        int RH = get_height(node->right);
        if  (LH > RH){
            node->height =  LH + 1;
            } else{
                node->height = RH +  1;
        }
    }

    void promote_left(Node*& root) {
        // implement promote_left here
        if (root == nullptr){
            return;
        }
        auto temp = root->left;
        root->left = temp->right;
        temp->right = root;
        root = temp;
        update_height(root->left);
        update_height(temp);
    }

    void promote_right(Node*& root) {
        // implement promote_right here
        if (root == nullptr){
            return;
        }
        auto temp = root->right;
        root->right = temp->left;
        temp->left = root;
        root = temp;
        update_height(root->right);
        update_height(temp);
    }

    void rebalance(Node*& root) {
        // implement rebalance here
        if  (root == nullptr){
            return;
        }
        // find the height difference
        int balance = get_height(root->left) - get_height(root->right);
        if (balance > 1){
            if (get_height(root->left->left) < get_height(root->left->right)){
                promote_right(root->left);
            }
            promote_left(root);
        }
        else if (balance < -1){
            if (get_height(root->right->left) > get_height(root->right->right)){
                promote_left(root->right);
            }
            promote_right(root);
        }
    }
};
