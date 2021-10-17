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
    while (height <= 0 || height > 8);

    ///build pyramids
    for (int i = 1; i <= height; i++)
    {
        int spaces = height - i;

        //get necessary characters based on data we have; until i > spaces, print only spaces, after get #; this will give the right side of the pyramid always.
        for (int j = 0; j < height; j++)
        {
            //when less add a space
            if (j < spaces)
            {
                printf(" ");
            }
            //when more add tags
            else
            {
                printf("#");
            }
        }
        
        //print gap
        printf("  ");
        //reverse string and make side2 euqal that
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}