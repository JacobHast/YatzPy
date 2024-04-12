# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 11:53:31 2022

@author: Jacob
"""

import numpy as np
import dice
import scoreboard
import training
import scoring
import matplotlib.pyplot as plt
import time


def play_game(BOARD_EV, NUM_DICE, NUM_CATEGORIES):
    NUM_ROLLS = 3
    ALL_OUTCOMES = dice.all_outcomes(NUM_DICE)
    SCORE_LISTS = [
        [
            scoring.calculate_score(outcome, category)
            for category in range(NUM_CATEGORIES)
        ]
        for outcome in ALL_OUTCOMES
    ]
    ALL_OUTCOME_PROBS = np.array([outcome.probability() for outcome in ALL_OUTCOMES])
    M_REROLL_LIST = dice.get_reroll_matrices(NUM_DICE)
    score = 0
    board = scoreboard.Scoreboard(np.ones(NUM_CATEGORIES), bonussum=0)
    got_bonus = False
    got_yatzy = False
    for turn in range(15):
        # print(f"turn: {turn + 1}")
        current_dice = dice.random(NUM_DICE)
        for rolls_remaining in range(NUM_ROLLS - 1, 0, -1):
            # print(board)
            _, dice_keep = training.best_roll(
                ALL_OUTCOMES,
                ALL_OUTCOME_PROBS,
                board,
                BOARD_EV,
                SCORE_LISTS,
                M_REROLL_LIST,
                rolls_remaining,
                current_dice,
            )
            kept_dice = dice_keep[0]
            remaining_dice = NUM_DICE - kept_dice.num_dice
            current_dice = kept_dice + dice.random(remaining_dice)

        _, categories = training.best_score(
            current_dice, board, BOARD_EV, SCORE_LISTS, return_priority=True
        )
        category_points = SCORE_LISTS[current_dice.index][categories[0]]
        board.fill_category(categories[0], category_points)
        score += category_points
        if categories[0] == 14:
            if category_points != 0:
                got_yatzy = True
    if board.bonussum == "bonus":
        score += 50
        got_bonus = True

    return score, got_yatzy, got_bonus
    # print(board)


NUM_GAMES = 100
NUM_DICE = 5
NUM_CATEGORIES = 15

use_bonus = True
if use_bonus:
    filename = "expected_values/EV_bonus.npy"
else:
    filename = f"expected_values/EV_nobonus.npy"
BOARD_EV = np.load(filename, allow_pickle=True)

tic = time.perf_counter()
scores_yatzy = []
scores_bonus = []
scores_yatzybonus = []
scores_none = []

fig, ax = plt.subplots()
since_last_plot = 0
bins = np.arange(0, 350, 1) - 0.5
for game in range(NUM_GAMES):
    score, got_yatzy, got_bonus = play_game(BOARD_EV, NUM_DICE, NUM_CATEGORIES)
    if got_yatzy:
        if got_bonus:
            scores_yatzybonus.append(score)
        else:
            scores_yatzy.append(score)
    else:
        if got_bonus:
            scores_bonus.append(score)
        else:
            scores_none.append(score)
    print(f"Games playes: {game + 1}")

    if since_last_plot >= 20:
        since_last_plot = 0
        fig.clear()
        ax = plt.hist(
            [scores_yatzy, scores_bonus, scores_yatzybonus, scores_none],
            bins,
            label=["Yatzy", "bonus", "Yatzy + bonus", "nothing"],
            stacked=True,
        )
        plt.draw()
        plt.legend()
        plt.pause(0.1)
    since_last_plot += 1


toc = time.perf_counter()
time_per_game = (toc - tic) / game
print(f"time per game: {time_per_game:.2g}s")

plt.figure()
plt.hist(
    [scores_yatzy, scores_bonus, scores_yatzybonus, scores_none],
    bins,
    label=["Yatzy", "bonus", "Yatzy + bonus", "nothing"],
    stacked=True,
)

plt.legend()

sum(scores_yatzy) + sum(scores_bonus) + sum(scores_yatzybonus) + sum(scores_none)

yatzy_ratio = (len(scores_yatzy) + len(scores_yatzybonus)) / game
bonus_ratio = (len(scores_bonus) + len(scores_yatzybonus)) / game
none_ratio = len(scores_none) / game


# scores = {'none': scores_none,
#           'yatzy': scores_yatzy,
#           'yatzybonus': scores_yatzybonus,
#           'bonus': scores_bonus}
# pickle_out = open(f"scorestatistics_{game}games", "wb")
# pickle.dump(scores, pickle_out)
# pickle_out.close()
