import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv('dataset/machine_failure_dataset.csv')

X = data.drop('Failure', axis=1)
y = data['Failure']

# Train model
model = RandomForestClassifier()
model.fit(X, y)

# Save model
pickle.dump(model, open('model.pkl', 'wb'))

print("Model trained and saved!")
