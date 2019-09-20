#!/usr/bin/env python3

import argparse
import os
from ruamel import yaml
from beautifultable import BeautifulTable

SEPARATOR = "#######################################" + os.linesep
MIN_TERMINAL_WIDTH = 160


class YamlStats:
    """
    Detects duplicate, different and missing key/value pairs between
    two YAML files
    """

    def __init__(self):
        self.file_a = ""
        self.file_b = ""
        self.file_a_contents = {}
        self.file_b_contents = {}

    def load(self, file_a, file_b):
        """
        Read the YAML files off disk and parse them
        """
        self.file_a = file_a
        self.file_b = file_b

        with open(file_a, 'r') as f:
            self.file_a_contents = yaml.round_trip_load(
                f.read(), preserve_quotes=True)

        with open(file_b, 'r') as f:
            self.file_b_contents = yaml.round_trip_load(
                f.read(), preserve_quotes=True)

    def check_for_duplicates(self):
        """
        Checks the two YAML files for identical key/value pairs and
        adds them to a list
        """
        duplicates = []
        for key in self.file_b_contents.keys():
            if self.file_b_contents.get(key) == self.file_a_contents.get(key):
                duplicates.append(
                    {
                        "key": key,
                        "value": self.file_a_contents.get(key)
                    }
                )

        return duplicates

    def check_for_differences(self):
        """
        Checks the two YAML files for matching keys with different values and
        adds them to a list
        """
        differences = []
        for key in self.file_b_contents.keys():
            if self.file_b_contents.get(key) != self.file_a_contents.get(key):
                differences.append(
                    {
                        "key": key,
                        "file_a": {
                            "file_name": self.file_a,
                            "value": str(self.file_a_contents.get(key)),
                        },
                        "file_b": {
                            "file_name": self.file_b,
                            "value": str(self.file_b_contents.get(key)),
                        }
                    }
                )

        return differences

    def run(self, file_a, file_b, show_differences):
        output = ""
        self.load(file_a, file_b)

        duplicates = self.check_for_duplicates()
        if duplicates:
            output += self.print_duplicates(duplicates)

        if show_differences:
            differences = self.check_for_differences()
            if differences:
                output += self.print_differences(differences)

        return output

    def print_duplicates(self, duplicates):
        output = SEPARATOR
        for duplicate in duplicates:
            output += ("%s is the same in both files:" %
                       duplicate["key"]) + os.linesep
            output += str(duplicate["value"]) + os.linesep
            output += SEPARATOR

        return output

    def print_differences(self, differences):
        _, column_width = os.popen('stty size', 'r').read().split()
        max_width = int(column_width, 10) if int(
            column_width, 10) < MIN_TERMINAL_WIDTH else MIN_TERMINAL_WIDTH
        table = BeautifulTable(max_width=max_width)
        table.column_headers = ['Key', self.file_a, self.file_b]
        for difference in differences:
            table.append_row([
                difference["key"],
                difference["file_a"]["value"],
                difference["file_b"]["value"]
            ])

        return table.get_string()


def run(a, b, differences=False):
    ys = YamlStats()
    return ys.run(a, b, differences)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("a", help="First File to Diff")
    parser.add_argument("b", help="Second File to Diff")
    parser.add_argument("-d", "--differences",
                        help="Show a table of the differences in values",
                        dest="differences", action="store_true")
    args = parser.parse_args()
    print(run(args.a, args.b, args.differences))
