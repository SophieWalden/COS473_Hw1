import random
import math
import matplotlib.pyplot as plt

# Setting to True will cause the simulator to
# throw out a lot of additional text. Not all
# of it helpful.
DEBUG = False


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
                 spot):
        self.ID = ID            # Which unit_templates
        self.data = data        # Unit stats (list)
        self.team_name = team_name  # name of the team
        self.spot = spot            # spot in the team

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

    def is_alive(self):
        return self.get_health() > 0

# Generates a randomized team using the
# various tier composition values.
# Each tier corresponds to five unit_templates
# the keys list can be used to specify types
# exactly.
def gen_rand_team(team_name,
                  tier0=0,
                  tier1=0,
                  tier2=0,
                  keys={}):
    team = []
    for key, amt in keys.items():
        for i in range(amt):
            stats = unit_templates[key][:]
            actor = Actor(key, stats, team_name, i)
            team.append(actor)
    for i in range(tier0):
        key = random.randrange(0,5)
        stats = unit_templates[key][:]
        actor = Actor(key, stats, team_name, i)
        team.append(actor)
    for i in range(tier1):
        key = random.randrange(0,5)+5
        stats = unit_templates[key][:]
        actor = Actor(key, stats, team_name, i)
        team.append(actor)
    for i in range(tier2):
        key = random.randrange(0,5)+10
        stats = unit_templates[key][:]
        actor = Actor(key, stats, team_name, i)
        team.append(actor)
    return team

def total_health_of_team(team):
    health = 0
    for actor in team:
        health += actor.get_health()
    return health

def print_team_composition(team_name, team):
    output(f"Team {team_name}")
    types = {}
    for actor in team:
        if actor.get_ID() not in types:
            types[actor.get_ID()] = 1
        else:
            types[actor.get_ID()] += 1
    for i,amt in types.items():
        output(f"Type {i}: {amt}")
    output("")

# Runs a combat round between two units.
# Each unit has a chance to attack and defend
# unless the first disables the second before
# it has a chance to go.
def combat(first, second):

    att1 = first.make_accuracy()
    def2 = second.make_evasion()
    if att1 > def2:
        dmg1 = first.make_damage()
        dmg1 = second.make_defense(dmg1)
        output(f"{first.get_team_name()}:{first.get_spot()} damaged {second.get_team_name()}:{second.get_spot()} for {dmg1}.")

    if second.is_alive():
        att2 = second.make_accuracy()
        def1 = first.make_evasion()
        if att2 > def1:
            dmg2 = second.make_damage()
            dmg2 = first.make_defense(dmg2)
            output(f"{second.get_team_name()}:{second.get_spot()} damaged {first.get_team_name()}:{first.get_spot()} for {dmg2}.")

# Runs an entire battle between two teams
# Battle ends when one team loses all its
# units.
def battle(teamA, teamB):

    round = 1
    while len(teamA) > 0 and len(teamB) > 0:
        output(f"ROUND {round}")
        output(f"Team 1: {len(teamA)} - Team 2: {len(teamB)}")
        aI = random.randrange(len(teamA))
        bI = random.randrange(len(teamB))
        actorA = teamA[aI]
        actorB = teamB[bI]

        if random.random() < 0.5:
            combat(actorA, actorB)
        else:
            combat(actorB, actorA)

        if not actorA.is_alive():
            output(f"Team 1 - Actor {actorA.get_spot()} died.")
            teamA.pop(aI)
        if not actorB.is_alive():
            output(f"Team 2 - Actor {actorB.get_spot()} died.")
            teamB.pop(bI)

        round += 1

    if len(teamA) == 0 or len(teamB) == 0:
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


