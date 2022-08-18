import json

import z4
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn

TEAMS_PER_ACTIVITY = 4
TEAMS = 24
ACTIVITIES = 5

assert TEAMS % TEAMS_PER_ACTIVITY == 0

rounds = TEAMS // TEAMS_PER_ACTIVITY
assert rounds == ACTIVITIES + 1


def z4_sum(x):
    return sum(x)


print("Building constraints...")

"""
x_i_j_k is true iff team i is in activity k at time j

Apparently int variables constrained to 0 or 1 are a lot faster than bool variables for this problem.
Running time with bool variables: ~22 min
Running time with int variables: ~17 seconds
"""
assignments = [
    [[z4.Int(f"x_{i}_{j}_{k}") for k in range(rounds)] for j in range(rounds)]
    for i in range(TEAMS)
]

constraints = []

for i in range(TEAMS):
    for j in range(rounds):
        for k in range(rounds):
            constraints.append(0 <= assignments[i][j][k])
            constraints.append(assignments[i][j][k] <= 1)

"""
Simplification: We can assume the initial round of assignments
"""
for i in range(TEAMS):
    first_k = i // TEAMS_PER_ACTIVITY
    for k in range(rounds):
        constraints.append(assignments[i][0][k] == int(k == first_k))

"""
Simplification: We can assume that team 0 participates in the activities in order
"""
for j in range(rounds):
    for k in range(rounds):
        constraints.append(assignments[0][j][k] == int(k == j))


"""
Each team must be assigned to exactly one activity at each time
"""
for i in range(TEAMS):
    for j in range(rounds):
        assign_count = z4_sum(assignments[i][j])
        constraints.append(assign_count == 1)

"""
Each team must be on a different activity every time
"""
for i in range(TEAMS):
    for k in range(rounds):
        assign_count = z4_sum(assignments[i][j][k] for j in range(rounds))
        constraints.append(assign_count == 1)


"""
Each activity at every time should have exactly TEAMS_PER_ACTIVITY teams assigned to it
"""
for j in range(rounds):
    for k in range(rounds):
        teams_on_activity = z4_sum(assignments[i][j][k] for i in range(TEAMS))
        constraints.append(teams_on_activity == TEAMS_PER_ACTIVITY)


"""
Each pair of teams should only be at the same activity max 1 time
However we don't care about teams meeting each other in the last activity,
which is the break activity
"""
for i1 in range(TEAMS):
    for i2 in range(i1 + 1, TEAMS):
        same_activity_count = z4_sum(
            assignments[i1][j][k] * assignments[i2][j][k]
            for j in range(rounds)
            for k in range(rounds - 1)  # Exclude break activity
        )
        constraints.append(same_activity_count <= 1)

print(f"Variables:   {TEAMS_PER_ACTIVITY * rounds * rounds:,}")
print(f"Constraints: {len(constraints):,}")
print("Solving (this make take A LOT of time)...")

with Progress(SpinnerColumn(), TimeElapsedColumn()) as progress:
    task = progress.add_task("Solving", total=None)
    model = z4.easy_solve(constraints)
    results = [
        [[model[assignments[i][j][k]] for k in range(rounds)] for j in range(rounds)]
        for i in range(TEAMS)
    ]


def get_activity(i: int, j: int):
    result_k = -1
    for k in range(rounds):
        if results[i][j][k] == 1:
            assert result_k == -1
            result_k = k

    assert result_k != -1
    return result_k


print()
print("Solution:")
solution = []
for j in range(rounds):
    by_activity = [[] for _ in range(rounds)]
    for i in range(TEAMS):
        activity = get_activity(i, j)
        by_activity[activity].append(i)

    print(f"Time {j}:")
    print(by_activity)
    print()

    solution.append(by_activity)

with open("solution.json", "w") as f:
    json.dump(solution, f)
    f.write("\n")
