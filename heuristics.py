"""

THIS IS NOT THE WELL WRITTEN UP NOTE THAT IT AS THE TOP OF hw1_main.py
THIS IS JUST MY SEMI-RAMBLY THOUGHTS OF ME DURING DEVELOPMENT OF THESE HEURISTICS
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

Added a function to check how often a heuristic chooses the right answer and their health off when they do
Wanted this to split it into two different problems, one to guess who wins and the other to guess final health since they are independent
Here are the current scores of heuristics:
end_health_calculating_heuristic: 83%, 0.21 off health
basic_class_heuristic: 83%, 0.24 off health
zero_guesser: 100%, 0.43 off health

A couple interesting takeaways from this one:
 - as expected the new heuristic with extra calculations for end health guessed the same percentage but was slightly closer on health
 - zero_guesser always guessed someone would die so it gets 100%, but it also shows that on average for these battles with randomized teams
        that the average surviving health is 0.43, so it's often closer to 0 then not

Additional Goals:
 - Will Revisit the 75% against zero_guesser later
 - Now, want to test all the unit matchups and get to 95% right team guessrate
 - Get below 0.15 average health off

To do this I will be starting another file unit_tester.py
This file takes every single unit and fights it against every other unit
I'm testing to see how units of different tiers match against each other exactly
and how different classes match.

This is a more scientific way then the one off bouts I did of roughly each tier 3 class above

Here are the results:
      0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   
0:    53   48   35   66   65   24   13   13   68   56   22   2    1    3    4
1:    52   52   51   68   72   18   18   26   72   57   21   0    1    8    4
2:    64   48   46   77   80   24   10   23   81   71   35   0    0    4    4
3:    33   31   22   49   49   8    5    10   49   38   4    0    0    2    0
4:    34   27   19   50   50   11   6    7    50   38   4    0    0    2    0
5:    75   82   75   91   88   51   47   49   94   75   48   12   5    18   50
6:    87   81   89   94   93   52   48   65   94   88   73   2    5    20   52
7:    86   73   77   89   92   50   34   51   91   87   67   2    2    13   46
8:    31   27   18   50   49   5    5    8    48   32   0    0    0    1    0
9:    43   42   28   61   61   24   11   12   67   47   8    1    1    3    2
10:   77   78   64   95   95   51   26   32   99   91   51   18   3    13   51
11:   97   99   99   99   99   87   98   97   100  98   81   51   57   84   99
12:   98   98   99   99   99   94   94   97   99   98   96   42   51   84   98
13:   96   92   95   97   97   81   79   86   98   96   86   15   15   50   89
14:   96   95   96   99   99   49   48   53   100  97   48   1    1    10   48

For this the unit on the left side has these listed winrates against these types of units.
For instance Unit 0 has a 24% winrate against Unit 5 and 3% against Unit 13

This pointed out generally how strong the tier 3 snipers seems to be. I think it was discounted
before because it was slightly weaker against the testing unit the tier 1 fighter, but it actually has +15% on duels with the tier 3 wraith
Also I didn't realize how bad the tier 2 golems were? The only one they edge out is beating Tier 1 golems by 2 percent points.

Also created is a dictonary with all these matchups. This will be used in a future heuristic for matchup based fighting. 
For instance golems only really have a chance against other golems or brutes
Using this we can create rankings of total winning percentage points out of 1400 max score (-100 due excluding fights against self) with the ranking as followed:

1: 12 - 1302
2: 11 - 1300
3: 13 - 1129
4: 6 - 900
5: 14 - 896
6: 5 - 815
7: 7 - 813
8: 10 - 799
9: 2 - 527
10: 1 - 474
11: 0 - 424
12: 9 - 370
13: 3 - 258
14: 4 - 254
15: 8 - 233

Interestingly while 11 does not beat 12 in terms of total winrate it still beats 12 in a one to one matchup
This values were tested in 1 to 1 combat, with many to many combat the values get pushed to the extremes even more
We can use this as a base for a new 

We can use this matchup data above and use the rankings like piecewise tables from chess heuristics
What piecewise tables do in chess is they are quick lookup tables that tell you what the estimated value of a piece is
For instance a pawn is 1 while a queen could be 9. Knight is 3 and Rook is 5. This tells you relatively how much losing each piece would be worth
In this scenario its used for seeing how effective a unit is relative to another
The main problem is that it doesnt quite have the distance we need between values. 12 is not 6 times better then 8, its 100s of times better. For this we can square the piecewise values



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


piece_values = [424, 474, 527, 258, 254, 815, 900, 813, 233, 370, 799, 1300, 1302, 1129, 896]

def matchup_dependent_heuristic(team1, team2):
    """ A value has been assigned to every ID of actor """

    def fitness_actor(actr):
        return piece_values[actr.ID] ** 3

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