piece_values_attempt2 = [424, 474, 527, 258, 254, 815, 900, 813, 233, 370, 799, 1300, 1302, 1129, 896]
matchup_stats = {0: {0: 53.3, 1: 48.0, 2: 35.8, 3: 66.8, 4: 65.1, 5: 24.1, 6: 13.0, 7: 13.3, 8: 68.1, 9: 56.3, 10: 22.4, 11: 2.1, 12: 1.8, 13: 3.8, 14: 4.0},
1: {0: 52.0, 1: 52.4, 2: 51.7, 3: 68.4, 4: 72.7, 5: 18.0, 6: 18.3, 7: 27, 8: 72.7, 9: 57.3, 10: 21.8, 11: 0.5, 12: 1.8, 13: 8.0, 14: 4.2},
2: {0: 64.2, 1: 48.3, 2: 46.0, 3: 77.6, 4: 80.7, 5: 24.2, 6: 10.8, 7: 23.0, 8: 81.4, 9: 71.9, 10: 36, 11: 0.5, 12: 0.3, 13: 4.2, 14: 4.0},
3: {0: 33.2, 1: 31.6, 2: 22.5, 3: 49.7, 4: 49.9, 5: 8.5, 6: 5.3, 7: 10.9, 8: 49.5, 9: 38.9, 10: 4.1, 11: 0.6, 12: 0.4, 13: 2.4, 14: 0.4},
4: {0: 34.9, 1: 27.3, 2: 19.3, 3: 50.1, 4: 50.2, 5: 11.8, 6: 6.2, 7: 7.6, 8: 50.2, 9: 38.6, 10: 4.5, 11: 0.4, 12: 0.5, 13: 2.4, 14: 0.4},
5: {0: 75.9, 1: 82.0, 2: 75.8, 3: 91.5, 4: 88.2, 5: 51.3, 6: 47.4, 7: 49.9, 8: 94.3, 9: 75.6, 10: 48.2, 11: 12.1, 12: 5.7, 13: 18.7, 14: 50.1},
6: {0: 87.0, 1: 81.7, 2: 89.2, 3: 94.7, 4: 93.8, 5: 52.6, 6: 48.4, 7: 65.4, 8: 94.1, 9: 88.6, 10: 73.4, 11: 2.0, 12: 5.2, 13: 20.8, 14: 52.0},
7: {0: 86.7, 1: 73.1, 2: 77.0, 3: 89.9, 4: 92.4, 5: 50.1, 6: 34.6, 7: 51.6, 8: 91.5, 9: 87.1, 10: 67.2, 11: 2.4, 12: 2.1, 13: 13.2, 14: 46.4},
8: {0: 31.9, 1: 27.3, 2: 18.6, 3: 50.5, 4: 49.8, 5: 5.7, 6: 5.9, 7: 8.5, 8: 48.4, 9: 32.7, 10: 0.7, 11: 0.0, 12: 0.3, 13: 1.2, 14: 0.0},        
9: {0: 43.7, 1: 42.7, 2: 28.1, 3: 61.1, 4: 61.4, 5: 24.4, 6: 11.4, 7: 12.9, 8: 67.3, 9: 47.7, 10: 8.8, 11: 1.6, 12: 1.2, 13: 3.4, 14: 2.9},
10: {0: 77.6, 1: 78.2, 2: 64.1, 3: 95.9, 4: 95.5, 5: 51.8, 6: 26.6, 7: 32.8, 8: 99.3, 9: 91.2, 10: 51.6, 11: 18.2, 12: 3.3, 13: 13.5, 14: 51.9},
11: {0: 97.9, 1: 99.5, 2: 99.5, 3: 99.4, 4: 99.6, 5: 87.9, 6: 98.0, 7: 97.6, 8: 100.0, 9: 98.4, 10: 81.8, 11: 51.1, 12: 57.4, 13: 84.1, 14: 99.0},
12: {0: 98.2, 1: 98.2, 2: 99.7, 3: 99.6, 4: 99.5, 5: 94.3, 6: 94.8, 7: 97.9, 8: 99.7, 9: 98.8, 10: 96.7, 11: 42.6, 12: 51.4, 13: 84.6, 14: 98.4},
13: {0: 96.3, 1: 92.0, 2: 95.8, 3: 97.6, 4: 97.6, 5: 81.3, 6: 79.2, 7: 86.8, 8: 98.8, 9: 96.6, 10: 86.5, 11: 15.9, 12: 15.4, 13: 50.9, 14: 89.7},
14: {0: 96.0, 1: 95.8, 2: 96.0, 3: 99.6, 4: 99.6, 5: 49.9, 6: 48.0, 7: 53.6, 8: 100.0, 9: 97.1, 10: 48.1, 11: 1.0, 12: 1.6, 13: 10.3, 14: 48.9}}

def fitness_actor(actr):
    return piece_values_attempt2[actr.ID] ** 4

def fitness_team(team):
    return sum(fitness_actor(actor) for actor in team)


