import joblib
import streamlit as st
import pandas as pd

#load my model
model = joblib.load("myxgboost.joblib")

#load standard scaler used during training
scaler = joblib.load("myscaler.joblib")

#define the columns based on your model's features
columns = ["last_season_x", "height_in_cm", "age", "contract_days_left", "month", "year", "goals", "assists", "yellow_cards", "red_cards", "minutes_played", "player_club_id", "net_transfer_record", "national_team_players", "foot_both", "foot_left", "foot_right", "position_Attack", "position_Defender", "position_Goalkeeper", "position_Midfield", "sub_position_Attacking Midfield", "sub_position_Central Midfield", "sub_position_Centre-Back", "sub_position_Centre-Forward", "sub_position_Defensive Midfield", "sub_position_Goalkeeper", "sub_position_Left Midfield", "sub_position_Left Winger", "sub_position_Left-Back", "sub_position_Right Midfield", "sub_position_Right Winger", "sub_position_Right-Back", "sub_position_Second Striker", "league_id_BE1", "league_id_DK1", "league_id_ES1", "league_id_FR1", "league_id_GB1", "league_id_GR1", "league_id_IT1", "league_id_L1", "league_id_NL1", "league_id_PO1", "league_id_RU1", "league_id_SC1", "league_id_TR1", "league_id_UKR1", "Country_Argentina", "Country_Belgium", "Country_Brazil", "Country_Cote d'Ivoire", "Country_Croatia", "Country_Denmark", "Country_England", "Country_France", "Country_Germany", "Country_Greece", "Country_Italy", "Country_Morocco", "Country_Netherlands", "Country_Nigeria", "Country_Other", "Country_Poland", "Country_Portugal", "Country_Russia", "Country_Scotland", "Country_Senegal", "Country_Serbia", "Country_Spain", "Country_Sweden", "Country_Turkey", "Country_Ukraine", "Country_Uruguay"]

#streamlit app
st.title("Player Market Value Predictor")

#collect user input
user_input = {}

#league dropdown
league_options = list(set(column.split("_")[2] for column in columns if column.startswith("league_id_")))
selected_league = st.selectbox("Select League", league_options)
user_input.update({f"league_id_{selected_league}": 1})

#position dropdown
position_options = list(set(column.split("_")[1] for column in columns if column.startswith("position_")))
selected_position = st.selectbox("Select Position", position_options)
user_input.update({f"position_{selected_position}": 1})

#subposition dropdown
if selected_position == "Midfield":
    subposition_options = list(set(column.split("_")[2] for column in columns if column.startswith("sub_position_") and "Midfield" in column))
elif selected_position == "Defender":
    subposition_options = list(set(column.split("_")[2] for column in columns if column.startswith("sub_position_") and "Back" in column))
elif selected_position == "Goalkeeper":
    subposition_options = list(set(column.split("_")[2] for column in columns if column.startswith("sub_position_") and "Goalkeeper" in column))
elif selected_position == "Attack":
    subposition_options = list(set(column.split("_")[2] for column in columns if column.startswith("sub_position_") and ("Striker" in column or "Centre-Forward" in column or "Left Winger" in column or "Right Winger" in column)))
else:
    subposition_options = list(set(column.split("_")[2] for column in columns if column.startswith("sub_position_")))
selected_subposition = st.selectbox("Select Subposition", subposition_options)
user_input.update({f"sub_position_{selected_subposition}": 1})

#nationality dropdown
nationality_options = list(set(column.split("_")[1] for column in columns if column.startswith("Country_")))
selected_nationality = st.selectbox("Select Nationality", nationality_options)
user_input.update({f"Country_{selected_nationality}": 1})

#preferred foot dropdown
foot_options = list(set(column.split("_")[1] for column in columns if column.startswith("foot_")))
selected_foot = st.selectbox("Select Foot", foot_options)
user_input.update({f"foot_{selected_foot}": 1})

#sliders for numerical features
user_input["age"] = st.slider(f"Select Age", min_value=16, max_value=50, key="age", step=1)
user_input["goals"] = st.slider(f"Select Goals", min_value=0, max_value=100, key="goals", step=1)
user_input["assists"] = st.slider(f"Select Assists", min_value=0, max_value=100, key="assists", step=1)
user_input["yellow_cards"] = st.slider(f"Select Yellow Cards", min_value=0, max_value=25, key="yellow_cards", step=1)
user_input["red_cards"] = st.slider(f"Select Red Cards", min_value=0, max_value=10, key="red_cards", step=1)
user_input["minutes_played"] = st.slider(f"Select Minutes Played", min_value=0, max_value=9000, key="minutes_played", step=100)
user_input["height_in_cm"] = st.slider(f"Select Height (cm)", min_value=140, max_value=220, key="height_in_cm", step=1)
user_input["month"] = st.slider(f"Select Month Of Valuation", min_value=1, max_value=12, key="month", step=1)
user_input["year"] = st.slider(f"Select Year Of Valuation", min_value=2012, max_value=2023, key="year", step=1)
user_input["last_season_x"] = st.slider(f"Select Year Of Retirement", min_value=2012, max_value=2023, key="last_season_x", step=1)
user_input["contract_days_left"] = st.slider(f"Select Days Remaining Of Contract", min_value=0, max_value=1500, key="contract_days_left", step=30)
user_input["net_transfer_record"] = st.slider(f"Select Club's Net Transfer Record", min_value=-300000000, max_value=300000000, key="net_transfer_record", step=1000000)
# Hide 'player_club_id'
# user_input["player_club_id"] = st.slider(f"Select Player Club ID", min_value=0, max_value=1000, key="player_club_id", step=1)
user_input["national_team_players"] = st.slider(f"Select the Count of Club Players in National Teams ", min_value=0, max_value=18, key="national_team_players", step=1)

#convert user input to DataFrame and perform one-hot encoding
user_input_df = pd.DataFrame([user_input])

#drop the 'highest_ever_market_value' column if it exists
user_input_df = user_input_df.drop('highest_ever_market_value', axis=1, errors='ignore')

#make sure that the user_input_df has the same order of columns as the scaler
user_input_df = user_input_df.reindex(columns=columns, fill_value=0)

#scale using my standard scaler
user_input_scaled = scaler.transform(user_input_df)

#when the user clicks the "Predict" button
if st.button("Predict Market Value"):
    #make predictions
    prediction = model.predict(user_input_scaled)

    #round the prediction and format with commas
    rounded_prediction = int(round(prediction[0], -3))

    formatted_prediction = "{:,}".format(rounded_prediction)

    #display the prediction
    st.subheader("Predicted Market Value")
    st.write(f"The predicted market value is: {formatted_prediction}")



