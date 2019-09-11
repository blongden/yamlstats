import copy
import sys
from functools import reduce
from ruamel import yaml
from datadiff import diff


class YamlHierarchy:
    """
    Represents a (possible) hierarchy of YAML. The idea is to initiate each element in the hierarchy and `combine` them.

    The source for each value is preserved and outputted by default in the result of as_yaml.
    """
    def __init__(self, txt, **kwargs):
        self.data = yaml.load(txt, Loader=yaml.RoundTripLoader)
        self.sources = {}
        self.duplicated = {}
        for key in self.data.keys():
            self.sources[key] = self
            self.duplicated[key] = []
        self.options = kwargs

    def combine(self, to_combine):
        combined = copy.copy(self)
        for key, item in combined.data.items():
            if item != to_combine.data.get(key):
                combined.data[key] = to_combine.data.get(key)
                combined.sources[key] = to_combine
            else:
                combined.duplicated[key].append((self, to_combine))
        combined.options = to_combine.options
        return combined

    def __str__(self):
        if self.options.get("name"):
            return self.options.get("name")
        return super().__str__()

    def as_yaml(self, annotate_source=True):
        if annotate_source:
            for key, source in self.sources.items():
                self.data.yaml_set_comment_before_after_key(key, str(source))
        return yaml.dump(self.data, Dumper=yaml.RoundTripDumper)

    def compare(self, to_compare):
        return diff(dict(self.data.items()), dict(to_compare.data.items()))


def file_get_contents(filename):
    with open(filename) as f:
        return f.read()


def read_yaml_files():
    to_combine = []
    for filename in sys.argv[1:]:
        to_combine.append(YamlHierarchy(file_get_contents(filename), name=filename))
    return to_combine


if __name__ == "__main__":
    combined = reduce(lambda accumulator, item: accumulator.combine(item), read_yaml_files())
    print(combined.as_yaml())
    for key, sources in combined.duplicated.items():
        if len(sources):
            print("\"{}\" is duplicated between:".format(key))
            for x in sources:
                print("  {} => {}".format(x[0], x[1]))

