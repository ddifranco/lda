#! /usr/bin/python3

import pdb
import json

for cleaner in ["raw", "rplus_headers", "baseline", "bminus_hfilter", "bminus_basic", "bminus_lemmatize", "bminus_sfilter", "bplus_posfilter"]:

    pct_tracker = []
    group_tracker = []
    for i in range(20):
        group_tracker.append([])

    with open(f"{cleaner}.json", "r") as f:

        data = json.loads(f.read())
        for goldgroup, assignments in data.items():
            total = sum(assignments)
            maxval = max(assignments)
            pct = round((maxval / total) * 100, 2)
            bestgroup = assignments.index(maxval)
            group_tracker[bestgroup].append(goldgroup)
            pct_tracker.append(pct)

    avg_pct = round(sum(pct_tracker) / 20, 2)
    print(f"Results from {cleaner} preprocessing")
    print(f"\tAverage same-group assignment -> {avg_pct}%")
    print("\tCollisions:")
    for group in group_tracker:
        if len(group) > 1:
            print(f"\t{json.dumps(group)}")
