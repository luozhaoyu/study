#!/usr/env/python3
import csv


def read_list_from_file(input_file_path):
    """assume the input file contains a list separated by lines"""
    with open(input_file_path, "r") as f:
        lines = [line.strip() for line in f]
        return lines[0], lines[1:]


def form_combinations():
    count = 0
    header_a, list_a = read_list_from_file("a.txt")
    header_b, list_b = read_list_from_file("b.txt")
    header_c, list_c = read_list_from_file("c.txt")
    # output_file_name 是输出文件路径，默认是当前目录下，也可改成 C:\output.csv
    output_file_name = "output_{}_{}_{}.csv".format(header_a, header_b, header_c)
    with open(output_file_name, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([header_a, header_b, header_c])
        for a in list_a:
            for b in list_b:
                for c in list_c:
                    count += 1
                    writer.writerow([a, b, c])
    print("{} has {} rows".format(output_file_name, count))


def main():
    form_combinations()

    
if __name__ == '__main__':
    main()
