#!/usr/env/python3
import csv


def read_list_from_file(input_file_path):
    """assume the input file contains a list separated by lines"""
    with open(input_file_path, "r") as f:
        return [line.strip() for line in f]


def form_combinations():
    count = 0
    with open("output.csv", "w") as csvfile:
        for a in read_list_from_file("a.txt"):
            for b in read_list_from_file("b.txt"):
                for c in read_list_from_file("c.txt"):
                    count += 1
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([a, b, c])
    print("output.csv has {} rows".format(count))


def main():
    form_combinations()

    
if __name__ == '__main__':
    main()
