import sys

import pandas


def main():
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    pd1 = pandas.read_csv(file1, index_col=0)
    pd2 = pandas.read_csv(file2, index_col=0)
    combined = pd1 + pd2
    print(combined.to_csv())

main()
