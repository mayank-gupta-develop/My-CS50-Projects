import csv
import sys


def main():

    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python dna.py database.csv sequence.txt")
        sys.exit(1)

    # Read database file
    with open(sys.argv[1], newline='') as file:
        reader = csv.DictReader(file)
        strs = reader.fieldnames[1:]
        database = []

        for row in reader:
            for s in strs:
                row[s] = int(row[s])
            database.append(row)

    # Read DNA sequence file
    with open(sys.argv[2]) as file:
        sequence = file.read().strip()

    # Find longest match of each STR
    counts = {}
    for s in strs:
        counts[s] = longest_match(sequence, s)

    # Check database for matching profile
    for person in database:
        match = True
        for s in strs:
            if person[s] != counts[s]:
                match = False
                break
        if match:
            print(person["name"])
            return

    # If no match
    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0

        while sequence[i + count * subsequence_length:i + (count + 1) * subsequence_length] == subsequence:
            count += 1

        longest_run = max(longest_run, count)

    return longest_run


if __name__ == "__main__":
    main()
