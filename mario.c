#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main(void)
{
    //essential vars
    int height = 0;
    //verify validity
    do
    {
        height = get_int("Height: ");
    }
    while(height > 0 || height > 8);

    ///build pyramids
    for(int i = 1; i <= height; i++)
    {
        //okay so cs50.h has  built in string which does jack, so we ave to use c strings, very stupid char arrays
        char side1[8];
        char side2[8];
        int spaces = height - i;
        
        //get necessary characters based on data we have; until i > spaces, print only spaces, after get #; this will give the right side of the pyramid always.
        for(int j = 0; j<height; j++){
            //when less add a space
            if(j < spaces)
            {
               side1[j] = ' ';
            }
            //when more add tags
            else
            {
                side1[j] = '#';
            }
        }
        
        //reverse string and make side2 euqal that
       for(int j = 0; j < height; j++)
       {
           if(side1[(height - 1) - j] == ' ')
           {
               continue
           }
           side2[j] = side1[(height - 1) - j];
       }
        
        printf("%s  %s\n", side1, side2);
       
    }
}