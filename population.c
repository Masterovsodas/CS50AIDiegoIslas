#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //essential vars
    long years = 0;
    
    // TODO: Prompt for start size
    long startSize;
    //verify validity
    do
    {
        startSize = get_long("Start size: ");
    }
    while (startSize < 9);
    
    
    // TODO: Prompt for end size
    long endSize = 0;
    //verify validity
    do
    {
        endSize = get_long("End size: ");
    }
    while (endSize < startSize);
    
    // TODO: Calculate number of years until we reach threshold
    while (startSize < endSize)
    {
        startSize += (startSize / 3) - (startSize / 4);
        years++;
    }
    // TODO: Print number of years
    printf("Years: %li\n", years);
}