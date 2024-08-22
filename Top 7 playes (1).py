#!/usr/bin/env python
# coding: utf-8

# In[12]:


import pandas as pd

# Load the data
df = pd.read_csv(r"C:\Users\awiga\OneDrive\Desktop\Sem 2\1.Data mining\project\data\NBA_Player_Stats.csv")



# In[13]:


# Data cleaning and filtering
filtered_df = df[(df['Age'] < 38) & (df['Year'] == '2021-2022')]
filtered_df.fillna({'FG%': 0, '3P%': 0, '2P%': 0, 'eFG%': 0, 'FT%': 0}, inplace=True)


# In[14]:


# Normalize percentage columns
for col in ['3P%', '2P%', 'FG%', 'eFG%', 'FT%']:
    filtered_df[col] = filtered_df[col] / 100


# In[15]:


# Calculate scores for each player category
filtered_df['Defense_Score'] = filtered_df[['TRB', 'DRB', 'BLK', 'ORB']].sum(axis=1)
filtered_df['Allround_Score'] = filtered_df[['AST', '3P%', 'STL', '2P%', 'FG%', 'eFG%']].sum(axis=1)
filtered_df['Forward_Score'] = filtered_df[['PTS', '2P%', '3P%', 'FT%']].sum(axis=1)


# In[16]:


# Function to select top 7 unique players for each category, ensuring no repetition within or across categories
def select_top_unique_players(score_column, excluded_players):
    unique_players = filtered_df.drop_duplicates(subset=['Player'])
    candidates = unique_players[~unique_players['Player'].isin(excluded_players)].sort_values(by=score_column, ascending=False)
    return candidates[:7]  # Return top 7 candidates not already selected or repeated
already_selected = []
categories = {'Defense': 'Defense_Score', 'Allround': 'Allround_Score', 'Forward': 'Forward_Score'}


# In[17]:


# Iterate over categories to select and print top players
for category, score_column in categories.items():
    top_players = select_top_unique_players(score_column, already_selected)
    already_selected.extend(top_players['Player'].tolist())
    print(f"Top 7 {category} Players:")
    print(top_players[['Player', score_column]])
    print("\n")


# In[ ]:




