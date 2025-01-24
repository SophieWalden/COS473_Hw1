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

We can use this matchup data above and use the rankings like piecewise tables from chess heuristics
What piecewise tables do in chess is they are quick lookup tables that tell you what the estimated value of a piece is
For instance a pawn is 1 while a queen could be 9. Knight is 3 and Rook is 5. This tells you relatively how much losing each piece would be worth
In this scenario its used for seeing how effective a unit is relative to another
The main problem is that it doesnt quite have the distance we need between values. 12 is not 6 times better then 8, its 100s of times better. For this we can square the piecewise values

Just using the piecewise values above cubed gets us up a point or two to about 85% accuarcy in guessing.

Trying to implement the match data, just adding it on and multiplying our strength by it actually brings our average down a point or two.
It's either that the data is too closer together from 8 -> 12 or due to the possible amount of entities one good matchup doesn't influence strength as much
To combat this we can try taking the average of its strength of matchups since any of these matchups can be chosen

So far additionally our operation has just been whatever team has the highest strength is likely the winner.
We can create another heuristic alternative_strongest_chooser who has more factors then just which one has the highest value
actually whatever values we are getting from our strength functions we are just all multiplying so it should affect anyways
I think amount of actors on a team also influences the strength

Our winrate checker even over 1000 guesses has too much variability on random teams that makes the heuristics hard to compare
I think we should generate 1000 consistently same battles that have differing levels of variability to eliminate variables
There's still slight variabiltiy in how the matches play out but hopefully it will face the same 1000 matchups everytime

Somehow doing that brought my win guessrate down to 51% and the heuristic off to 0.35
I think this is due to really large team size and more varied units? Does it just become a coinflip at some point?

Okay, if we get it to work on these varied teams we should be able to apply it back to small teams aswell
So I'm hoping to get this up to ~60% as a start

At this point I'm going to assign "modifier strengths" to each three of our values to regulate them.
These will be low decimal values (>1.0) that the value is the exponent of that that we can use to slow the multiplying and apply at different strengths

To map this out I opened up desmos and started graphing out some of the potential values based on realistic outputs I'e seen from our values
For instance we can put 1.01^(len(actors)) as a good modifier since it shows that having +10 is only about a 50% increase in strength to combat having 40 Tier 1 fighters vs 1 Tier 3 wraith situation
I'm messing around with the values but still getting a ton of variability. I'm going to implement a way to pass in strengths for the values and mass try to see what provides good results
I'm going to run 1000 heuristics all at 1000 rounds each and choose the best one while I work on creating a visual format for watching these fights for better observations
After 1 million battles ran, the current best heuristics seem to be [[536501350.31, '+'], [9002206015.69, '*'], [4133157533.95, '*']]. This means it thought matchup and length were more important while units themselves didnt need to be multiplied
... and it infact made me worse against random_guesser, going back to 50-50% odds instead of 67-33 odds. Well atleast that example was explored
wait I accidentally removed a multiplcation symbol in my end evaluator ... another 1 million simulations to try I guess

basically what was happening was that for those a million it was evaluating strength purely based off of the length
I am still getting roughly 50% guessrate on these battles which is worrying though, maybe higher actor count battles are truly random

Finally we get [[4543695934.35, '+'], [1.02, '**'], [0.63, '**']] which shows that length needs to be tuned down, matchups a little up and strength
... and its still not useful. I think theres something wrong with my test_winrate its still only producing 50% with the new seeded battles

Also going back to testing why certain matchups are so imbalanced. Since wraith has high evasion against low acc on tier 2 golem the golem only can hit 1.4% of turns and even then the wraith has armor

