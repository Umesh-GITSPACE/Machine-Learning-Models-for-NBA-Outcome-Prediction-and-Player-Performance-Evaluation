#!/usr/bin/env python
# coding: utf-8

# In[14]:


#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import tkinter as tk
from tkinter import messagebox, Entry, Button, Label
from PIL import Image, ImageTk
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA

def load_data(teams_performance_path, players_path):
    teams_performance_df = pd.read_excel(r"C:\Users\awiga\Downloads\NBA_teams_performance_with_dummies.xlsx")
    players_df = pd.read_excel(r"C:\Users\awiga\OneDrive\Desktop\Sem 2\1.Data mining\project\data\players 1.xlsx")
    return teams_performance_df, players_df

def preprocess_data(teams_performance_df):
    teams_performance_df['Win'] = (teams_performance_df['W/L%'] > 0.5).astype(int)
    features = teams_performance_df.drop(columns=['Team', 'W/L%', 'Win', 'Season'] + teams_performance_df.columns[teams_performance_df.columns.str.contains('Div_|Conf_')].tolist())
    target = teams_performance_df['Win']
    return features, target

def train_model(features, target):
    X_train, _, y_train, _ = train_test_split(features, target, test_size=0.2, random_state=42)
    pipeline = make_pipeline(StandardScaler(), PCA(n_components=2), LogisticRegression(random_state=42))
    pipeline.fit(X_train, y_train)
    return pipeline

def predict_winner(team1, team2, model, teams_performance_df):
    team1_stats = teams_performance_df[teams_performance_df['Team'] == team1].drop(columns=['Team', 'W/L%', 'Win', 'Season'] + teams_performance_df.columns[teams_performance_df.columns.str.contains('Div_|Conf_')].tolist())
    team2_stats = teams_performance_df[teams_performance_df['Team'] == team2].drop(columns=['Team', 'W/L%', 'Win', 'Season'] + teams_performance_df.columns[teams_performance_df.columns.str.contains('Div_|Conf_')].tolist())
    
    if team1_stats.empty or team2_stats.empty:
        missing_teams = [team1 if team1_stats.empty else "", team2 if team2_stats.empty else ""]
        messagebox.showerror("Error", f"Could not find stats for {' and '.join(filter(None, missing_teams))}. Please check the team names.")
        return None
    
    team1_prob = model.predict_proba(team1_stats)[:, 1][0]
    team2_prob = model.predict_proba(team2_stats)[:, 1][0]
    return team1 if team1_prob > team2_prob else team2

def get_top_5_players(team, players_df):
    team_players = players_df[players_df['Tm'] == team]
    unique_team_players = team_players.drop_duplicates(subset='Player')
    top_players = unique_team_players.nlargest(5, 'PTS')
    return [(row['Player'], row['PTS']) for index, row in top_players.iterrows()]

def show_prediction(team1, team2, model, teams_performance_df, players_df):
    winner = predict_winner(team1, team2, model, teams_performance_df)
    if not winner:
        return
    
    top_players_team1 = get_top_5_players(team1, players_df)
    top_players_team2 = get_top_5_players(team2, players_df)
    result_text = f"Likely Winner: {winner}\n\nTop 5 Performing Players from {team1}:\n"
    for player, pts in top_players_team1:
        result_text += f"{player}: {pts} PTS\n"
    result_text += f"\nTop 5 Performing Players from {team2}:\n"
    for player, pts in top_players_team2:
        result_text += f"{player}: {pts} PTS\n"
    
    messagebox.showinfo("Prediction Results", result_text)

if __name__ == "__main__":
    teams_performance_path = r"C:\Users\awiga\Downloads\NBA_teams_performance_with_dummies.xlsx"
    players_path = r"C:\Users\awiga\OneDrive\Desktop\Sem 2\1.Data mining\project\data\players 1.xlsx"
    teams_df, players_df = load_data(teams_performance_path, players_path)
    features, target = preprocess_data(teams_df)
    model = train_model(features, target)

    root = tk.Tk()
    root.title("NBA Team Performance Predictor")

    bg_image_path = "C:/Users/awiga/OneDrive/Desktop/Sem 2/1.Data mining/project/data/nba.jpg"
    bg_image = Image.open(bg_image_path)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    Label(root, text="Team 1:", bg='light gray').pack(pady=(10, 0))
    team1_entry = Entry(root)
    team1_entry.pack(pady=(0, 10))

    Label(root, text="Team 2:", bg='light gray').pack(pady=(10, 0))
    team2_entry = Entry(root)
    team2_entry.pack(pady=(0, 10))

    predict_button = Button(root, text="Predict Winner", command=lambda: show_prediction(team1_entry.get(), team2_entry.get(), model, teams_df, players_df))
    predict_button.pack(pady=20)

    root.mainloop()


# In[ ]:




