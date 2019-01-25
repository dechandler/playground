#!/usr/bin/env python3

import sys

try:
    array = [int(arg) for arg in sys.argv[1:]]
except ValueError:
    print("Integers Only")
    sys.exit(1)

def sort(arr):
    if len(arr) <= 1:
        return arr

    print(arr)
    pivot = arr[-1]
    less = []
    more = []
    equal = []
    for item in arr:
        if item > pivot:
            more.append(item)
        elif item < pivot:
            less.append(item)
        else:
            equal.append(item)

    return sort(less) + equal + sort(more)

print(sort(array))