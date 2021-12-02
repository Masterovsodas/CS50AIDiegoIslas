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
        printf("Incorrect usagee: please specify only one forensic image in the arguments");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");

    if (input == NULL)
    {
        printf("Could not open file");
        return 1;
    }

    //workflow
    bool endReached = false;
    int fileCount = 0;

    while (endReached == false)
    {
        printf("porn");
        //make proper name
        char *fileName = "";
        char *finalName = "0";
        sprintf(fileName, "%d", fileCount);

        while (sizeof(fileName) != 2)
        {
            strcat(finalName, fileName);
            //since final name now consistently has the full string, make filename the zero
            fileName = "0";
        }
        printf("%s", finalName);
         printf("poop");
        //fopen
        FILE  *outputJpg = fopen(finalName, "w");


        //look for header, after header found, use fseek to move back in the file
        while (1)
        {
            //read header amount of bytes
            BYTE header[4];
            fread(header, sizeof(BYTE), 4, input);
            fwrite(header, sizeof(BYTE), 4, outputJpg);
            
            //check if jpeg
            if (header[0] == 0xff && header[1] == 0xd8 && header[2] == 0xff && (header[4]  <= 0xef && header[4] >= 0xe0))
            {
                //read blocks until another jpeg signature is found, then fseek back 3 bytes and reset the function
                
                //break out of loop when next sig found
                while(1)
                {
                    //make buffer
                    BYTE block[512];
                    fread(block, sizeof(BYTE), 512, input);
                    //write to file
                    fwrite(block, sizeof(BYTE), 512, outputJpg);
                    
                    //check for new header, else recycle, always fseek....
                    BYTE newHeader[4];
                    fread(header, sizeof(BYTE), 4, input);
                    
                    //check if jpeg
                    if (header[0] == 0xff && header[1] == 0xd8 && header[2] == 0xff && (header[4]  <= 0xef && header[4] >= 0xe0))
                    {
                        //makes file pointer go back 3 bytes in the file
                        fseek(input, -4, SEEK_CUR);
                        break;
                    }
                }
            }
            else
            {
                //look for header again
                continue;
            }
            
            
            //if we get here we went thouugh the while loop and thus are done
            break;
        }
        fileCount++;
    }
}