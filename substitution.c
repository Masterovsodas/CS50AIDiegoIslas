#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

int main(int argc, string arga[])
{
    
    //check input validity
    if(argc != 2)
    {
        printf("Too many or too little command-line arguments!\n");
        return 1;
    }
    
    if(strlen(arga[1]) != 26)
    {
        printf("Key is invalid: too long or short; must be 26 unique letters\n");
        return 1;
    }
    
    //check if all of key is unique
    for (int i = 0, n = strlen(arga[1]); i < n; i++)
    {
        //get current character
        char thisChar = tolower(arga[1][i]);
        
        //check if character is unique
        for (int j = 0, o = strlen(arga[1]); j < o; j++)
        {
            //if self continue, else check if equal, if equal the key sucks
            if(j == i)
            {
                continue;
            }
            else if(thisChar == tolower(arga[1][j]))
            {
                printf("Use unique characters!\n");
                return 1;
            }
            
        }
        
        //check if is alphabetical letter
        if (thisChar < 65 || thisChar > 122 || (thisChar > 90 && thisChar < 97))
        {
            printf("Use all alphabeticals please!!\n");
            return 1;
        }
    }
    ////////////////////////////////////PROGRAM START//////////////////////////////////////
    
    //essential vars
    string alphabet = "abcdefghijklmnopqrstuvwxyz";
    string plainText = get_string("plaintext: ");
    string cipherText = "";
    
    
    //start output line
    printf("ciphertext: ");
    for (int i = 0, n = strlen(plainText); i < n; i++)
    {
        char thisChar = plainText[i];
        
        //if is lower add corresponding lower char, else add upper
        if (islower(thisChar))
        {
            //quick method to find last index of a char in a string, idk why subtracting the alphabet string form the pointer returns the index but it do
            char* alphIndex = strchr(alphabet, thisChar);
            
            //add char
            printf("%c", tolower(arga[1][alphIndex - alphabet]));
        }
        else if(isupper(thisChar))
        {
          //quick method to find last index of a char in a string, idk why subtracting the alphabet string form the pointer returns the index but it do
            char* alphIndex = strchr(alphabet, thisChar);
            
            //add char
            printf("%c", toupper(arga[1][alphIndex - alphabet]));
        }
        else
        {
            //if other char just print it
            printf("%c", thisChar);
        }
        
    }
    //move tilda
    printf("\n");
}