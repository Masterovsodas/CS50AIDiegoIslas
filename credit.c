#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>

int main(void)
{
    //essential vars
    string number = get_string("Number: ");
    long sumDigs = 0;
    long sumMults = 0;
    
    //multiply
    for(int i = 1; i <= strlen(number); i++)
    {
        //check if character is one of every other
        if(i % 2 == 0)
        {
            int thisChar = number[strlen(number) - i] - '0';
            thisChar *= 2;
            
            //convert to a string
            char digis[thisChar];
            sprintf(digis, "%d", thisChar); 

            //add individual digits
            for(int j =0; j < strlen(digis); j++)
            {
                int currentDigi = digis[j] - '0';
                sumMults += currentDigi;
            }
        }
        else
        {
            //convert char to int as such
            sumDigs += number[strlen(number) - i] - '0';
        }
    }
   
    
    //check if number is valid
    if((sumMults + sumDigs) % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }
    
    
    //if valid verify distributor
    switch(number[0])
    {
        //if possibly amex
        case '3':
            if(strlen(number) == 15 && (number[1] == '4' || number[1] == '7'))
            {
                printf("AMEX\n");
                return 0;
            }
        break;
        
        //check VISA
        case '4':
            if((strlen(number) == 13 || strlen(number) == 16))
            {
                printf("VISA\n");
                return 0;
            }
        break;
        
        //check mastercard
        case '5':
          if(strlen(number) == 16 && number[1] <= '5')
            {
                printf("MASTERCARD\n");
                return 0;
            }
        break;
    }
    printf("INVALID\n");
}