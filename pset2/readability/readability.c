#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    // Ask user for text
    string text = get_string("Text: ");

    int letters = 0;
    int words = 1;     // start from 1 because last word has no space after it
    int sentences = 0;

    // Count letters, words, sentences
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
        else if (text[i] == ' ')
        {
            words++;
        }
        else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }

    // Calculate L and S
    float L = (letters * 100.0) / words;
    float S = (sentences * 100.0) / words;

    // Coleman-Liau formula
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // Print result
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}
