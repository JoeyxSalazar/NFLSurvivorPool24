import random
import numpy as np
from deap import base, creator, tools, algorithms

# Example preseason rankings (1 is the best team, 32 is the worst)
preseason_rankings = {
                        1: "49ers",
                        2: "Chiefs",
                        3: "Lions",
                        4: "Ravens",
                        5: "Bengals",
                        6: "Eagles",
                        7: "Texans",
                        8: "Bills",
                        9: "Packers",
                        10: "Cowboys",
                        11: "Jets",
                        12: "Dolphins",
                        13: "Browns",
                        14: "Falcons",
                        15: "Bears",
                        16: "Rams",
                        17: "Steelers",
                        18: "Colts",
                        19: "Jaguars",
                        20: "Seahawks",
                        21: "Chargers",
                        22: "Vikings",
                        23: "Buccaneers",
                        24: "Saints",
                        25: "Cardinals",
                        26: "Titans",
                        27: "Raiders",
                        28: "Commanders",
                        29: "Patriots",
                        30: "Giants",
                        31: "Broncos",
                        32: "Panthers"
                    }
#Reverse dictionary for easier lookups
rank_to_team = {team: rank for rank, team in preseason_rankings.items()}
# Example structure for NFL schedule (week 1-18)
nfl_schedule = {
    1: [('Cowboys', 'Eagles'),('Chiefs', 'Chargers'),('Dolphins', 'Colts'),('Steelers', 'Jets'),('Panthers', 'Jaguars'),('Cardinals', 'Saints'),('Giants', 'Commanders'),('Buccaneers', 'Falcons'),('Bengals', 'Browns'),('Raiders', 'Patriots'),('49ers', 'Seahawks'),('Titans', 'Broncos'),('Lions', 'Packers'),('Texans', 'Rams'),('Ravens', 'Bills'),('Vikings', 'Bears'),],
    2: [('Commanders', 'Packers'),('Giants', 'Cowboys'),('Seahawks', 'Steelers'),('Rams', 'Titans'),('Bills', 'Jets'),('Patriots', 'Dolphins'),('Jaguars', 'Bengals'),('49ers', 'Saints'),('Browns', 'Ravens'),('Bears', 'Lions'),('Broncos', 'Colts'),('Panthers', 'Cardinals'),('Eagles', 'Chiefs'),('Falcons', 'Vikings'),('Buccaneers', 'Texans'),('Chargers', 'Raiders'),],
    3: [('Dolphins', 'Bills'),('Bengals', 'Vikings'),('Texans', 'Jaguars'),('Colts', 'Titans'),('Raiders', 'Commanders'),('Rams', 'Eagles'),('Falcons', 'Panthers'),('Steelers', 'Patriots'),('Packers', 'Browns'),('Jets', 'Buccaneers'),('Broncos', 'Chargers'),('Saints', 'Seahawks'),('Cowboys', 'Bears'),('Cardinals', '49ers'),('Chiefs', 'Giants'),('Lions', 'Ravens'),],
    4: [('Seahawks', 'Cardinals'),('Vikings', 'Steelers'),('Commanders', 'Falcons'),('Chargers', 'Giants'),('Titans', 'Texans'),('Eagles', 'Buccaneers'),('Panthers', 'Patriots'),('Saints', 'Bills'),('Browns', 'Lions'),('Jaguars', '49ers'),('Colts', 'Rams'),('Bears', 'Raiders'),('Ravens', 'Chiefs'),('Packers', 'Cowboys'),('Jets', 'Dolphins'),('Bengals', 'Broncos'),],
    5: [('49ers', 'Rams'),('Vikings', 'Browns'),('Cowboys', 'Jets'),('Giants', 'Saints'),('Raiders', 'Colts'),('Dolphins', 'Panthers'),('Broncos', 'Eagles'),('Texans', 'Ravens'),('Titans', 'Cardinals'),('Buccaneers', 'Seahawks'),('Lions', 'Bengals'),('Commanders', 'Chargers'),('Patriots', 'Bills'),('Chiefs', 'Jaguars'),],
    6: [('Eagles', 'Giants'),('Broncos', 'Jets'),('49ers', 'Buccaneers'),('Seahawks', 'Jaguars'),('Chargers', 'Dolphins'),('Rams', 'Ravens'),('Cardinals', 'Colts'),('Cowboys', 'Panthers'),('Browns', 'Steelers'),('Titans', 'Raiders'),('Bengals', 'Packers'),('Patriots', 'Saints'),('Lions', 'Chiefs'),('Bills', 'Falcons'),('Bears', 'Commanders'),],
    7: [('Steelers', 'Bengals'),('Rams', 'Jaguars'),('Eagles', 'Vikings'),('Patriots', 'Titans'),('Panthers', 'Jets'),('Dolphins', 'Browns'),('Saints', 'Bears'),('Raiders', 'Chiefs'),('Colts', 'Chargers'),('Giants', 'Broncos'),('Packers', 'Cardinals'),('Commanders', 'Cowboys'),('Falcons', '49ers'),('Buccaneers', 'Lions'),('Texans', 'Seahawks'),],
    8: [('Vikings', 'Chargers'),('Dolphins', 'Falcons'),('Bears', 'Ravens'),('Jets', 'Bengals'),('Bills', 'Panthers'),('49ers', 'Texans'),('Browns', 'Patriots'),('Giants', 'Eagles'),('Buccaneers', 'Saints'),('Titans', 'Colts'),('Cowboys', 'Broncos'),('Packers', 'Steelers'),('Commanders', 'Chiefs'),],
    9: [('Ravens', 'Dolphins'),('49ers', 'Giants'),('Chargers', 'Titans'),('Vikings', 'Lions'),('Falcons', 'Patriots'),('Colts', 'Steelers'),('Broncos', 'Texans'),('Bears', 'Bengals'),('Panthers', 'Packers'),('Saints', 'Rams'),('Jaguars', 'Raiders'),('Chiefs', 'Bills'),('Seahawks', 'Commanders'),('Cardinals', 'Cowboys'),],
    10: [('Raiders', 'Broncos'),('Falcons', 'Colts'),('Browns', 'Jets'),('Saints', 'Panthers'),('Patriots', 'Buccaneers'),('Ravens', 'Vikings'),('Bills', 'Dolphins'),('Giants', 'Bears'),('Jaguars', 'Texans'),('Cardinals', 'Seahawks'),('Lions', 'Commanders'),('Rams', '49ers'),('Steelers', 'Chargers'),('Eagles', 'Packers'),],
    11: [('Jets', 'Patriots'),('Commanders', 'Dolphins'),('Packers', 'Giants'),('Texans', 'Titans'),('Panthers', 'Falcons'),('Bears', 'Vikings'),('Chargers', 'Jaguars'),('Buccaneers', 'Bills'),('Bengals', 'Steelers'),('49ers', 'Cardinals'),('Seahawks', 'Rams'),('Chiefs', 'Broncos'),('Ravens', 'Browns'),('Lions', 'Eagles'),('Cowboys', 'Raiders'),],
    12: [('Bills', 'Texans'),('Colts', 'Chiefs'),('Seahawks', 'Titans'),('Vikings', 'Packers'),('Jets', 'Ravens'),('Giants', 'Lions'),('Steelers', 'Bears'),('Patriots', 'Bengals'),('Browns', 'Raiders'),('Jaguars', 'Cardinals'),('Eagles', 'Cowboys'),('Falcons', 'Saints'),('Buccaneers', 'Rams'),('Panthers', '49ers'),],
    13: [('Packers', 'Lions'),('Chiefs', 'Cowboys'),('Bengals', 'Ravens'),('Bears', 'Eagles'),('Saints', 'Dolphins'),('Texans', 'Colts'),('Falcons', 'Jets'),('49ers', 'Browns'),('Rams', 'Panthers'),('Jaguars', 'Titans'),('Cardinals', 'Buccaneers'),('Vikings', 'Seahawks'),('Bills', 'Steelers'),('Raiders', 'Chargers'),('Broncos', 'Commanders'),('Giants', 'Patriots'),],
    14: [],
    15: [],
    16: [],
    17: [],
}
def get_rank(team_name):
    return rank_to_team.get(team_name, 'N/A')

