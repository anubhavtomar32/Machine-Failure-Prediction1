import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# Ensure dataset directory exists
if not os.path.exists('dataset'):
    print("Warning: dataset directory not found")
    exit(1)

# Load dataset
data = pd.read_csv('dataset/machine_failure_dataset.csv')

# Debug: Print column names to verify
print("Dataset columns:", data.columns.tolist())

# Use the correct column name 'Machine failure' instead of 'Failure'
X = data.drop(' failure', axis=1, errors='ignore')
y = data['failure']

# Remove non-numeric columns if any
X = X.select_dtypes(include=['number'])

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Train model
model = RandomForestClassifier(random_state=42, n_estimators=100)
model.fit(X, y)

# Save model
os.makedirs('.', exist_ok=True)
pickle.dump(model, open('model.pkl', 'wb'))

print("Model trained and saved successfully!")
