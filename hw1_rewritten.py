import random
import math
from termcolor import colored
from collections import defaultdict

"""

A rough rewrite of the debugging tools to allow better visuals and more clarities of what actions is going on in a battle at a glance

Also associated names with every single kind of unit

"""

# Setting to True will cause the simulator to
# throw out a lot of additional text. Not all
# of it helpful.
DEBUG = True


# Each sublist represents a unit type's stats
# The values are (by index):
# - 0: Damage Value
# - 1: Accuracy Value (To-Hit)
# - 2: Evasion (dodge)
# - 3: Armor (damage reduction)
# - 4: Health
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


# {x} to be replaced if there is multiple of a unit on a team
unit_names = [
    "Fighter {x} (Tier 1)",
    "Sniper {x} (Tier 1)",
    "Wraith {x} (Tier 1)",
    "Golem {x} (Tier 1)",
    "Brute {x} (Tier 1)",
    "Fighter {x} (Tier 2)",
    "Sniper {x} (Tier 2)",
    "Wraith {x} (Tier 2)",
    "Golem {x} (Tier 2)",
    "Brute {x} (Tier 2)",
    "Fighter {x} (Tier 3)",
    "Sniper {x} (Tier 3)",
    "Wraith {x} (Tier 3)",
    "Golem {x} (Tier 3)",
    "Brute {x} (Tier 3)"
]

# Index constants for the above unit_templates
DAMAGE = 0
ACCURACY = 1
EVASION = 2
ARMOR = 3
HEALTH = 4

# Print function controlled by the DEBUG constants
def output(msg):
    if DEBUG:
        print(msg)

# Basic unit of the game
class Actor:
    def __init__(self,
                 ID,
                 data,
                 team_name,
                 spot,
                 name):
        self.ID = ID            # Which unit_templates
        self.data = data        # Unit stats (list)
        self.team_name = team_name  # name of the team
        self.spot = spot            # spot in the team
        self.name = name            # name for output purposes

        # for i in range(len(self.data)):
        #     var = self.data[i]//5
        #     adjustment = random.randint(-var, var)
        #     self.data[i] += adjustment

    def make_accuracy(self):
        return (random.randint(0, self.get_accuracy()) + random.randint(0, self.get_accuracy()) + random.randint(0, self.get_evasion())) // 3
    
    def make_evasion(self):
        return (random.randint(0, self.get_evasion()) + random.randint(0, self.get_evasion()) + random.randint(0, self.get_accuracy())) // 3

    def make_damage(self):
        total_dmg = 0
        cur_dmg = random.randint(0,self.get_damage())
        total_dmg += cur_dmg
        while cur_dmg == self.get_damage():
            cur_dmg = random.randint(0,self.get_damage())
            if cur_dmg == 0:
                total_dmg = 0
            else:
                total_dmg += cur_dmg
        return total_dmg

    def make_armor(self):
        total_arm = 0
        cur_arm = random.randint(0,self.get_armor())
        total_arm += cur_arm
        while total_arm == self.get_armor():
            cur_arm = random.randint(0,self.get_armor())
            total_arm += cur_arm
        return total_arm

    def make_defense(self, dmg):
        dmg -= self.make_armor()
        if dmg > 0:
            self.data[HEALTH] -= dmg
            if self.get_health() <= 0:
                self.data[HEALTH] = 0
            return dmg
        return 0
    def get_ID(self):
        return self.ID
    def get_health(self):
        return self.data[HEALTH]
    def get_damage(self):
        return self.data[DAMAGE]
    def get_accuracy(self):
        return self.data[ACCURACY]
    def get_evasion(self):
        return self.data[EVASION]
    def get_armor(self):
        return self.data[ARMOR]
    def get_team_name(self):
        return self.team_name
    def get_spot(self):
        return self.spot
    def get_name(self):
        return self.name

    def is_alive(self):
        return self.get_health() > 0

