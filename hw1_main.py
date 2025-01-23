import random
import math
import matplotlib.pyplot as plt

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
def fitness_actor(actr):
    return sum(actr.data)

# This should return the fitness of an entire team. Similarly to them
# unit fitness function, you are free to return one or more values.
# And use those values in any way you choose.
def fitness_team(team):
    return sum(fitness_actor(actor) for actor in team)

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
    NUM_BATTLES = 100
    finalhealth1 = []
    finalhealth2 = []
    error1 = []
    error2 = []
    preds1 = []
    preds2 = []
    winner = []

    ################################################
    # Use these to configure team composition
    team1_tier0 = 10
    team1_tier1 = 10
    team1_tier2 = 10
    team1_keys = {}
    
    team2_tier0 = 10
    team2_tier1 = 10
    team2_tier2 = 10
    team2_keys = {}
    #################################################
    
    for i in range(NUM_BATTLES):
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
