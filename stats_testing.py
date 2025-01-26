import random


"""

Units

unit_templates = [
    [20, 10, 10, 10, 10],
    [10, 20, 10, 10, 10],
    [10, 10, 20, 10, 10],
    [10, 10, 10, 20, 10],
    [10, 10, 10, 10, 20],
    [30, 20, 5, 10, 10],
    [10, 30, 20, 5, 10],
    [10, 10, 30, 20, 5],
    [5, 10, 10, 30, 20],
    [20, 5, 10, 10, 30],
    [40, 5, 10, 20, 30],
    [30, 40, 5, 10, 20],
    [20, 30, 40, 5, 10],
    [10, 20, 30, 40, 5],
    [5, 10, 20, 30, 40],
    ]


"""

def get_armor(amount):

    total_arm = 0
    cur_arm = random.randint(0,amount)
    total_arm += cur_arm
    while total_arm == amount:
        cur_arm = random.randint(0,amount)
        total_arm += cur_arm
    return total_arm

n = 1000
for i in [5, 10, 20, 30, 40]:
    total_armor = 0
    for _ in range(n):
        total_armor += get_armor(i)

    print(f"Average Armor made ({i} armor): {total_armor / n:.4f}")