def get_matchup_strength(team, opp):
    val = 0

    for actor in team:
        for opp_actor in opp:
            val += matchup_stats[actor.ID][opp_actor.ID]

    return val / (len(team) * len(opp))

def get_team_strengths(strengthA, strengthB, matchupsA, matchupsB):
    return [strengthA * matchupsA, strengthB * matchupsB]

def fitness_outcome(team1, team2):
    # Call functions to detemine team strength, matchup, and size
    team1_strength, team2_strength = fitness_team(team1), fitness_team(team2)
    team1_matchup_strength, team2_matchup_strength = get_matchup_strength(team1, team2), get_matchup_strength(team2, team1)
    team1_size, team2_size = len(team1), len(team2)


    # Equations in how to factor each of these values
    total_team_strengths = get_team_strengths(team1_strength, team2_strength, team1_matchup_strength, team2_matchup_strength)

    unbalanced_rating = (max(total_team_strengths)/min(total_team_strengths)) // 2.1
    winner_index = int(total_team_strengths[1] > total_team_strengths[0])
    

    # remaining health is calculated by factoring in unit defense and how unbalanced the match was
    health_remaining = [0, 0]
    remaining_health = 0
    health_left_by_defense = {5: [0, 1], 10: [0.1,0.5], 20: [0.1, 0.7], 30: [0.25, 0.8], 40: [0.5, 0.9]}
    
    for i, actor in enumerate(team1):
        health_range = health_left_by_defense[actor.get_armor()]
        remaining_health += ((health_range[1]-health_range[0]) * (min(1, unbalanced_rating / 3.0)))+health_range[0]
    
    remaining_health = remaining_health / len(team1)
    health_remaining[winner_index] = remaining_health

    if unbalanced_rating == 0: 
        health_remaining = [0,0]
        health_remaining[winner_index] = 0.01

    return health_remaining[0], health_remaining[1] 



# #####################################################################
# #####################################################################
# #####################################################################
def main():

    # Number of battles to simulate.
    NUM_BATTLES = 1000
    finalhealth1 = []
    finalhealth2 = []
    error1 = []
    error2 = []
    preds1 = []
    preds2 = []
    winner = []

   
    
    for i in range(NUM_BATTLES):
         ################################################
        # Use these to configure team composition
        team1_tier0 = random.randint(1, 10)
        team1_tier1 = random.randint(0, 10)
        team1_tier2 = random.randint(0, 10)
        team1_keys = {}
        
        team2_tier0 = random.randint(1, 10)
        team2_tier1 = random.randint(0, 10)
        team2_tier2 = random.randint(0, 10)
        team2_keys = {}
        #################################################

        team1 = gen_rand_team("1",
                              team1_tier0,
                              team1_tier1,
                              team1_tier2,
                              team1_keys)
        team2 = gen_rand_team("2",
                              team2_tier0,
                              team2_tier1,
                              team2_tier2,
                              team2_keys)

        team1_health = total_health_of_team(team1)
        team2_health = total_health_of_team(team2)

        print_team_composition("1", team1)
        print_team_composition("2", team2)

        p1, p2 = fitness_outcome(team1, team2)
        print(f"Prediction: {p1} {p2}")
        preds1.append(p1)
        preds2.append(p2)
        result1, result2 = battle(team1, team2)
        fh1 = result1/team1_health
        fh2 = result2/team2_health
        finalhealth1.append(fh1)
        finalhealth2.append(fh2)
        error1.append(abs(fh1-p1))
        error2.append(abs(fh2-p2))
        if result1 > result2:
            winner.append(1)
        elif result2 > result1:
            winner.append(2)
        else:
            winner.append(0)
            print("ERROR: TIE")

    win1 = winner.count(1)
    win2 = winner.count(2)
    print(f"Team 1 wins: {win1:<5} - Avg Error: {sum(error1)/NUM_BATTLES:.3f}")
    print(f"Team 2 wins: {win2:<5} - Avg Error: {sum(error2)/NUM_BATTLES:.3f}")

    fig, axs = plt.subplots(2)
    axs[0].set_title("Team 1")
    axs[1].set_title("Team 2")
    axs[0].plot(range(NUM_BATTLES), error1, label="Team 1 Prediction Error")
    axs[1].plot(range(NUM_BATTLES), error2, label="Team 2 Prediction Error")
    for ax in axs.flat:
        ax.set(xlabel='Battle', ylabel='Error')
        ax.label_outer()
    plt.show()

main()
