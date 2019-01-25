#!/usr/bin/env python3

import sys

try:
    array = [int(arg) for arg in sys.argv[1:]]
except ValueError:
    print("Integers Only")
    sys.exit(1)

def merge(arrA, arrB):
    merged = []
    while arrA or arrB:
        if not arrA:
            return arrB + merged
        elif not arrB:
            return arrA + merged
        elif arrA[-1] >= arrB[-1]:
            merged.insert(0, arrA.pop())
        else:
            merged.insert(0, arrB.pop())
    return merged

def sort(arr):
    arr = [[i] for i in arr]
    while len(arr) > 1:
        arrA = arr.pop()
        arrB = arr.pop()
        arr.insert(0, merge(arrA, arrB))
    return arr[0]

print(sort(array))