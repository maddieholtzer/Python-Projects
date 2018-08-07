from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    roll_sum = 0 # sums values of rolled dice
    ones_total = 0 # counts number of times the value 1 is rolled
    while num_rolls>0:
        current_roll = dice()
        if current_roll==1:
            ones_total += 1
        roll_sum += current_roll
        num_rolls -= 1
    if ones_total > 0:
        return ones_total
    else:
        return roll_sum
    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    a, b = opponent_score % 10, opponent_score // 10 # separation into digits
    return (max(a, b) + 1)
    # END PROBLEM 2


# Write your prime functions here!

def is_prime(turn_score): # detect prime number
    counterA = 2
    if(turn_score == 1): # 1 is not prime
        return False
    while(counterA <= (turn_score/2)):
        if(turn_score % counterA == 0):
            return False
        counterA += 1
    return True

def next_prime(turn_score): # move to next prime number
    the_next_prime = turn_score + 2
    if(turn_score == 2):
        return 3
    while (the_next_prime<25):
        if(is_prime(the_next_prime) == True):
            return the_next_prime
        the_next_prime+=2


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime and When Pigs Fly rules.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    score = 0
    # free bacon rule implementation
    if num_rolls == 0:
        score = free_bacon(opponent_score)
    else:
        score = roll_dice(num_rolls, dice)
    # hogtimus prime rule implementation
    if score == 19:
        score = 23
    if score == 17:
        score = 19
    if score == 13:
        score = 17
    if score == 11:
        score = 13
    if score == 7:
        score = 11
    if score == 5:
        score = 7
    if score == 3:
        score = 5
    if score == 2:
        score = 3
    # when pigs fly rule implementation
    if score > 25 - num_rolls:
        score = 25
        score -= num_rolls
    return score

    # END PROBLEM 2


def reroll(dice):
    """Return dice that return even outcomes and re-roll odd outcomes of DICE."""
    def rerolled():
        # BEGIN PROBLEM 3
        this_roll = dice()
        if this_roll % 2 != 0:
            return dice()
        else:
            return this_roll
        # END PROBLEM 3
    return rerolled


def select_dice(score, opponent_score, dice_swapped):
    """Return the dice used for a turn, which may be re-rolled (Hog Wild) and/or
    swapped for four-sided dice (Pork Chop).

    DICE_SWAPPED is True if and only if four-sided dice are being used.
    """
    # BEGIN PROBLEM 4
    dice = six_sided
    if dice_swapped == True:
        dice = four_sided
    # END PROBLEM 3
    if (score + opponent_score) % 7 == 0:
        dice = reroll(dice)
    return dice



def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    dice_swapped = False  # Whether 4-sided dice have been swapped for 6-sided
    my_score = score0
    opponent_score = score1
    while(score0<goal and score1<goal): # 'While' loop that ends when game ends
        if(player == 0): # If it is Player0's turn...
            num_rolls = strategy0(my_score,opponent_score) # strategy for Player0 implemented
            if num_rolls == -1 and dice_swapped == False: # if strategy is Pork Chop, and current die is six sided
                my_score+=1
                dice_swapped = True
            elif num_rolls == -1 and dice_swapped == True: # if strategy is Pork Chop, and current die is four sided
                my_score+=1
                dice_swapped = False
            else: #if strategy is not Pork Chop
                dice = select_dice(my_score, opponent_score, dice_swapped)
                my_score += take_turn(num_rolls, opponent_score, dice)
            player = other(player)
        else: # If it is Player1's turn...
            num_rolls = strategy1(opponent_score,my_score)
            if num_rolls == -1 and dice_swapped == False:
                opponent_score+=1
                dice_swapped = True
            elif num_rolls == -1 and dice_swapped == True:
                opponent_score+=1
                dice_swapped = False
            else:
                dice = select_dice(opponent_score, my_score, dice_swapped)
                opponent_score = opponent_score + take_turn(strategy1(opponent_score, my_score), my_score, dice)
            player = other(player)
        if(my_score*2 == opponent_score or opponent_score*2 == my_score): #Swine Swap implementation via placeholders
            zerocounter = my_score
            onecounter = opponent_score
            score0 = onecounter
            my_score = onecounter
            score1  = zerocounter
            opponent_score = zerocounter
        else: #Final reassignments to original score variables before return statement
            score0 = my_score
            score1 = opponent_score
# END PROBLEM 5
    return score0, score1

#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert -1 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy returns an invalid
    output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    score = 0
    opponent_score = 0
    while(score<goal):
        opponent_score=0
        while(opponent_score<goal):
            check_strategy_roll(score,opponent_score,strategy(score,opponent_score))
            opponent_score = opponent_score+1
        score+=1
    # END PROBLEM 6


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    # BEGIN PROBLEM 7
    def average_function(*args):
        counter = 0
        result = 0
        while(counter<num_samples):
            result_holder = fn(*args)
            result+= result_holder
            counter+=1
        return result/num_samples
    return average_function
    # END PROBLEM 7


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8

    """maxi, number_of_dice, ret = 0, 10, 0
    while number_of_dice > 0:
        avg = make_averaged(roll_dice)(number_of_dice, dice)
        maxi = max(maxi, avg)
        if avg >= maxi:
            ret = number_of_dice
        number_of_dice -= 1
    return ret"""



    counterA = 1
    num_rolls=1
    max_value = 0
    best_num_rolls = 0
    while counterA <= 10:
        num_rolls = counterA
        average_function = make_averaged(roll_dice)(counterA, dice)
        if average_function > max_value:
            max_value = average_function
            best_num_rolls = counterA
        counterA +=1
    return best_num_rolls

    """counterA = 1
    maxvalue = 0
    maxvaluenumber = 0
    while(counterA<=10):
        num_rolls = counterA
        average_for_roll = make_averaged(roll_dice(num_rolls, dice), num_samples)
        counterB = average_for_roll(roll_dice(counterA, dice))
        if(counterB>maxvalue):
            maxvalue = counterB
            maxvaluenumber = counterA
        counterA +=1
    return maxvaluenumber"""
    # END PROBLEM 8


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        rerolled_max = max_scoring_num_rolls(reroll(six_sided))
        print('Max scoring num rolls for re-rolled dice:', rerolled_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9
    counter = 0
    counter = free_bacon(opponent_score)
    if(is_prime(counter) == True):
        newscore = next_prime(counter)
        counter += (newscore - counter)
    if(counter>= margin):
        return 0
    else:
        return num_rolls
    # END PROBLEM 9
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    scorecounter = free_bacon(opponent_score)
    if(is_prime(scorecounter) == True):
        newscore = next_prime(scorecounter)
        scorecounter = newscore
    if(scorecounter*2 == opponent_score):
        return 0
    if(opponent_score*2 == scorecounter):
        return num_rolls
    if(bacon_strategy(score, opponent_score, margin, num_rolls) == 0):
        return 0
    return num_rolls
    # END PROBLEM 10
check_strategy(swap_strategy)


def final_strategy(score, opponent_score):
    """
    *** Immediately implement Pork Chop. This handicaps the opponent who must always
        roll 4 dice, because there is an increased chance of their rolling a 1 (and
        therefore triggering Pig Out) while using a 4-sided die compared to when using
        a 6-sided-die.

        Implement swap strategy thereafter, with a lower margin and lower number of rolls.
        The lower margin will give the swap strategy more frequent implementation.
        The lower number of rolls decreases the chances of rolling a 1. ***
    """
    # BEGIN PROBLEM 11
    if(score == 0):
        return -1
    return swap_strategy(score, opponent_score, 6, 3)
    # END PROBLEM 11
check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()

