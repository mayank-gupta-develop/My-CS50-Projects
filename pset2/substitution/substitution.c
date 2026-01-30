#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

bool valid_key(string key);

int main(int argc, string argv[])
{
    // Must have exactly 1 argument
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    string key = argv[1];

    // Validate key
    if (!valid_key(key))
    {
        printf("Key must contain 26 unique alphabetic characters.\n");
        return 1;
    }

    // Get plaintext
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");

    // Encrypt
    for (int i = 0; i < strlen(plaintext); i++)
    {
        char c = plaintext[i];

        if (isupper(c))
        {
            int index = c - 'A';
            printf("%c", toupper(key[index]));
        }
        else if (islower(c))
        {
            int index = c - 'a';
            printf("%c", tolower(key[index]));
        }
        else
        {
            printf("%c", c);
        }
    }

    printf("\n");
    return 0;
}

// Function to check if key is valid
bool valid_key(string key)
{
    // Must be 26 characters
    if (strlen(key) != 26)
    {
        return false;
    }

    int seen[26] = {0};

    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            return false;
        }

        int index = toupper(key[i]) - 'A';

        // Duplicate found
        if (seen[index] == 1)
        {
            return false;
        }

        seen[index] = 1;
    }

    return true;
}
