# Implements the Top-Trading-Cycles algorithm
import csv
import os
import random

### Functions ##################################################

def find_cycle(seekers):
    seeker = seekers.keys()[0] #randomize?
    cycle = [get_house(seeker)]
    while True:
        h = get_favorite_house(seeker)
        cycle.append(h)
        if h in cycle[:-1]:
            index_h = cycle[:-1].index(h)
            return cycle[index_h:]
        seeker = get_owner(h)
    return [] #should never be empty
    
def execute_trades(cycle):
    for i in xrange(len(cycle)-1):
        seeker = get_owner(cycle[i])
        assignments[seeker] = cycle[i+1]
        remove_from_market(seeker)

def remove_from_market(seeker):
    h = assignments[seeker]
    del seekers[seeker]
    for s in seekers.keys():
        if h in seekers[s][1]:
            seekers[s][1].remove(h)        

def get_owner(house):
    return houses[house]

def get_house(owner):
    return seekers[owner][0]

def get_favorite_house(owner):
    return seekers[owner][1][0]

### Script #######################################################

os.chdir(os.path.dirname(os.getcwd())) #move up tp parent director
input_file = 'data/preferences.csv'
output_file = 'data/assignments.csv'
reader = csv.DictReader(open(input_file, 'rU'))
writer = csv.writer(open(output_file, 'w'))

seekers = dict()
houses = dict()
assignments = dict()

for row in reader: 
    seekers[row['seeker_email']] = (row['current_house_id'], row['prefs'].split(','))
    houses[row['current_house_id']] = row['seeker_email']

while seekers:
    c = find_cycle(seekers)
    print c
    execute_trades(c)

writer.writerow(['seeker_email', 'current_house_id', 'assigned_house_id'])
for house in houses:
    seeker = get_owner(house)
    new_house = assignments[seeker]
    writer.writerow([seeker, house, new_house])
    
    