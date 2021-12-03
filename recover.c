#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>

typedef uint8_t BYTE;

#define BLOCK 512;

FILE *makeName(int fileCount);

int main(int argc, char *argv[])
{
    //check input validdity and open files
    if (argc != 2)
    {
        printf("Incorrect usage: please specify only one forensic image in the arguments\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");

    if (input == NULL)
    {
        printf("Could not open file\n");
        return 1;
    }

    //workflow
    bool endReached = false;
    int fileCount = 0;
    //bool to indicate when to start constantly writting
    bool writeStart = false;

    //FILES ARENT ENDING FOR SOME REASON, FIND OUT WHY THE NEXT JPEG HEADER IS NOT FOUND; ANYWAYS I AHVE TO POO....

    //read in blocks of 512, idk why we cant look for a header and then read in blocks; Brian said to do this, i have a negatively progressing IQ and thus am incapable of understanding why the ass this works
    FILE *outputJpg;

    while (1)
    {
        //read the bytes
        BYTE block[512];
        if (fread(block, sizeof(BYTE), 512, input) == 512)
        {
            //check for jpg
            if (block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] <= 0xef && block[3] >= 0xe0))
            {
                //when first jpeg, continue loop, when beyond that close our file
                if (writeStart == false)
                {
                    writeStart = true;
                    outputJpg = makeName(fileCount);
                }
                else
                {
                    fclose(outputJpg);
                    fileCount++;
                    //make file and write first block to it
                    outputJpg = makeName(fileCount);
                }
            }

            //if bytes are writeable, go write them; the wriatble condition is written to avoid garbage pre first header
            if (writeStart == true)
            {
                fwrite(block, sizeof(BYTE), 512, outputJpg);
            }
        }
        else
        {
            break;
        }
    }

    return 0;
}


FILE *makeName(int fileCount)
{
    //make proper name
    char NumPart[8];
    char finalName[8];
    sprintf(NumPart, "%i", fileCount);

    //add zeroes based on count
    if (fileCount < 10)
    {
        //add two zeroes
        snprintf(finalName, sizeof(finalName), "00%s", NumPart);
    }
    else if (fileCount < 100)
    {
        //add a zero
        snprintf(finalName, sizeof(finalName), "0%s", NumPart);
    }

    //fopen
    FILE  *outputJpg = fopen(strcat(finalName, ".jpg"), "w");
    return outputJpg;
}