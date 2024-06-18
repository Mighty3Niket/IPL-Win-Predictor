import numpy as np
import pandas as pd
match = pd.read_csv('matches.csv')
delivery = pd.read_csv('deliveries.csv')
#print(match.head())
#print(match.shape)
#print(delivery.head())
#print(delivery.shape)
total_score_df = delivery.groupby(['ID', 'innings']).sum()['total_run'].reset_index()
total_score_df = total_score_df[total_score_df['innings'] == 1]
match_df = match.merge(total_score_df[['ID', 'total_run']], on='ID')

#Present IPL Teams
teams = ['Chennai Super Kings', 'Delhi Capitals', 'Gujarat Titans', 'Kolkata Knight Riders', 'Lucknow Super Giants', 'Mumbai Indians', 'Punjab Kings', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad']

#Merging same teams
match_df['Team1'] = match_df['Team1'].str.replace('Delhi Daredevils', 'Delhi Capitals')
match_df['Team2'] = match_df['Team2'].str.replace('Delhi Daredevils', 'Delhi Capitals')

match_df['Team1'] = match_df['Team1'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')
match_df['Team2'] = match_df['Team2'].str.replace('Deccan Chargers', 'Sunrisers Hyderabad')

match_df['Team1'] = match_df['Team1'].str.replace('Kings XI Punjab', 'Punjab Kings')
match_df['Team2'] = match_df['Team2'].str.replace('Kings XI Punjab', 'Punjab Kings')

#Discarding unnecessary teams
match_df = match_df[match_df['Team1'].isin(teams)]
match_df = match_df[match_df['Team2'].isin(teams)]

#Eliminating D/L matches
match_df = match_df.drop(match_df[match_df['method'] == 'D/L'].index)

#Selecting required columns
match_df = match_df[['ID', 'City', 'Team1', 'Team2', 'WinningTeam', 'total_run']]

#Merging with delivery table
delivery_df = match_df.merge(delivery, on='ID')
delivery_df = delivery_df[delivery_df['innings'] == 2]

#Determining Bowling Team
def get_bowling_team(row):
    if row['BattingTeam'] == row['Team1']:
        return row['Team2']
    else:
        return row['Team1']

delivery_df['BowlingTeam'] = delivery_df.apply(get_bowling_team, axis=1)

#Dropping Team1 & Team2
delivery_df = delivery_df.drop('Team1', axis=1)
delivery_df = delivery_df.drop('Team2', axis=1)

#Calculating Current Score
delivery_df['current_score'] = delivery_df.groupby('ID')['total_run_y'].cumsum()

#Calculating Runs Required
delivery_df['runs_reqd'] = delivery_df['total_run_x'] + 1 - delivery_df['current_score']

#Calculating Balls Left
delivery_df['balls_left'] = 120 - (delivery_df['overs']*6 + delivery_df['ballnumber'])

#Calculating Wickets Left
delivery_df['player_out'] = delivery_df['player_out'].fillna("0")
delivery_df['player_out'] = delivery_df['player_out'].apply(lambda x:x if x == "0" else "1")
delivery_df['player_out'] = delivery_df['player_out'].astype('int')
wickets = delivery_df.groupby('ID')['player_out'].cumsum().values
delivery_df['wkts_left'] = 10 - wickets

#Calculating Current Run Rate
delivery_df['crr'] = (delivery_df['current_score']*6)/(120 - delivery_df['balls_left'])

#Calculating Required Run Rate
delivery_df['rrr'] = (delivery_df['runs_reqd']*6)/delivery_df['balls_left']

#Evaluating result of the match
def result(row):
    return 1 if row['BattingTeam'] == row['WinningTeam'] else 0
delivery_df['result'] = delivery_df.apply(result, axis=1)

final_df = delivery_df[['BattingTeam', 'BowlingTeam', 'City', 'runs_reqd', 'balls_left', 'wkts_left', 'total_run_x', 'crr', 'rrr', 'result']]

#Shuffling all over
final_df = final_df.sample(final_df.shape[0])

final_df = final_df[final_df['balls_left'] != 0]

#for col in final_df.columns:
#    print(col)

final_df.sample()

#for col in delivery_df.columns:
#    print(col)
#print(delivery_df)

#print(match_df['Team1'].unique())
#print(match_df['method'].value_counts())
#print(match_df.head)
#x=delivery_df['City'].unique(),
#print(x)