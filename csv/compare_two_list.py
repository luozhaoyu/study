#!/usr/env/python3
import csv
import sys


def read_list_from_csv(path):
    result = []
    with open(path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            result.append(row[0])
    return result


def main():
    set1 = set(read_list_from_csv(sys.argv[1]))
    set2 = set(read_list_from_csv(sys.argv[2]))
    print(
        "{} has {}, {} has {}, {} in both: {}".format(
            sys.argv[1],
            len(set1),
            sys.argv[2],
            len(set2),
            len(set1 & set2),
            set1 & set2,
        )
    )


if __name__ == "__main__":
    main()
