import random
import pandas as pd

win_odds = [325, 325, 285, 400, 450]
my_win_prob = [.396, .332, .296, .224, .218]

def play_game(odds, prob):
    result = random.random()
    if result <= prob:
        return (odds)/100
    else:
        return -1

def play_all_games_no_parlay(odds_list, prob_list):
    total = 0
    any_wins = False
    for i in range(len(odds_list)):
        game_result = play_game(odds_list[i], prob_list[i])
        if game_result != -1:
            any_wins = True
        total += game_result
    if any_wins == False:
        None
    return total

def run_n_times(n, func, odds_list, prob_list):
    results = []
    for i in range(n):
        results.append(func(odds_list, prob_list))
    return sum(results) / n



print(run_n_times(10, play_all_games_no_parlay, win_odds, my_win_prob))


current_games_df = pd.read_csv('current_ncaa_games.csv')
max_date = max(current_games_df['Day'])
print(max_date)