# Generates a randomized team using the
# various tier composition values.
# Each tier corresponds to five unit_templates
# the keys list can be used to specify types
# exactly.

class Team:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.actors = []

    def add_actor(self, actor):
        self.actors.append(actor)

def get_team_color(teamName):
    for color in ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]:
        if color in teamName: return color

    return "light_grey"

def replace_name(name, unit_number):
    if unit_number <= 1: return name.replace("{x} ", "")

    return name.replace("{x}", f"#{unit_number}")

def gen_rand_team(team_name,
                  tier0=0,
                  tier1=0,
                  tier2=0,
                  keys={}):
    
    team = Team(team_name, get_team_color(team_name))
    unit_amounts = defaultdict(lambda: 0)
    for key, amt in keys.items():
        for i in range(amt):
            stats = unit_templates[key][:]
            unit_amounts[key] += 1
            actor = Actor(key, stats, team_name, i, replace_name(unit_names[key], unit_amounts[key]))
            team.add_actor(actor)
    for i in range(tier0):
        key = random.randrange(0,5)
        stats = unit_templates[key][:]
        unit_amounts[key] += 1
        actor = Actor(key, stats, team_name, i, replace_name(unit_names[key], unit_amounts[key]))
        team.add_actor(actor)
    for i in range(tier1):
        key = random.randrange(0,5)+5
        stats = unit_templates[key][:]
        unit_amounts[key] += 1
        actor = Actor(key, stats, team_name, i, replace_name(unit_names[key], unit_amounts[key]))
        team.add_actor(actor)
    for i in range(tier2):
        key = random.randrange(0,5)+10
        stats = unit_templates[key][:]
        unit_amounts[key] += 1
        actor = Actor(key, stats, team_name, i, replace_name(unit_names[key], unit_amounts[key]))
        team.add_actor(actor)
    return team

def total_health_of_team(team):
    health = 0
    for actor in team.actors:
        health += actor.get_health()
    return health



def remove_name_count(unit_name):
    """ Removing the count from a units name for example Fighter #3 (Tier 1) -> Fighter (Tier 1) """
    split_name = unit_name.split()
    return f"{split_name[0]} {unit_name[unit_name.index('('):]}"

def print_team_composition(team):
    print(colored(f"Team {team.name}", team.color, attrs=["underline"]))
    types = {}
    for actor in team.actors:
        name = remove_name_count(actor.get_name())

        if name not in types:
            types[name] = 1
        else:
            types[name] += 1

    for i,amt in types.items():
        print(f'{colored(i, "light_green")}: {colored(amt, "light_cyan")}')
    print()

# Runs a combat round between two units.
# Each unit has a chance to attack and defend
# unless the first disables the second before
# it has a chance to go.
def combat(first, second, debug=False):

    att1 = first.make_accuracy()
    def2 = second.make_evasion()
    if att1 > def2:
        dmg1 = first.make_damage()
        dmg1 = second.make_defense(dmg1)

        if debug: print(f"{colored(first.name, get_team_color(first.team_name))} hit {colored(second.name, get_team_color(second.team_name))} for {colored(dmg1, 'yellow')} {colored(f'Health {second.get_health() + dmg1} -> {second.get_health()}', 'green')}")
    else:
        if debug: print(f"{colored(first.name, get_team_color(first.team_name))} swung at {colored(second.name, get_team_color(second.team_name))} and missed")

    if second.is_alive():
        att2 = second.make_accuracy()
        def1 = first.make_evasion()
        if att2 > def1:
            dmg2 = second.make_damage()
            dmg2 = first.make_defense(dmg2)

            if debug: print(f"{colored(second.name, get_team_color(second.team_name))} hit {colored(first.name, get_team_color(first.team_name))} for {colored(dmg2, 'yellow')} {colored(f'Health {first.get_health() + dmg2} -> {first.get_health()}', 'green')}")
        else:
            if debug: print(f"{colored(second.name, get_team_color(second.team_name))} swung at {colored(first.name, get_team_color(first.team_name))} and missed")

