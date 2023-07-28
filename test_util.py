import util
import pytest

@pytest.fixture
def sample_file():
    file = util.getFile("./sample.json")
    len(file)
    return file

def test_counter_initial_state():
    counter = util.Counter()
    assert(counter.count == 0)

def test_counter(sample_file):
    counter = util.Counter()
    [counter.process(i) for i in sample_file]
    assert(counter.count == 10)

def test_unique_initial_state():
    unique = util.CollectUnique("trailer_id")
    assert(unique.count() == 0)

def test_unique(sample_file):
    unique = util.CollectUnique("trailer_id")
    [unique.process(i) for i in sample_file]
    assert(unique.count() == 6)

def test_unique_multi_key_initial_state():
    unique_multi_key = util.CollectUniqueMulti(["yard_id", "trailer_id"])
    assert(unique_multi_key.count() == 0)

def test_unique_multi_key(sample_file):
    unique_multi_key = util.CollectUniqueMulti(["yard_id", "trailer_id"])
    [unique_multi_key.process(i) for i in sample_file]
    assert(unique_multi_key.count() == 10)

def test_min_collector_initial_state():
    min_collector = util.Minimum("duration_minutes")
    assert(min_collector.minimum == 9999999999) # indicates we haven't seen any object

def test_min_collector(sample_file):
    min_collector = util.Minimum("duration_minutes")
    [min_collector.process(i) for i in sample_file]
    assert(min_collector.minimum == 45)

def test_max_collector_initial_state():
    max_collector = util.Maximum("duration_minutes")
    assert(max_collector.maximum == -9999999999) # indicates we haven't seen any object

def test_max_collector(sample_file):
    max_collector = util.Maximum("duration_minutes")
    [max_collector.process(i) for i in sample_file]
    assert(max_collector.maximum == 240) # indicates we haven't seen any object

def test_group_by_initial_state():
    group_by = util.GroupBy("yard_id")
    assert(len(group_by.table.keys()) == 0)

def test_group_by(sample_file):
    group_by = util.GroupBy("yard_id")
    [group_by.process(i) for i in sample_file]
    assert(len(group_by.table.keys()) == 3)
