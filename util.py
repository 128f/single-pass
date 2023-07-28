from abc import ABC, abstractmethod
import json


def getFile(filename: str):
    with open(filename, "rb") as file:
        return json.load(file)


class Processor(ABC):
    """
    Base class for functions used to gather statistics on streaming
    input data.
    The main idea is that each data object will come through once
    and be presented to the process function.
    Each class can store state for later examination.
    """

    @abstractmethod
    def process(self, data):
        pass


class Counter(Processor):
    """
    Simply increment a counter as data passes through
    """

    count = 0

    def process(self, _data):
        self.count = self.count + 1


class CollectUnique(Processor):
    """
    Given a key, collect a set of unique values that pass through
    """

    unique: set = set()

    def __init__(self, key):
        self.key = key

    def process(self, data):
        try:
            self.unique.add(data[self.key])
        except KeyError:
            pass
        except Exception as e:
            print("We don't know what happened")
            print(e)

    def count(self):
        return len(self.unique)


class CollectUniqueMulti(Processor):
    """
    Given a list of keys, collect a set of unique combinations of the values
    """

    unique: set = set()

    def __init__(self, keys: list[str]):
        self.keys = keys

    def process(self, data):
        try:
            values = [data[key] for key in self.keys]
            self.unique.add(",".join(values))
        except KeyError:
            pass
        except Exception as e:
            print("We don't know what happened")
            print(e)

    def count(self):
        return len(self.unique)


class Average(Processor):
    """
    Average across a given key
    """

    def __init__(self, key):
        self.key = key

    total = 0
    count = 0

    def process(self, data):
        try:
            value = data[self.key]
            assert isinstance(value, (int, float, complex))
            # these next two would be better if they were atomic
            self.total = self.total + value
            self.count = self.count + 1
        except KeyError:
            pass
        except Exception as e:
            print("Average collector error: ", e)

    def compute(self):
        if self.count == 0:
            return 0
        return self.total / self.count


class Minimum(Processor):
    """
    Minimum across a given key
    """

    def __init__(self, key):
        self.key = key

    min_object = None
    minimum = 9999999999

    def process(self, data):
        try:
            value = data[self.key]
            assert isinstance(value, (int, float, complex))
            # assuming we have the same type
            if value < self.minimum:
                self.minimum = value
                self.min_object = data
        except KeyError as e:
            print("Key error: ", e)
        except Exception as e:
            print("Minimum collector error: ", e)


class Maximum(Processor):
    """
    Maximum across a given key
    """

    def __init__(self, key):
        self.key = key

    max_object = None
    maximum = -9999999999

    def process(self, data):
        try:
            value = data[self.key]
            assert isinstance(value, (int, float, complex))
            # assuming we have the same type
            if value > self.maximum:
                self.maximum = value
                self.max_object = data
        except KeyError as e:
            print("Key error: ", e)
        except Exception as e:
            print("Maximum collector error: ", e)


class GroupBy(Processor):
    """
    Group objects across a given key
    """

    def __init__(self, key):
        self.key = key

    table = {}

    def process(self, data):
        try:
            value = data[self.key]
            if value not in self.table:
                self.table[value] = []
            self.table[value].append(data)
        except KeyError:
            pass
        except Exception as e:
            print("GroupBy error: ", e)


def process(data: list, processors: list[Processor]):
    for block in data:
        for p in processors:
            p.process(block)
