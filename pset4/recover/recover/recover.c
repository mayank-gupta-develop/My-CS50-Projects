#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Must have exactly 1 command line argument
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open memory card file
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    BYTE buffer[512];
    int file_count = 0;
    FILE *output = NULL;
    char filename[8];

    // Read 512 bytes at a time
    while (fread(buffer, sizeof(BYTE), 512, input) == 512)
    {
        // Check if this block starts a new JPEG
        bool is_jpg = buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
                      (buffer[3] & 0xf0) == 0xe0;

        if (is_jpg)
        {
            // Close previous jpg if already open
            if (output != NULL)
            {
                fclose(output);
            }

            // Create new filename
            sprintf(filename, "%03i.jpg", file_count);
            file_count++;

            // Open new jpg file
            output = fopen(filename, "w");
        }

        // If output file is open, write to it
        if (output != NULL)
        {
            fwrite(buffer, sizeof(BYTE), 512, output);
        }
    }

    // Close files
    if (output != NULL)
    {
        fclose(output);
    }
    fclose(input);

    return 0;
}
