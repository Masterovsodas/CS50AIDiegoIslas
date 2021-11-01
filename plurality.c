#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Define candidate count (-1 because ./prgmname is counted as an arg)
    candidate_count = argc - 1;
    
    //break if too many candidates
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    
     // Populate array of candidates
    for (int i = 0; i < candidate_count; i++)
    {
        //i + 1; because once again the ./ command is processed as an arg
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    //for number of candids
    for(int i = 0, n = candidate_count; i < n; i++)
    {
        //checks where both strngs are placed on alphabet, if 0 they are in the same alphabetical position and so equal
        if(strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes++;
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    int currentHighest = -1;
    string names[MAX];
    int namesInArray = 0;
    int placeIndex = 0;
    
    for(int i = 0, n = candidate_count; i < n; i++)
    {
        if(candidates[i].votes > currentHighest)
        {
            currentHighest = candidates[i].votes;
            memset(names, 0, sizeof names);
            names[0] = candidates[i].name;
            placeIndex = 1;
            namesInArray = 1;
        }
        else if(candidates[i].votes == currentHighest)
        {
            names[placeIndex] = candidates[i].name;
            placeIndex++;
            namesInArray++;
        }
    }
    
    //to prevent segfaults when empty strings are inserted, only runf or the amount of names in teh array
    for(int i = 0; i < namesInArray; i++)
    {
        printf("%s\n", names[i]);
        
    }
    return;
}

