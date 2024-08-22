#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error

# Load your data
players_df = pd.read_excel(r"C:\Users\awiga\OneDrive\Desktop\Sem 2\1.Data mining\project\data\players 1.xlsx")  # Update with the correct path

# Preprocess your data
# Filter for the 2021-2022 season and ages 18-20
young_players_2021_2022 = players_df[(players_df['Age'] >= 18) & 
                                     (players_df['Age'] <= 20) & 
                                     (players_df['Year'] == '2021-2022')]

# Convert categorical variables to dummy variables
# Assuming 'Pos' (position) is a categorical variable
young_players_2021_2022 = pd.get_dummies(young_players_2021_2022, columns=['Pos'])

# Selecting features and the target
# Remember to include the dummy variables for 'Pos' in your features
features_columns = ['PTS', 'TRB', 'AST'] + [col for col in young_players_2021_2022.columns if 'Pos_' in col]
features = young_players_2021_2022[features_columns]
target = young_players_2021_2022['PTS']  # Assuming 'PTS' as a performance metric

# Split your data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

# Initialize and train your Decision Tree model
model = DecisionTreeRegressor(random_state=42)
model.fit(X_train, y_train)

# Make predictions and evaluate your model
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

# Predict performance scores for all young players in the 2021-2022 season and find the top 5 performers
young_players_2021_2022['Predicted_Performance'] = model.predict(features)
top_5_young_players = young_players_2021_2022.sort_values('Predicted_Performance', ascending=False).head(5)

# Display the top 5 young players for the 2021-2022 season
print(top_5_young_players[['Player', 'Age', 'PTS', 'TRB', 'AST', 'Predicted_Performance']])


# In[ ]:




