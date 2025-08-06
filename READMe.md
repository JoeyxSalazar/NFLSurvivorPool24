# Background
Every year, some friends and I create an NFL Survivor Pool. Each week, the participants need to select one team that they think will win their match-up. If the participant's chosen team wins, they survive. If they lose, the participant is removed from the pool and must wait until next year. 
If your team wins that weak, you progress. However, once you select a team, you cannot use that team in future weeks. This prevents someone from choosing the number one team every week. 
The last remaining participant survives
# My theory
Simulate as many weekly picks as possible, calculate a fitness score based on the discrepancy of the match-ups ranks, apply genetic algorithm principals. 
# To run
- Install poetry, poetry is a dependency manager to keep consistent environments
- ''' poetry install '''
- ''' poetry run python nfl_gen_algo.py '''
