import fileinput
from collections import namedtuple

Mapping = namedtuple("Mapping", "dst_start dst_end src_start src_end length")

with fileinput.input(files=('input'), encoding="utf-8") as f:
    key = None
    m: dict[str, list[Mapping]] = {}
    for n, line in enumerate(f):
        if n == 0:
            title, numbers = line.rstrip('\n').split(': ')
            assert title == "seeds"
            seeds = [int(i) for i in numbers.split()]
        elif line.endswith("map:\n"):
            key = line.split()[0]
            m[key] = []
        elif line != '\n':
            dst_start, src_start, length = [int(i) for i in line.rstrip('\n').split()]
            m[key].append(Mapping(dst_start, dst_start + length, src_start, src_start + length, length))

    min_num = 999999999999

    for i in range(0, len(seeds), 2):
        num_ranges = [[seeds[i], seeds[i + 1]]]

        # print("before: {}".format(num_ranges))
        for key, mappings in m.items():
            mapped_ranges = []
            for mapping in mappings:
                # print(" - ", mapping)
                unmapped_ranges = []
                while len(num_ranges) != 0:
                    num_range = num_ranges.pop()
                    num_range_start = num_range[0]
                    num_range_end = num_range[0] + num_range[1]

                    # Check if num ranges overlap (StartA <= EndB) and (EndA >= StartB)
                    if num_range_start < mapping.src_end and num_range_end >= mapping.src_start:
                        # Split range into 3 ranges: [before mapping], mapped, [after mapping]

                        # Before mapping
                        if num_range_start < mapping.src_start:
                            # print("\tbefore", [num_range_start, mapping.src_start - num_range_start])
                            unmapped_ranges.append([num_range_start, mapping.src_start - num_range_start])

                        # Mapping
                        # print("\tmapped", [
                        #     mapping.dst_start + max(num_range_start, mapping.src_start) - mapping.src_start,
                        #     min(num_range_end, mapping.src_end) - max(num_range_start, mapping.src_start),
                        # ])
                        mapped_ranges.append([
                            mapping.dst_start + max(num_range_start, mapping.src_start) - mapping.src_start,
                            min(num_range_end, mapping.src_end) - max(num_range_start, mapping.src_start),
                        ])

                        # After mapping
                        if num_range_end > mapping.src_end:
                            # print("\tafter", [mapping.src_end, num_range_end - mapping.src_end])
                            unmapped_ranges.append([mapping.src_end, num_range_end - mapping.src_end])
                    else:
                        unmapped_ranges.append(num_range)
                num_ranges = unmapped_ranges
            num_ranges.extend(mapped_ranges)
            # print("after {}: {}".format( key, num_ranges))
        lowest_range_start = min([range[0] for range in num_ranges])
        if lowest_range_start < min_num:
            min_num = lowest_range_start

    print(min_num)
