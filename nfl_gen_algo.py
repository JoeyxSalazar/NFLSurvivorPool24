import random
import numpy as np
from deap import base, creator, tools, algorithms

# Example preseason rankings (1 is the best team, 32 is the worst)
preseason_rankings = {
                        1: "Eagles",
                        2: "Ravens",
                        3: "Bills",
                        4: "Chiefs",
                        5: "Lions",
                        6: "Commanders",
                        7: "Chargers",
                        8: "Packers",
                        9: "Rams",
                        10: "Texans",
                        11: "49ers",
                        12: "Broncos",
                        13: "Buccaneers",
                        14: "Bengals",
                        15: "Vikings",
                        16: "Steelers",
                        17: "Bears",
                        18: "Cardinals",
                        19: "Seahawks",
                        20: "Cowboys",
                        21: "Jaguars",
                        22: "Patriots",
                        23: "Dolphins",
                        24: "Falcons",
                        25: "Raiders",
                        26: "Panthers",
                        27: "Jets",
                        28: "Giants",
                        29: "Titans",
                        30: "Colts",
                        31: "Browns",
                        32: "Saints"
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
        #Opponent is at home, lets add a slight gain for that
        opponent_rank = get_rank(opponent) + 1.5
        team_rank = get_rank(team)
        fitness += (opponent_rank - team_rank)  # Positive value means a better team selected
        used_teams.add(team)
    return fitness,

def main(pop_size: int = 2000,
         ngen: int = 750,
         cxpb: float = 0.7,
         mutpb: float = 0.4,
         tournsize: int = 3,
         weeks: int = 13) -> None:
    
    random.seed(42)

    if "FitnessMax" not in creator.__dict__:
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("indices",
                     random.sample,
                     list(preseason_rankings.values()) + [None],
                     weeks)
    toolbox.register("individual", tools.initIterate,
                     creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat,
                     list, toolbox.individual)

    toolbox.register("evaluate", eval_survivor)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=tournsize)

    hof = tools.HallOfFame(1)
    algorithms.eaSimple(toolbox.population(pop_size),
                        toolbox, cxpb, mutpb, ngen,
                        halloffame=hof, verbose=False)

    best_strategy = hof[0]
    print("Best survivor plan:", best_strategy,
          best_strategy.fitness.values)

if __name__ == "__main__":
    main()
