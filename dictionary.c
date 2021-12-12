// Implements a dictionary's functionality
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <strings.h>
#include <stdlib.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

//Number of words placed into the hash table
int wordCount = 0;

// Number of buckets in hash table, has one for every ordered combination of two letter sin the alphabet (ie: 0 = aa, 1= ab...)....27 is added in second to get words that may have a second letter apostrophe
const unsigned int N = 26*27;

// Hash table (array (square brackets) of linked lists)
node *table[N];


// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    //get nav index
    int navIndex = hash(word);
    //node defined as the head of the linked list
    node *marker = table[navIndex];

    while (marker != NULL)
    {
        //check if strcasecmp of both words returns equal
        if (strcasecmp(marker->word, word) == 0)
        {
            return true;
        }
        //if not move the marker
        marker = marker->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    //get two strings which will be used to find the indexes of the different letters, these idnexes will be multiplied and added accordingly to return the correct hash index
    char *alphabet = "abcdefghijklmnopqrstuvwxyz";
    char *apostAlph = "'abcdefghijklmnopqrstuvwxyz";

    int hashValue = 0;

    //do math
    //strchr returns a pointer, so we subtract it from the pointer to the first letter to get our index / difference.
    int firstLetterHop = (strchr(alphabet, tolower(word[0])) - alphabet) * 27;

    //check if letter search goes out of bounds; do it as such because strchr returns the amount of values surfed before reaching \0 or the searched value. so if you subtract the out of bounds adress from the initial one, you get an out of bounds second value.
    if (strchr(apostAlph, tolower(word[1])) - apostAlph > strlen(apostAlph) - 1)
    {
        return firstLetterHop;
    }
    else
    {
        //get second letter index and send it off
        int secondLetterHop = (strchr(apostAlph, tolower(word[1])) - apostAlph);
        return firstLetterHop + secondLetterHop;
    }
}



// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    //open dictionary
    FILE *words = fopen(dictionary, "r");
    if(words == NULL)
    {
        return false;
    }

    char thisWord[LENGTH + 1];
    //read dictionary words
    while (fscanf(words, "%s", thisWord) != EOF)
    {
       //hash word
       node *thisNode = malloc(sizeof(node));
       if (thisNode == NULL)
       {
           return false;
       }
       //put word into node
       strcpy(thisNode->word, thisWord);

       //hash word and find out which bucket it falls into using hash function, then load it into table here
       int wordIndex = hash(thisWord);

       //printf("%s  %i\n", thisWord, wordIndex);

       //add to linked list
       //check if first value in list
       if (table[wordIndex] == NULL)
       {
           //make initial pointer equal to thisNode pointer
          table[wordIndex] = thisNode;
       }
       else
       {
          //first make this node point to the start of the list
          thisNode->next = table[wordIndex]->next;
          //then make og pointer point to new node
          table[wordIndex]->next = thisNode;
       }

       wordCount++;
    }
    fclose(words);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return wordCount;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    //loop through entire table
    for (int i = 0; i < N; i++)
    {
        node *cursorList = table[i];

        while (0 == 0)
        {
            node *temp = cursorList->next;
            free(cursorList);
            cursorList = temp;
            
            if (cursorList == NULL)
            {
                break;
            }
        }
    }
    return true;
}
