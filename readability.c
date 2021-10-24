#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
int main(void)
{
    //essential vars
    string text = get_string("Text: ");
    float letters = 0;
    float sentences = 0;
    float words = 0;
    
    //loop through everything and harvest letters and sentence counts
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        //check if letter by checking ascii ranges (capital letter range 65-90; lower, 97-122)
        if ((text[i] >= 65 && text[i] <= 90) || (text[i] >= 97 && text[i] <= 122))
        {
            letters++;
        }
        
        //check if character is a sentence ender to proc sentence ++;
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
        
        //if space is present add word
        if (text[i] == ' ')
        {
            words++;
        }
    }
    //last word is not counted since space is absent at the end, add one extra
    words++;
    
    
    //printf("Letters: %f ; Sentences %f ; Words %f\n", letters, sentences, words);
    //get averages
    //how many times does 100 divide into the word count? What do we need to multiply teh word count and therefore the numerator (letters) to get a denominator of 100
    float lettersPerWordsMultiplier = letters * (100.0 / words);
    float sentencesPerWordsMultiplier = sentences * (100.0 / words);
    //printf("Letters / words avg: %f ; Sentences per words avg: %f\n",lettersPerWordsMultiplier, sentencesPerWordsMultiplier);
    
    
    
    //get level
    float grade =  0.0588 * lettersPerWordsMultiplier - 0.296 * sentencesPerWordsMultiplier - 15.8;
    grade = round(grade);
    
    
    //check limits (lower than g 1; about g 16)
    if(grade >= 16)
    {
        printf("Grade 16+");
        return 0;
    }
    else if(grade < 1)
    {
        printf("Before Grade 1");
        return 0;
    }
    
    printf("Grade %i\n", (int) grade);
    
}