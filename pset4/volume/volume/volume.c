#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef int16_t SAMPLE;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open input file
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open input file.\n");
        return 1;
    }

    // Open output file
    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open output file.\n");
        fclose(input);
        return 1;
    }

    // Convert factor to float
    float factor = atof(argv[3]);

    // Copy WAV header (44 bytes)
    uint8_t header[44];
    fread(header, sizeof(uint8_t), 44, input);
    fwrite(header, sizeof(uint8_t), 44, output);

    // Read samples and write adjusted samples
    SAMPLE buffer;
    while (fread(&buffer, sizeof(SAMPLE), 1, input))
    {
        buffer = buffer * factor;
        fwrite(&buffer, sizeof(SAMPLE), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);

    return 0;
}
