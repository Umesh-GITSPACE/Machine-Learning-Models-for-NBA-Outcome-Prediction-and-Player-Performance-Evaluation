#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Load the dataset
file_path = r"C:\Users\awiga\Downloads\NBA_teams_performance_with_dummies.xlsx"
nba_data = pd.read_excel(file_path)

# For demonstration, we assume the team with the highest W/L% is the champion
nba_data['Champion'] = (nba_data['W/L%'] == nba_data['W/L%'].max()).astype(int)

# Selecting features for the model
features = ['MOV', 'ORtg', 'DRtg', 'NRtg', 'MOV/A', 'ORtg/A', 'DRtg/A', 'NRtg/A']
X = nba_data[features]
y = nba_data['Champion']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize Logistic Regression model
logreg = LogisticRegression(max_iter=1000)

# Train the model
logreg.fit(X_train, y_train)

# Predict the probability of each team being the champion
probabilities = logreg.predict_proba(X)[:, 1]

# Create a DataFrame with team names and their probabilities
team_probabilities = pd.DataFrame({
    'Team': nba_data['Team'],
    'Probability': probabilities
})


top_three_teams = team_probabilities.sort_values(by='Probability', ascending=False).head(3)


print(top_three_teams)


# In[ ]:




