#include <cs50.h>
#include <stdio.h>
#include<string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
//okay, names are totally meant to be stored in alternative data as indexes; cool
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }

    //fill array
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}






// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    bool candidateReal = false;

    //check candidate validity
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            //add candidate to ranks as name index
            ranks[rank] = i;
            candidateReal = true;
        }
    }

    if (candidateReal == false)
    {
        return false;
    }

    return true;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        //array is sorted so increase starting index procedurally, as people wont prefer a deeper value than one closer to index 0
        for(int j = i + 1; j < candidate_count; j++)
        {
            //preferences for candidate at string index (ranks[i]; an index pointing to a candidate name in the array) vs candidate at string index (ranks[j]; an index pointing to a candidate name in the array; loops for all values past I)
            preferences[ranks[i]][ranks[j]]++;
            //printf(" %i people prefer %i candidate over %i candidate\n",  preferences[ranks[i]][ranks[j]], ranks[i], ranks[j]);
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{

    //for every candidate
    for (int  i = 0; i < candidate_count; i++)
    {
        //check every matchup other than self
        //j = i +1 in order for current cadidate to skip self, and because as the candidate index increases, candidates prior will already have had pairs recorded between them.
        for (int j = i + 1; j < candidate_count; j++)
        {

            //compare preferences[i][j] and [j][i] to each other and determine the winner (each of these values stores how many people prefer the candidate in the first index indicator to that of the second)
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;

                // printf("For %i and %i...%i is the winner dood!!! the marign was %i - %i\n", i, j, i, preferences[j][i], preferences[i][j]);
            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count++;

               // printf("For %i and %i...%i is the winner dood!!! the marign was %i - %i\n", i, j, j, preferences[j][i], preferences[i][j]);
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    //printf("\n");
    //for every pair
    for (int i = 0; i < pair_count; i++)
    {
        pair greatestPair = pairs[i];
        //varaible to keep track of which index the current greatest pair is at
        int greatestIndex = i;

        // i + 1 = starting index; since last num will be in order
        for (int j = i + 1; j < pair_count; j++)
        {
            //get strengths (note: greatStrength will changes as the greatestPair var does too)
            int greatStrength = preferences[greatestPair.winner][greatestPair.loser] - preferences[greatestPair.loser][greatestPair.winner];
            int analyzedStrength = preferences[pairs[j].winner][pairs[j].loser] - preferences[pairs[j].loser][pairs[j].winner];


            if (greatStrength > analyzedStrength)
            {
                //do nothing
            }
            else if (greatStrength < analyzedStrength)
            {
                greatestPair = pairs[j];
                greatestIndex = j;
            }
        }

        //swap our values

        //move the thing in pairs[i] away
        pairs[greatestIndex] = pairs[i];
        //put winner in current spot up for grabs
        pairs[i] = greatestPair;
    }

    //debug
    /*
    for (int i = 0; i < pair_count; i++)
    {
        pair currentPair = pairs[i];
        printf("This pair of %s (winner) and %s (LOOZER XD GANG GANG); has a strength of %i  fortnite\n", candidates[currentPair.winner], candidates[currentPair.loser], preferences[currentPair.winner][currentPair.loser] - preferences[currentPair.loser][currentPair.winner]);
    }
    */

    return;
}


bool HasCycle (int ThisWinner, int loser)
{

    //if an element above in the locked graph is named the loser, a cycle is made; loser is immutable
    if (ThisWinner == loser)
    {
        return true;
    }


    bool winnerConnected = false;
    //check if current winner is connected to a candidate in the diagram, then do the same for it
    for (int i = 0; i < candidate_count; i++)
    {
       if (locked[i][ThisWinner] == true)
       {
           //check if winner has cycle
          if(HasCycle(i, loser))
          {
              return true;
          }
           winnerConnected = true;
       }
    }

   
    return false;
}



// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
       if (!HasCycle(pairs[i].winner, pairs[i].loser))
       {
           locked[pairs[i].winner][pairs[i].loser] = true;
       }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    //search the 2D array on a per column basis
    for (int i = 0; i < candidate_count; i++)
    {
        bool columnFalse = true;
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[i][j] == true)
            {
                columnFalse = false;
            }
        }

        if (columnFalse == true){
            printf("%s", candidates[i]);
        }
    }
    return;
}

