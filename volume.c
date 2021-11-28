// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    
    //create header storage
    uint8_t header[HEADER_SIZE];
    fread(header, sizeof(uint8_t), sizeof(header), input);
    fwrite(header, sizeof(uint8_t), sizeof(header), output);
   

    //TODO: Read samples from input file and write updated data to output file
    //creat a 16 bit value that will hold each sample of audio
    int16_t buffer;
    
    //while 2 bytes (one int16_t value) can be read from the source file; put read value at teh adress of the buffer variable's memory
    while (fread(&buffer, sizeof(int16_t), 1, input))
    {
        //multiply sample by factor to modify volume
        buffer *= factor;
        //then write from the adress of the buffer's memory, the next 16 bit value, one time, to the next part of the output file
        fwrite(&buffer, sizeof(int16_t), 1, output);
    }
    
    // Close files
    fclose(input);
    fclose(output);
}
