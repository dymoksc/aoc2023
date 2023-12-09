import fileinput


def get_prev_element(nums: list[int]) -> int:
    if len([i for i in nums if i != 0]) == 0:
        return 0
    else:
        return nums[0] - get_prev_element([nums[i] - nums[i - 1] for i in range(1, len(nums))])


sum = 0
with fileinput.input(files=("input"), encoding="utf-8") as f:
    for l in f:
        numbers = [int(i) for i in l.strip("\n").split()]
        sum += get_prev_element(numbers)

print(sum)
