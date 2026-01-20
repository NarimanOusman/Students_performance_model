# train_model.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
import joblib

# Load the new dataset
df = pd.read_csv('student_data.csv', sep=',')

# Define target: pass if G3 >= 10
df['passed'] = (df['G3'] >= 10).astype(int)
y = df['passed']

# Select relevant features
feature_columns = [
    'studytime',      # Weekly study time (1-4)
    'failures',       # Number of past failures (0-3)
    'higher',         # Wants higher education? (yes/no)
    'internet',       # Has internet? (yes/no)
    'famrel',         # Family relationship (1-5)
    'goout',          # Going out with friends (1-5)
    'absences'        # Number of absences
]

X = df[feature_columns].copy()

# Handle missing values (if any)
X = X.fillna(0)

# Encode categorical variables
label_encoders = {}
for col in ['higher', 'internet']:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# Train model
model = LogisticRegression(random_state=42, max_iter=200)
model.fit(X, y)

# Save model and encoders
joblib.dump(model, 'student_pass_model.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')

print("✅ Model trained on student_data.csv!")
print(f"Pass rate: {y.mean():.1%}")
print(f"Features used: {list(X.columns)}")