# Runs an entire battle between two teams
# Battle ends when one team loses all its
# units.
def battle(teamA, teamB, predictions, debug=False):

    if debug:  
        print_team_composition(teamA)
        print_team_composition(teamB)

        print(f"Prediction (Percent Health Left): {colored(f'{teamA.name}: {predictions[0]:.2%}', teamA.color)} - {colored(f'{teamB.name}: {predictions[1]:.2%}', teamB.color)}")
        print()

    round = 1
    while len(teamA.actors) > 0 and len(teamB.actors) > 0:
        
        
        if debug: 
            print(colored(f"ROUND {round}", "cyan"))
            print(f"{colored('Actors Alive:','light_grey')} {colored(len(teamA.actors), 'red')} - {colored(len(teamB.actors), 'blue')}")
            print()

        aI = random.randrange(len(teamA.actors))
        bI = random.randrange(len(teamB.actors))
        actorA = teamA.actors[aI]
        actorB = teamB.actors[bI]

        if random.random() < 0.5:
            combat(actorA, actorB, debug)
        else:
            combat(actorB, actorA, debug)

        if debug:  print()

        if not actorA.is_alive():
            
            
            if debug:
                print(f"{colored(f'Team {teamA.name}', teamA.color)} - {colored(f'{actorA.get_name()} died.', 'yellow')}")
            teamA.actors.pop(aI)
        if not actorB.is_alive():
            if debug:
                print(f"{colored(f'Team {teamB.name}', teamB.color)} - {colored(f'{actorB.get_name()} died.', 'yellow')}")
            teamB.actors.pop(bI)

        round += 1

    
    return (total_health_of_team(teamA), total_health_of_team(teamB))

# #####################################################################
# #####################################################################
# #####################################################################
# Your prediction algorithm should be in these three functions.
# If you add more functions please keep them within the bounds of
# these comment blocks.

# WARNING: You may NOT call the combat() or battle() functions in
# any of your fitness evaluations. Or recreate them.
# The assumption is, running
# a full battle between two teams is expensive time-wise. Your job
# is to give each side's AI an estimate of the cost (in terms of
# health) of the battle, with the idea that other parts of the AI
# (not simulated here) would decide to initiate combat based on
# your fitness function's prediction.

# WARNING 2: The actual team and actor objects are being passed
# into these functions for the sake of simplicity. Evaluate them.
# DO NOT change the teams or the stats of the units.

# The fitness_actor functionshould return the fitness of a single unit.
# This will form
# the basis of evaluating an entire team. Fitness values can be
# multivariate; however, remember the idea is to distill a unit's
# stats down to something simpler. What the return of this function
# (and the fitness_team function) represents and how it is used
# is totally up to you.
def fitness_actor(actr):
    return sum(actr.data)

# This should return the fitness of an entire team. Similarly to them
# unit fitness function, you are free to return one or more values.
# And use those values in any way you choose.
def fitness_team(team):
    return sum(fitness_actor(actor) for actor in team.actors)

# This function should return an estimate of the final health
# percentage of both teams as a tuple. For example, a value of 0.0
# means that, if a battle were to occur between these two teams,
# the team with 0.0 would end the battle with 0 health across all
# units. Whereas, 1.0 means a team does not lose any health.
#
# NOTE: The two health predictions DO NOT have to sum to one. This
# is not a probability distribution but an evaluation of the cost
# of battle between two teams.
def fitness_outcome(team1, team2):
    s1, s2 = fitness_team(team1)**25, fitness_team(team2)**25
    return s1/(s1+s2), s2/(s1+s2)