"""

import random
def random_guesser(team1, team2):
    return (random.randint(1, 100)/100, random.randint(1, 100)/100)

def zero_guesser(team1, team2):
    return 0,0

def one_guesser(team1, team2):
    return 1,1


piecewise_values_attempt1 = [5,7,12, 7, 5,  10, 15,  20, 15, 10, 22.5,  75, 200, 75, 22.5 ]

def basic_class_heuristic(team1, team2):
    """ A value has been assigned to every ID of actor """

    def fitness_actor(actr):
        return piecewise_values_attempt1[actr.ID] 

    def fitness_team(team):
        return sum(fitness_actor(actor) for actor in team.actors)
    
    def fitness_outcome(team1, team2):
        team1_strength, team2_strength = fitness_team(team1), fitness_team(team2)


        outputs = team1_strength/(team1_strength+team2_strength), team2_strength/(team1_strength+team2_strength)
        if team1_strength > team2_strength: team2_strength = 0
        else: team1_strength = 0
        
        return outputs[0] if team1_strength else team1_strength, outputs[1] if team2_strength else team2_strength


    return fitness_outcome(team1, team2)

def end_health_calculating_heuristic(team1, team2):
    """ A value has been assigned to every ID of actor """ 

    def fitness_actor(actr):
        return piecewise_values_attempt1[actr.ID] 

    def fitness_team(team):
        return sum(fitness_actor(actor) for actor in team.actors)
    
    def unit_end_health(actr):
        tier = actr.ID // 5
        return tier
    
    def fitness_outcome(team1, team2):
        team1_strength, team2_strength = fitness_team(team1), fitness_team(team2)


        outputs = [team1_strength/(team1_strength+team2_strength), team2_strength/(team1_strength+team2_strength)]
        health = [0, 0]
        for actr in team1.actors:
            health[0] += 6 - unit_end_health(actr) * 2
        for actr in team2.actors:
            health[1] += 6 - unit_end_health(actr) * 2

        if team1_strength > team2_strength: 
            team2_strength = 0
            outputs[0] = health[0]/sum(health)
        else: 
            team1_strength = 0
            outputs[1] = health[1]/sum(health)
        
        return outputs[0] if team1_strength else team1_strength, outputs[1] if team2_strength else team2_strength


    return fitness_outcome(team1, team2)


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

def matchup_dependent_heuristic(team1, team2):
    """ A value has been assigned to every ID of actor """

    def fitness_actor(actr):
        return piece_values_attempt2[actr.ID] ** 3

    def fitness_team(team):
        return sum(fitness_actor(actor) for actor in team.actors)
    
    def unit_end_health(actr):
        tier = actr.ID // 5
        return tier
    
    def get_matchup_strength(team, opp):
        val = 0

        for actor in team.actors:
            for opp_actor in opp.actors:
                val += matchup_stats[actor.ID][opp_actor.ID]

        return val / (len(team.actors) * len(opp.actors))
    
    def fitness_outcome(team1, team2):
        # Call functions to detemine team strength, matchup, and size
        team1_strength, team2_strength = fitness_team(team1), fitness_team(team2)
        team1_matchup_strength, team2_matchup_strength = get_matchup_strength(team1, team2), get_matchup_strength(team2, team1)
        team1_size, team2_size = len(team1.actors), len(team2.actors)


        # Equations in how to factor each of these values
        team_values = [[team1_strength, team1_matchup_strength, team1_size], [team2_strength, team2_matchup_strength, team2_size]]

        value_strengths = [[1, '*'], [1, '*'], [1.01, '**']]

        # Totalling the Values
        total_team_strengths = [1.0, 1.0]
        for i in range(2):
            for value, strength in zip(team_values[i], value_strengths):
                equation = "".join(map(str, strength + [value]))
                
                try: 
                    result = eval(equation)
                except Exception:
                    result = value

                total_team_strengths[i] *= result
        
        # Calculating likely health left due to low actor quality
        health = [0, 0]
        health_remaining = [0, 0]
        for actr in team1.actors:
            health[0] += 6 - unit_end_health(actr) * 2
        for actr in team2.actors:
            health[1] += 6 - unit_end_health(actr) * 2



        if total_team_strengths[0] > total_team_strengths[1]: 
            health_remaining[0] = health[0]/sum(health)
        else: 
            health_remaining[1] = health[1]/sum(health)
    

        return health_remaining[0], health_remaining[1] 


    return fitness_outcome(team1, team2)