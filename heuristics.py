"""

THIS IS NOT THE WELL WRITTEN UP NOTE THAT IT AS THE TOP OF hw1_main.py
THIS IS THE RAMBLY THOUGHTS OF ME DURIGN DEVELOPMENT OF THESE HEURISTICS
HERE SO YOU CAN SEE THE THOUGH PROCESS BEHIND ALL CHANGES

KEY:
In these notes I'll refer to units by tiers and class instead of ID name for clarity.

0, 5, and 10 are Fighters
1, 6, and 11 are Snipers
2, 7, and 12 are Wraiths
3, 8, and 13 are Golems
4, 9, and 14 are Brutes

Ex: 5 is a Tier 2 Fighter. 12 is a Tier 3 Wraith

Notes:

Since one team is guranteed to die by the time a fight is over
The only way to beat a heuristic that always guesses 0, 0
is to create one that can guess with less error then the remaining teams health percentage

For instance if the battles are consistently ending with a team 30-40% health then average errors needs to be <0.4
the zero guesser does worse the more unbalanced the teams are and very well when there is close matches
Creating a heuristic that can guess both when unbalanced and balanced may combat it

You can guess a score like (0.1, 0.1) if you are unlikely which side is going to win and you think
that the bounding box between one team is another (ex: 0.1 on the deadteam is less then zero guesser for 0.01 -> 0.19 for alive team)

First goal: Beat zero-guesser 75% of the time
How do we do this?

If we take a total sum of the stats of the team we get ~55% - 45% on the zero guesser.
Next step is taking into effect both team size and maybe tier quality of unit
Certain tier units last much longer and can take on multiple lower tiers

The rough power scaling is:
Tier 2 unit = ~1.8 Tier 1s
Tier 3 unit = ~4 Tier 2s or ~8.5 Tier 1s

The basic noting is that most Tier 2 units are mid powered, but Tier 3 units specifically dominate

A breakdown of how many Tier 1s can a Tier 3 beat up on average:
Fighter: 2.5 Tier 1s
Sniper: 15 Tier 1s
Wraith: 40 Tier 1s
Golem: 15 Tier 1s
Brute: 4.5 Tier 1s

Clear outlier here is the wraith is really broken along with the sniper and golem being good.
Fighter has too low of an acc to kill that many and gets bogged down
and Brute doesn't do enough damage

Good note here is that the same actor defends attacks, so having a brute tank doesn't matter since he wont kill
But having a fighter attack is good since theres a chance he one shots the Wraith the strongest enemy
Still not much of an increase, just that fighters are better against higher tiers

Doing a class based determiner gets us a couple points up to 57-58%

is there benefits to team combinations? Like one tier 3 fighter could take out tier 3 wraith and let tier 1 fighters run amuck but they still weak?
The main problem is them attacking all at the same time

Theres not a complete correlation between unit strenght and team health.
Since 100 Tier 1s could die and then the tier3 wraith could sweep 40 Tier 1s in a row
We can calculate who will win through team strength, but how much health they lose is through tier unit difference?
Like more lower tiers compared to oponent = more lost health

Using our first calc for strength and second for health based off of amount of low tiers we get to 63% above 0 guessers

--------------- RANDOM GUESSER BREAK ---------------

At this point the heuristic beats the random guesser 90% with an average error of 14% or 0.14 
With one team being 0 that means with two teams it is on average 0.28 off the correct health
So basically either we are having bad winning evals or our health can stand to gain up to another 28 points of accuarcy

Also while our original just strength eval had an average error of 0.4 in the main evaluator this new one is down to 0.2

-------------- RANDOM GUESSER BREAK OVER -----------

Messing around with the values, if you assign a bigger differential to tier 1 units as opposed to tier 3 we increase to 65%
Interesting to note here though that our average total error isnt going down with our wins going up
This is likely to say that we are just barely beating the zero guesser OR we improved on a ton of scenarios and lost accuarcy hard on a few


"""

import random
def random_guesser(team1, team2):
    return (random.randint(1, 100)/100, random.randint(1, 100)/100)

def zero_guesser(team1, team2):
    return 0,0

def one_guesser(team1, team2):
    return 1,1


def basic_class_heuristic(team1, team2):
    """ A value has been assigned to every ID of actor """

    values = [
        5,
        7,
        12,
        7,
        5,
        10,
        15,
        20,
        15,
        10,
        22.5,
        75,
        200,
        75,
        22.5
    ]

    def fitness_actor(actr):
        return values[actr.ID] 

    def fitness_team(team):
        return sum(fitness_actor(actor) for actor in team.actors)
    
    def fitness_outcome(team1, team2):
        a1, a2 = fitness_team(team1), fitness_team(team2)


        outputs = a1/(a1+a2), a2/(a1+a2)
        if a1 > a2: a2 = 0
        else: a1 = 0
        
        return outputs[0] if a1 else a1, outputs[1] if a2 else a2


    return fitness_outcome(team1, team2)

def end_health_calculating_heuristic(team1, team2):
    """ A value has been assigned to every ID of actor """

    values = [
        5,
        7,
        12,
        7,
        5,
        10,
        15,
        20,
        15,
        10,
        22.5,
        75,
        200,
        75,
        22.5
    ]

    def fitness_actor(actr):
        return values[actr.ID] 

    def fitness_team(team):
        return sum(fitness_actor(actor) for actor in team.actors)
    
    def unit_end_health(actr):
        tier = actr.ID // 5
        return tier
    
    def fitness_outcome(team1, team2):
        a1, a2 = fitness_team(team1), fitness_team(team2)


        outputs = [a1/(a1+a2), a2/(a1+a2)]
        health = [0, 0]
        for actr in team1.actors:
            health[0] += 6 - unit_end_health(actr) * 2
        for actr in team2.actors:
            health[1] += 6 - unit_end_health(actr) * 2

        if a1 > a2: 
            a2 = 0
            outputs[0] = health[0]/sum(health) 
        else: 
            a1 = 0
            outputs[1] = health[1]/sum(health)
        
        return outputs[0] if a1 else a1, outputs[1] if a2 else a2


    return fitness_outcome(team1, team2)