# #####################################################################
# #####################################################################
# #####################################################################
def main():

    # Number of battles to simulate.
    NUM_BATTLES = 500
    finalhealth1 = []
    finalhealth2 = []
    error1 = []
    error2 = []
    preds1 = []
    preds2 = []
    winner = []

    ################################################
    # Use these to configure team composition
    team1_tier1 = 0
    team1_tier2 = 0
    team1_tier3 = 0
    team1_keys = {8: 70}
    
    team2_tier1 = 0
    team2_tier2 = 0
    team2_tier3 = 0
    team2_keys = {12: 1}

    TEAM1 = "red"
    TEAM2 = "blue"
    #################################################
    
    total_error = 0

    for i in range(NUM_BATTLES):
        team1 = gen_rand_team(TEAM1,
                              team1_tier1,
                              team1_tier2,
                              team1_tier3,
                              team1_keys)
        team2 = gen_rand_team(TEAM2,
                              team2_tier1,
                              team2_tier2,
                              team2_tier3,
                              team2_keys)

        team1_health = total_health_of_team(team1)
        team2_health = total_health_of_team(team2)


        p1, p2 = fitness_outcome(team1, team2)
        result1, result2 = battle(team1, team2, (p1, p2), debug=False) # Only show one battle every 100 battles

        fh1 = result1/team1_health
        fh2 = result2/team2_health
        total_error += abs(fh1-p1) + abs(fh2-p2)
        
        if result1 > result2:
            winner.append(1)
        elif result2 > result1:
            winner.append(2)
        else:
            winner.append(0)
            print("ERROR: TIE")

    win1 = winner.count(1)
    win2 = winner.count(2)
    print(colored(f'Team {TEAM1} wins: {win1:<5}', get_team_color(TEAM1)))
    print(colored(f'Team {TEAM2} wins: {win2:<5}', get_team_color(TEAM2)))

    print(colored(f'Average Total Error: {total_error / (2*NUM_BATTLES):.4f}', "green"))

def heuristic_faceoff(heuristic1, heuristic2):
     # Number of battles to simulate.
    NUM_BATTLES = 1000
    finalhealth1 = []
    finalhealth2 = []
    error1 = []
    error2 = []
    preds1 = []
    preds2 = []
    winner = []

    ################################################
    # Use these to configure team composition

    team1_keys = {}
    team2_keys = {}

    TEAM1 = "red"
    TEAM2 = "blue"
    #################################################
    
    total_error_heuristic_1 = 0
    total_error_heuristic_2 = 0
    heuristic_score = [0, 0]
    win1, win2, ties = 0, 0, 0

    for i in range(NUM_BATTLES):
        team1_tier1 = random.randint(1, 10)
        team1_tier2 = random.randint(0, 10)
        team1_tier3 = random.randint(0, 10)
        team2_tier1 = random.randint(1, 10)
        team2_tier2 = random.randint(0, 10)
        team2_tier3 = random.randint(0, 10)

        team1 = gen_rand_team(TEAM1,
                              team1_tier1,
                              team1_tier2,
                              team1_tier3,
                              team1_keys)
        team2 = gen_rand_team(TEAM2,
                              team2_tier1,
                              team2_tier2,
                              team2_tier3,
                              team2_keys)

        team1_health = total_health_of_team(team1)
        team2_health = total_health_of_team(team2)


        p1, p2 = heuristic1(team1, team2)
        p3, p4 = heuristic2(team1, team2)
        result1, result2 = battle(team1, team2, (p1, p2), debug=False) # Only show one battle every 100 battles

        fh1 = result1/team1_health
        fh2 = result2/team2_health

        heuristic_1_error = abs(fh1-p1) + abs(fh2-p2)
        heuristic_2_error = abs(fh1-p3) + abs(fh2-p4)

        total_error_heuristic_1 += heuristic_1_error
        total_error_heuristic_2 += heuristic_2_error
        
        if heuristic_1_error < heuristic_2_error:
            win1 += 1
        elif heuristic_2_error < heuristic_1_error:
            win2 += 1
        else:
            ties += 1
        
    print(colored(f'Heuristic 1 wins: {win1:<5}', "red"))
    print(colored(f'Heuristic 2 wins: {win2:<5}', "blue"))
    print(colored(f'Ties: {ties:<5}', "cyan"))
    print()

    print(colored(f'Heuristic 1 Average Total Error: {total_error_heuristic_1 / (2*NUM_BATTLES):.4f}', "green"))
    print(colored(f'Heuristic 2 Average Total Error: {total_error_heuristic_2 / (2*NUM_BATTLES):.4f}', "green"))

    return total_error_heuristic_2 / (2*NUM_BATTLES)

