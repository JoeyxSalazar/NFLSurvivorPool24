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
    1 : [("Ravens", "Chiefs" ),("Packers", "Eagles" ),("Patriots", "Bengals" ),("Texans", "Colts" ),("Steelers", "Falcons" ),("Jaguars", "Dolphins" ),("Vikings", "Giants" ),("Cardinals", "Bills" ),("Panthers", "Saints" ),("Titans", "Bears" ),("Broncos", "Seahawks" ),("Raiders", "Chargers" ),("Commanders", "Buccaneers" ),("Cowboys", "Browns" ),("Rams", "Lions" ),("Jets", "49ers" )],
    2: [("Bills", "Dolphins" ),("Raiders", "Ravens" ),("Chargers", "Panthers" ),("Browns", "Jaguars" ),("Seahawks", "Patriots" ),("Colts", "Packers" ),("49ers", "Vikings" ),("Buccaneers", "Lions" ),("Giants", "Commanders" ),("Saints", "Cowboys" ),("Jets", "Titans" ),("Rams", "Cardinals" ),("Bengals", "Chiefs" ),("Steelers", "Broncos" ),("Bears", "Texans" ),("Falcons", "Eagles" )],
    3: [("Patriots", "Jets" ),("Packers", "Titans" ),("Eagles", "Saints" ),("Texans", "Vikings" ),("Giants", "Browns" ),("Chargers", "Steelers" ),("Broncos", "Buccaneers" ),("Bears", "Colts" ),("Panthers", "Raiders" ),("Dolphins", "Seahawks" ),("Lions", "Cardinals" ),("Ravens", "Cowboys" ),("49ers", "Rams" ),("Chiefs", "Falcons" ),("Jaguars", "Bills" ),("Commanders", "Bengals" )],
    4: [("Cowboys", "Giants" ),("Vikings", "Packers" ),("Saints", "Falcons" ),("Bengals", "Panthers" ),("Rams", "Bears" ),("Steelers", "Colts" ),("Broncos", "Jets" ),("Jaguars", "Texans" ),("Eagles", "Buccaneers" ),("Commanders", "Cardinals" ),("Patriots", "49ers" ),("Browns", "Raiders" ),("Chiefs", "Chargers" ),("Bills", "Ravens" ),("Titans", "Dolphins" ),("Seahawks", "Lions" )],
    5: [("Buccaneers", "Falcons" ),("Jets", "Vikings" ),("Bills", "Texans" ),("Dolphins", "Patriots" ),("Browns", "Commanders" ),("Panthers", "Bears" ),("Colts", "Jaguars" ),("Ravens", "Bengals" ),("Cardinals", "49ers" ),("Raiders", "Broncos" ),("Packers", "Rams" ),("Giants", "Seahawks" ),("Cowboys", "Steelers" ),("Saints", "Chiefs" )],
    6: [("49ers", "Seahawks" ),("Jaguars", "Bears" ),("Cardinals", "Packers" ),("Texans", "Patriots" ),("Browns", "Eagles" ),("Colts", "Titans" ),("Commanders", "Ravens" ),("Buccaneers", "Saints" ),("Chargers", "Broncos" ),("Steelers", "Raiders" ),("Falcons", "Panthers" ),("Lions", "Cowboys" ),("Bengals", "Giants" ),("Bills", "Jets" )],
    7: [('Broncos', 'Saints'),('Patriots', 'Jaguars'),('Eagles', 'Giants'),('Texans', 'Packers'),('Bengals', 'Browns'),('Lions', 'Vikings'),('Dolphins', 'Colts'),('Seahawks', 'Falcons'),('Titans', 'Bills'),('Panthers', 'Commanders'),('Raiders', 'Rams'),('Chiefs', '49ers'),('Jets', 'Steelers'),('Ravens', 'Buccaneers'),('Chargers', 'Cardinals')],
    8: [('Vikings', 'Rams'),('Falcons', 'Buccaneers'),('Cardinals', 'Dolphins'),('Ravens', 'Browns'),('Bears', 'Commanders'),('Packers', 'Jaguars'),('Titans', 'Lions'),('Jets', 'Patriots'),('Colts', 'Texans'),('Saints', 'Chargers'),('Bills', 'Seahawks'),('Eagles', 'Bengals'),('Panthers', 'Broncos'),('Chiefs', 'Raiders'),('Cowboys', '49ers'),('Giants', 'Steelers')],
    9: [('Texans', 'Jets'),('Saints', 'Panthers'),('Cowboys', 'Falcons'),('Patriots', 'Titans'),('Chargers', 'Browns'),('Commanders', 'Giants'),('Broncos', 'Ravens'),('Colts', 'Vikings'),('Raiders', 'Bengals'),('Dolphins', 'Bills'),('Bears', 'Cardinals'),('Lions', 'Packers'),('Rams', 'Seahawks'),('Jaguars', 'Eagles'),('Buccaneers', 'Chiefs')],
    10: [('Bengals', 'Ravens'),('Giants', 'Panthers'),('49ers', 'Buccaneers'),('Patriots', 'Bears'),('Vikings', 'Jaguars'),('Steelers', 'Commanders'),('Broncos', 'Chiefs'),('Falcons', 'Saints'),('Bills', 'Colts'),('Titans', 'Chargers'),('Jets', 'Cardinals'),('Eagles', 'Cowboys'),('Lions', 'Texans'),('Dolphins', 'Rams')],
    11: [('Commanders', 'Eagles'),('Rams', 'Patriots'),('Vikings', 'Titans'),('Packers', 'Bears'),('Jaguars', 'Lions'),('Raiders', 'Dolphins'),('Ravens', 'Steelers'),('Browns', 'Saints'),('Seahawks', '49ers'),('Falcons', 'Broncos'),('Chiefs', 'Bills'),('Bengals', 'Chargers'),('Colts', 'Jets'),('Texans', 'Cowboys')],
    12: [('Steelers', 'Browns'),('Lions', 'Colts'),('Buccaneers', 'Giants'),('Vikings', 'Bears'),('Chiefs', 'Panthers'),('Cowboys', 'Commanders'),('Patriots', 'Dolphins'),('Titans', 'Texans'),('Broncos', 'Raiders'),('49ers', 'Packers'),('Cardinals', 'Seahawks'),('Eagles', 'Rams'),('Ravens', 'Chargers')],
    13: [('Bears', 'Lions'),('Giants', 'Cowboys'),('Dolphins', 'Packers'),('Raiders', 'Chiefs'),('Colts', 'Patriots'),('Texans', 'Jaguars'),('Cardinals', 'Vikings'),('Chargers', 'Falcons'),('Seahawks', 'Jets'),('Titans', 'Commanders'),('Steelers', 'Bengals'),('Rams', 'Saints'),('Buccaneers', 'Panthers'),('Eagles', 'Ravens'),('49ers', 'Bills'),('Browns', 'Broncos')],
    14: [('Packers', 'Lions'),('Browns', 'Steelers'),('Raiders', 'Buccaneers'),('Panthers', 'Eagles'),('Falcons', 'Vikings'),('Jets', 'Dolphins'),('Jaguars', 'Titans'),('Saints', 'Giants'),('Seahawks', 'Cardinals'),('Bills', 'Rams'),('Bears', '49ers'),('Chargers', 'Chiefs'),('Bengals', 'Cowboys')],
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
    for week, team in enumerate(individual, 1):
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
    weeks = 13  # Number of weeks in the survivor pool
    toolbox.register("indices", random.sample, list(preseason_rankings.values()), weeks)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", eval_survivor)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    # Running the Genetic Algorithm
    population = toolbox.population(n=500)
    ngen = 500
    cxpb = 0.7  # Crossover probability
    mutpb = 0.2  # Mutation probability

    # Applying the genetic algorithm
    best_ind = algorithms.eaSimple(population, toolbox, cxpb, mutpb, ngen, verbose=False)[0]

    # Output the best team selection strategy
    best_strategy = tools.selBest(best_ind, k=5)[0]
    print("Best Survivor Strategy:")
    print(best_strategy, best_strategy.fitness.values)
    print(len(best_strategy))

if __name__ == "__main__":
    main()
