#!/usr/bin/env python3

import argparse
import os
from ruamel import yaml
from beautifultable import BeautifulTable
from termcolor import colored

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
        self.file_a_contents = self._load_file(file_a)
        self.file_b_contents = self._load_file(file_b)

    def _load_file(self, file_name):
        with open(file_name, 'r') as f:
            try:
                return yaml.round_trip_load(f.read(), preserve_quotes=True)
            except yaml.constructor.DuplicateKeyError as e:
                raise DuplicateKeyException("%s in file %s" % (e.problem, file_name))

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
            if not self.file_a_contents.get(key) or not self.file_b_contents.get(key):
                continue
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

    def check_for_additional_keys(self):
        """
        Checks the two YAML files for keys present in one but not the other
        """
        additional_keys_in_file_a = list(
            set(self.file_a_contents.keys()) - set(self.file_b_contents.keys()))
        additional_keys_in_file_b = list(
            set(self.file_b_contents.keys()) - set(self.file_a_contents.keys()))

        return {
            "file_a": additional_keys_in_file_a,
            "file_b": additional_keys_in_file_b
        }

    def run(self, file_a, file_b, show_differences, show_additional):
        output = ""
        try:
            self.load(file_a, file_b)
        except DuplicateKeyException as e:
            return colored(e, 'red', attrs=['bold'])

        duplicates = self.check_for_duplicates()
        if duplicates:
            output += self.print_duplicates(duplicates) + os.linesep

        if show_differences:
            differences = self.check_for_differences()
            if differences:
                output += self.print_differences(differences) + os.linesep

        if show_additional:
            additional = self.check_for_additional_keys()
            if additional:
                output += self.print_additional(additional) + os.linesep

        return output

    def print_duplicates(self, duplicates):
        table = self._create_table()
        table.column_headers = [
            colored('Key', 'white', attrs=['bold']),
            colored('Value', 'white', attrs=['bold']),
        ]
        for duplicate in duplicates:
            table.append_row([
                colored(duplicate['key'], 'blue', attrs=['bold']),
                colored(str(duplicate['value']), 'white', attrs=['bold']),
            ])

        return 'The following values are identical in both files:' + os.linesep + table.get_string()

    def print_differences(self, differences):
        table = self._create_table()
        table.column_headers = [
            colored('Key', 'white', attrs=['bold']),
            colored(self.file_a, 'white', attrs=['bold']),
            colored(self.file_b, 'white', attrs=['bold']),
        ]
        for difference in differences:
            table.append_row([
                colored(difference["key"], 'blue', attrs=['bold']),
                colored(difference["file_a"]["value"], 'red', attrs=['bold']),
                colored(difference["file_b"]["value"], 'green', attrs=['bold']),
            ])

        return 'The following values are different in both files:' + os.linesep + table.get_string()

    def print_additional(self, additional):
        number_of_items_in_file_a = len(additional["file_a"])
        number_of_items_in_file_b = len(additional["file_b"])
        number_of_keys = number_of_items_in_file_a if number_of_items_in_file_a > number_of_items_in_file_b else number_of_items_in_file_b

        table = self._create_table()
        table.column_headers = [
            colored(self.file_a, 'white', attrs=['bold']),
            colored(self.file_b, 'white', attrs=['bold']),
        ]
        for i in range(number_of_keys):
            table.append_row([
                colored(additional["file_a"][i] if number_of_items_in_file_a > i else '', 'red', attrs=['bold']),
                colored(additional["file_b"][i] if number_of_items_in_file_b > i else '', 'green', attrs=['bold'])
            ])
        return 'The following keys are defined in one file, but not the other:' + os.linesep + table.get_string()

    def _create_table(self):
        _, column_width = os.popen('stty size', 'r').read().split()
        max_width = int(column_width, 10) if int(
            column_width, 10) > MIN_TERMINAL_WIDTH else MIN_TERMINAL_WIDTH
        return BeautifulTable(max_width=max_width)


class DuplicateKeyException(Exception):
    pass


def run(a, b, differences=False, additional=False):
    ys = YamlStats()
    return ys.run(a, b, differences, additional)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("a", help="First File to Diff")
    parser.add_argument("b", help="Second File to Diff")
    parser.add_argument("-d", "--differences",
                        help="Show a table of the differences in values",
                        dest="differences", action="store_true")
    parser.add_argument("-a", "--additional",
                        help="Show a table of the additional keys not found in the other file",
                        dest="additional", action="store_true")
    args = parser.parse_args()
    print(run(args.a, args.b, args.differences, args.additional))