def test_winrate(heuristic):
     # Number of battles to simulate.
    NUM_BATTLES = 1000
    finalhealth1 = []
    finalhealth2 = []
    error1 = []
    error2 = []
    preds1 = []
    preds2 = []
    winner = []

    ################################################
    # Use these to configure team composition

    team1_keys = {}
    team2_keys = {}

    TEAM1 = "red"
    TEAM2 = "blue"
    #################################################
    
    total_error_heuristic_1 = 0
    total_error_heuristic_2 = 0
    heuristic_score = [0, 0]
    wins = 0
    score_off, count = 0, 0

    for i in range(NUM_BATTLES):

        team1 = gen_rand_team(TEAM1, random.randint(1,10), random.randint(0,10), random.randint(0,10))
        team2 = gen_rand_team(TEAM2, random.randint(1,10), random.randint(0,10), random.randint(0,10))

        team1_health = total_health_of_team(team1)
        team2_health = total_health_of_team(team2)


        p1, p2 = heuristic(team1, team2)
        result1, result2 = battle(team1, team2, (p1, p2), debug=False) # Only show one battle every 100 battles

        fh1 = result1/team1_health
        fh2 = result2/team2_health

        heuristic_1_error = abs(fh1-p1) + abs(fh2-p2)

        total_error_heuristic_1 += heuristic_1_error
        
        if (p1 == 0 and result1 == 0) or (p2 == 0 and result2 == 0):
            wins += 1
            score_off += abs(fh1 - p1) + abs(fh2 - p2)
            count += 1

        


    print(colored(f'Heuristic Winrate: {wins / NUM_BATTLES:.2%}', "red"))
    print(colored(f'Heuristic Loss Off: {score_off / (1 if not count else count):.2f}', "blue"))
    print()

    print(colored(f'Heuristic 1 Average Total Error: {total_error_heuristic_1 / (2*NUM_BATTLES):.4f}', "green"))
    
    return total_error_heuristic_1 / (2*NUM_BATTLES)

import heuristics

#main()
heuristic_faceoff(heuristics.zero_guesser, heuristics.complex_health_heuristic)

#test_winrate(heuristics.complex_health_heuristic)

# Testing for best heuristic operation
# lowest_heuristic = []
# lowest_loss = math.inf
# operators = ["+","*","**"]
# testing_heuristic = None
# for i in range(1000):

#     if testing_heuristic == None:
#         heuristic = []
#         for _ in range(3):
#             operator = random.choice(operators)

#             if operator in "+*": heuristic.append([random.randint(1,1000000000000)/100, operator])
#             elif operator == "**": heuristic.append([random.randint(1, 150)/100, operator])
#     else:
#         heuristic = testing_heuristic[:]

#     loss = heuristic_faceoff(heuristics.zero_guesser, heuristics.complex_health_heuristic, heuristic)

#     if loss < lowest_loss and testing_heuristic == None:
#         testing_heuristic = heuristic
#     elif loss < lowest_loss * 1.1 and testing_heuristic != None:
#         lowest_loss = loss
#         lowest_heuristic = heuristic
#         testing_heuristic = None
#     else:
#         testing_heuristic = None
        

#     print(f"ROUND {i} Lowest Loss {lowest_loss} Heuristic {lowest_heuristic}")