#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
 #include <string.h>

typedef uint8_t BYTE;

#define BLOCK 512;

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


    //FILES ARENT ENDING FOR SOME REASON, FIND OUT WHY THE NEXT JPEG HEADER IS NOT FOUND; ANYWAYS I AHVE TO POO....
    while (endReached == false)
    {
        //make proper name
        char NumPart[4];
        char finalName[4];
        sprintf(NumPart, "%i", fileCount);

        //add zeroes based on count
        if (fileCount < 10)
        {
            //add two zeroes
            snprintf(finalName, sizeof(finalName), "00%s", NumPart);
        }
        else if(fileCount < 100)
        {
            //add a zero
            snprintf(finalName, sizeof(finalName), "0%s", NumPart);
        }

        //fopen
        FILE  *outputJpg = fopen(strcat(finalName, ".jpg"), "w");


        //look for header, after header found, use fseek to move back in the file
        while (1)
        {
            //read header amount of bytes
            BYTE header[4];
            fread(header, sizeof(BYTE), 4, input);

            //check if jpeg
            if (header[0] == 0xff && header[1] == 0xd8 && header[2] == 0xff && (header[3] <= 0xef && header[3] >= 0xe0))
            {
                printf("Jpog\n");
                //read blocks until another jpeg signature is found, then fseek back 3 bytes and reset the function
                fwrite(header, sizeof(BYTE), 4, outputJpg);

                //break out of loop when next sig found
                while(1)
                {
                    //make buffer
                    BYTE block[512];

                    //check if read successfully else return
                    if (fread(block, sizeof(BYTE), 512, input) == 512)
                    {
                        //write to file
                        fwrite(block, sizeof(BYTE), 512, outputJpg);

                        //check for new header, else recycle pointer, always fseek....
                        BYTE newHeader[4];
                        fread(newHeader, sizeof(BYTE), 4, input);
                        //makes file pointer go back 3 bytes in the file
                        fseek(input, -4, SEEK_CUR);
                        //printf("%i  %i %i %i\n", newHeader[0], newHeader[1], newHeader[2], newHeader[3]);


                        //check if jpeg
                        if (newHeader[0] == 0xff && newHeader[1] == 0xd8 && newHeader[2] == 0xff && (newHeader[3]  <= 0xef && newHeader[3] >= 0xe0))
                        {
                            fclose(outputJpg);
                            break;
                        }
                    }
                    else
                    {
                        //end of file likely reached, kill prgm
                        printf("end of file\n");
                        return 0;
                    }
                }
            }
            else
            {
                //look for header again
                continue;
            }
            printf("end of this jpeg\n");
            //if we get here we went though the while loop and thus are done
            break;
        }
        fileCount++;
    }
}