// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in hash table
// 26 is fine but slow, so we use bigger for better performance
const unsigned int N = 10000;

// Hash table
node *table[N];

// Keep count of words loaded
unsigned int word_count = 0;

// Hashes word to a number (djb2 hash)
unsigned int hash(const char *word)
{
    unsigned long hash_value = 5381;
    int c;

    while ((c = *word++))
    {
        c = tolower(c);
        hash_value = ((hash_value << 5) + hash_value) + c; // hash * 33 + c
    }

    return hash_value % N;
}

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    unsigned int index = hash(word);

    node *cursor = table[index];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];

    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            fclose(file);
            return false;
        }

        strcpy(n->word, word);

        unsigned int index = hash(word);

        n->next = table[index];
        table[index] = n;

        word_count++;
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }

    return true;
}