# Fitness function: sum of ranking discrepancies
def print_schedule():
    for week, matchups in nfl_schedule.items():
        print(f"Week {week}:")
        for (t1, t2) in matchups:
            print(f"{t1}, Rank: {get_rank(t1)} vs {t2}, Rank: {get_rank(t2)}")
        
def eval_survivor(individual):
    fitness = 0
    used_teams = set()
    bye_week_used = False
    for week, team in enumerate(individual, 1):
        if team == None:
            if bye_week_used:
                return -1000,
            bye_week_used = True
            fitness += 30  # Increase for using a bye week
            continue
        if team in used_teams:
            return -1000,  # Immediate penalty for reusing a team
        matchups = nfl_schedule[week]
        opponent = None
        for (t1, t2) in matchups:
            if t1 == team:
                opponent = t2
                break
            elif t2 == team:
                opponent = t1
                break
        if opponent is None:
            return -1000,
        opponent_rank = get_rank(opponent)
        team_rank = get_rank(team)
        #print(f"Week {week}: {team} vs {opponent} (Team Rank: {team_rank}, Opponent Rank: {opponent_rank})")
        fitness += (opponent_rank - team_rank)  # Positive value means a better team selected
        used_teams.add(team)
    return fitness,

def main():
    # Genetic Algorithm Setup
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    weeks = 13       # Number of weeks in the survivor pool
    toolbox.register("indices", random.sample, list(preseason_rankings.values()) + [None], weeks)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", eval_survivor)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Running the Genetic Algorithm
    population = toolbox.population(n=2000)
    ngen = 750
    cxpb = 0.7  # Crossover probability
    mutpb = 0.4 # Mutation probability

    
    # Applying the genetic algorithm
    best_ind = algorithms.eaSimple(population, toolbox, cxpb, mutpb, ngen, verbose=False)[0]
    # Output the best team selection strategy
    best_strategy = tools.selBest(best_ind, k=1)[0]
    print("Best Survivor Strategy:")
    print(len(best_strategy))
    print(best_strategy, best_strategy.fitness.values)

if __name__ == "__main__":
    main()
