#using the march madness predictor program, this will attempt to find the most profitable bracket
#this will simulate a variety of outcomes to find which yields the most predicted points
#predicted points are determined by multiplying the possible points gained by the probability of that team winning
#whichever has greatest sum of return is the best
#NOTE I simulated what would happen if the highest seed won every game, and got a TERRIBLE result (~-213)

import math
import random
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re
import lxml

path = input('Paste Kenpom .html file here: ')

#insert file location below here:
with open(path) as fp:
    soup = BeautifulSoup(fp, 'html.parser')
table_html = soup.find_all('table', {'id': 'ratings-table'})

thead = table_html[0].find_all('thead')

table = table_html[0]
for x in thead:
    table = str(table).replace(str(x), '')

#print(table)

#define df (dataframe)
df = pd.read_html(table)[0]

#finds Adjusted Offensive Efficiency of team
def AdjOSearch(Team):
    AdjO = float(df[df[1] == Team][5])
    return(AdjO)

#finds Adjusted Defensive Efficiency of team
def AdjDSearch(Team):
    AdjD = float(df[df[1] == Team][7])
    return(AdjD)

#calculates pythag of team, aka how "good" they are
def pythag(AdjO, AdjD):
        
    EW = (AdjO**11.5) / ((AdjO**11.5) + (AdjD**11.5))
    # the following tests pythag calculation:
    # print(str(EW))

    return EW

# Log5: Prob Team A wins against Team B (similar to ELO method in chess)
def log5(ProbA, ProbB):

    EWA = (ProbA - ProbA *  ProbB) / (ProbA + ProbB -2 * ProbA * ProbB)

    return EWA

def sep(TeamName):
        Seed = ''
        Name = ''
        for t in TeamName:

            try:
                Seed = Seed + str(int(t))
            except ValueError:
                Name = Name + t

        l = len(Name)
        Name = Name[:l-1]

        if Seed:
            return Name, int(Seed)

        else:
            return Name, False

#Sum of all point returns
def returner(A, B, round):
    TeamA = sep(A)[0]
    ASeed = sep(A)[1]
    TeamB = sep(B)[0]
    BSeed = sep(B)[1]

    AdjOA = AdjOSearch(TeamA)
    AdjDA = AdjDSearch(TeamA)
    AdjOB = AdjOSearch(TeamB)
    AdjDB = AdjDSearch(TeamB)
    
    PythagA = pythag(AdjOA, AdjDA)
    PythagB = pythag(AdjOB, AdjDB)

    AdjAProb = log5(PythagA, PythagB)
    AdjBProb = 1 - AdjAProb

    #print(AdjAProb)
    #print(AdjBProb)

    initialpoints = 2**round

    AReturn = AdjAProb * (initialpoints * ASeed)
    BReturn = AdjBProb * (initialpoints * BSeed)

    if random.randint(0,1) == 0:
        return AReturn, BReturn, A

    else:
        return BReturn, AReturn, B

    

#edit the below 'teams' list according to what teams are in the tournament (and what their seed is)


sims = int(input('How many tournaments do you want to simulate? '))

#the following for loop conducts the simulations. If the return is greater than the original, that tournament result and its return is printed
#if the return is lesser, it disregards and goes to the next one

Return = 0
roundteams = []
for i in range(0, sims):
    
    teams = ["Alabama 1", "Alcorn St. 16", "N.C. State 8", "Oklahoma St. 9", "Indiana 5", "Drake 12", "Miami FL 4", "Utah Valley 13", "Iowa 6", "Kentucky 11", "Marquette 3", "Eastern Washington 14", "San Diego St. 7", "Arkansas 10", "Baylor 2", "Youngstown St. 15", "Purdue 1", "Morehead St. 16", "Auburn 8", "Pittsburgh 9", "Creighton 5", "Oral Roberts 12", "Iowa St. 4", "Yale 13", "TCU 6", "Wisconsin 11", "Gonzaga 3", "UC Irvine 14", "Maryland 7", "Nevada 10", "UCLA 2", "Samford 15", "Houston 1", "Texas A&M Corpus Chris 16", "Rutgers 8", "Texas A&M 9", "Xavier 5", "VCU 12", "Kansas St. 4", "Southern Miss 13", "Illinois 6", "Memphis 11", "Tennessee 3", "Vermont 14", "Providence 7", "Boise St. 10", "Texas 2", "Kennesaw St. 15", "Kansas 1", "Rider 16", "Missouri 8", "Duke 9", "Saint Mary's 5", "Kent St. 12", "Connecticut 4", "Hofstra 13", "Northwestern 6", "West Virginia 11", "Virginia 3", "Colgate 14", "Michigan St. 7", "Florida Atlantic 10", "Arizona 2", "UNC Asheville 15"]
    teamnumber = len(teams)
    totalrounds = int(math.log(teamnumber, 2))

    roundteams0 = []
    Return0 = 0

    for round in range(0, totalrounds):
    
        #the following erases the previous nextround list. At the end of the previous iteration we switched nextround over to teams, so we can reset this.
        nextround = []
        Aindex = 0
        Bindex = 1
    
        #calculate # of teams in round
        teamnum = 2**(totalrounds - round)
    
        #print('teamnum: ' + str(teamnum))
        #print(round)
    
        #run all games in round
        while Bindex <= (teamnum-1):
            #print(Aindex)
            #print(Bindex)
            team = returner(teams[Aindex], teams[Bindex], round)[2]
            roundteams0.append(team)
            nextround.append(team)
            Return0 = Return0 + returner(teams[Aindex], teams[Bindex], round)[0]
            Return0 = Return0 - returner(teams[Aindex], teams[Bindex], round)[1]
            Aindex = Aindex + 2
            Bindex = Bindex + 2
    
        #switch winning teams to list of remaining competitors
        teams = nextround


    print(Return0)
    if (i+1) % 100 == 0:
        print(roundteams)

    if Return0 > Return:
        roundteams = roundteams0
        Return = Return0

print(roundteams)
print(Return)