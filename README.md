###  One pass processing

A collection of data-processing classes useful for collecting stats from a list of data or stream. Very similar to what I understand [statstream](https://github.com/jmaces/statstream) to be, but as of right now, worse.

### How to use this

```
def process(data: list, processors: list[Processor]):
    for block in data:
        for p in processors:
            p.process(block)

data = getFile('./sample.json') # list of dicts

counter = Counter()
unique = CollectUnique("trailer_id")
unique_multi_key = CollectUniqueMulti(["yard_id", "trailer_id"])
average = Average("duration_minutes")
min_collector = Minimum("duration_minutes")
max_collector = Maximum("duration_minutes")
group_by_yard = GroupBy("yard_id")

process(data, [counter, unique, unique_multi_key, average, min_collector, max_collector, group_by_yard])

print("count: ", counter.count)
print("unique trailers: ", unique.count())
print("unique trailer/yard combos: ", unique_multi_key.count())
print("average duration: ", average.compute())
print("min: ", min_collector.minimum)
print("max: ", max_collector.maximum)
print("grouped by yard ", group_by_yard.table)
```

### Why do this?

Just wanted to dust off my python skills.
