import streamlit as st
import pickle
import pandas as pd

teams = ['Chennai Super Kings', 'Delhi Capitals', 'Gujarat Titans', 'Kolkata Knight Riders', 'Lucknow Super Giants', 'Mumbai Indians', 'Punjab Kings', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad']
cities = ['Ahmedabad', 'Kolkata', 'Mumbai', 'Navi Mumbai', 'Pune', 'Dubai',
       'Sharjah', 'Abu Dhabi', 'Delhi', 'Chennai', 'Hyderabad',
       'Visakhapatnam', 'Chandigarh', 'Bengaluru', 'Jaipur', 'Indore',
       'Bangalore', 'Raipur', 'Ranchi', 'Cuttack', 'Dharamsala', 'Nagpur',
       'Johannesburg', 'Centurion', 'Durban', 'Bloemfontein',
       'Port Elizabeth', 'Kimberley', 'East London', 'Cape Town']

pipe = pickle.load(open('pipe.pkl', 'rb'))

st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the Batting Team', sorted(teams))

with col2:
    bowling_team = st.selectbox('Select the Bowling Team', sorted(teams))

selected_city = st.selectbox('Select Host City', sorted(cities))

target = st.number_input('Target')

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Current Score')

with col4:
    overs = st.number_input('Overs Completed')

with col5:
    wickets = st.number_input('Wickets Fallen')

if st.button('Predict Win Probability'):
    runs_left = target - score
    balls_left = 120 - (overs*6)
    wickets_left = 10 - wickets
    crr = score/overs
    rrr = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'BattingTeam':[batting_team], 'BowlingTeam':[bowling_team], 'City':[selected_city], 'runs_reqd':[runs_left], 'balls_left':[balls_left], 'wkts_left':[wickets_left], 'total_run_x':[target], 'crr':[crr], 'rrr':[rrr]})
    #st.table(input_df)
    if batting_team!=bowling_team and target>0 and wickets<=10 and overs<=20 and score<=target:    
        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]
        st.header(batting_team + " - " + str(round(win*100)) + "%")
        st.header(bowling_team + " - " + str(round(loss*100)) + "%")
    else:
        st.header("Invalid data.")

st.text("built by Triniket Maiti")
