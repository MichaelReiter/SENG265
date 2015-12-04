#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "string_set.h"

using namespace std;

string_set::string_set() {
  //initialize iterator and hash table elements
  iterator_node = NULL;
  iterator_index = 0;
  int i;
  for (i = 0; i < HASH_TABLE_SIZE; i++) {
    hash_table[i] = NULL;
  }
}

void string_set::add(const char *s) {
  //check for duplicate and memory exceptions
  if (this->contains(s)) {
    throw duplicate_exception();
  }
  node *newNode = new node;
  if (newNode == NULL) {
    throw memory_exception();
  }
  newNode->s = new char[strlen(s) + 1];
  if (newNode->s == NULL) {
    throw memory_exception();
  }
  strcpy(newNode->s, s);

  //add the new node to the set
  newNode->next = hash_table[hash_function(s)];
  hash_table[hash_function(s)] = newNode;

  this->reset();
}

void string_set::remove(const char *s) {
  //check for not found exception
  if (!this->contains(s)) {
    throw not_found_exception();
  }

  int h = hash_function(s);
  node* curr = hash_table[h];

  //traverse the list
  node* trail = NULL;
  while (curr != NULL) {
    if (strcmp(s, curr->s) == 0) {
      break;
    } else {
      trail = curr;
      curr = curr->next;
    }
  }

  //the node to remove is at the head of the list
  if (hash_table[h] == curr) {
    hash_table[h] = curr->next;
  } else {
    trail->next = curr->next;
  }
  delete curr;

  this->reset();
}

int string_set::contains(const char *s) {
  int h = hash_function(s);
  node* curr = hash_table[h];

  //iterate through the list to check if it contains s
  while (curr != NULL) {
    if (strcmp(s, curr->s) == 0) {
      return 1;
    }
    curr = curr->next;
  }

  return 0;
}

void string_set::reset() {
  //reset the iterator to the first element in the set
  for (iterator_index = 0; iterator_index < HASH_TABLE_SIZE; iterator_index++) {
    if (hash_table[iterator_index] != NULL) {
      break;
    }
  }
  iterator_node = hash_table[iterator_index];
}

const char *string_set::next() {
  //iterate through each key in the hash table and each node in each list
  char* next = iterator_node->s;
  while (iterator_index < HASH_TABLE_SIZE) {
    if (iterator_node->next == NULL) {
      iterator_index++;
      while (iterator_index < HASH_TABLE_SIZE) {
        if (hash_table[iterator_index] != NULL) {
          iterator_node = hash_table[iterator_index];
          break;
        }
        iterator_index++;
      }
    } else {
      iterator_node = iterator_node->next;
    }
    return next;
  }
  return NULL;
}

string_set::~string_set() {
  //iterate through the hashtable freeing all dynamically allocated memory
  int i;
  node* nextPointer;
  for (i = 0; i < HASH_TABLE_SIZE; i++) {
    node* curr = hash_table[i];
    while (curr != NULL) {
      nextPointer = curr->next;
      delete curr->s;
      delete curr;
      curr = nextPointer;
    }
    hash_table[i] = NULL;
  }
}

int string_set::hash_function(const char *s) {
  int stringLength = strlen(s);
  int sum = 0;
  int i;
  //determine which key in the table a string belongs to by summing characters
  for (i = 0; i < stringLength; i++) {
    sum += s[i];
  }
  int result = sum % HASH_TABLE_SIZE;
  return result;
}
