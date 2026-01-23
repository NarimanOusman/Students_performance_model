# visual/views.py
import pandas as pd
from django.shortcuts import render
from pathlib import Path


# Add these imports at the top
import joblib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np

def index(request):
    """Landing page"""
    return render(request, 'visual/index.html')

def signup(request):
    return render(request, 'visual/signup.html')
    
def login(request):
    return render(request, "visual/login.html")

def logout(request):
    return render(request, "visual/logout.html")

def dashboard(request):
    BASE_DIR = Path(__file__).resolve().parent.parent
    df = pd.read_csv(BASE_DIR / 'student_data.csv', sep=',')

    # Compute metrics (0–20 scale)
    avg_g1 = round(df['G1'].mean(), 1)
    avg_g2 = round(df['G2'].mean(), 1)
    avg_g3 = round(df['G3'].mean(), 1)
    
    # Pass if G3 >= 10
    pass_rate = round((df['G3'] >= 10).mean() * 100, 1)
    total_students = len(df)

    # Insights: Study time vs Pass Rate
    study_pass = df.groupby('studytime')['G3'].apply(lambda x: (x >= 10).mean()) * 100
    study_effect = {
        'low': round(study_pass.get(1, 0), 1),
        'high': round(study_pass.get(4, 0), 1)
    }

    # Internet access impact
    internet_pass = df.groupby('internet')['G3'].apply(lambda x: (x >= 10).mean()) * 100
    internet_effect = {
        'yes': round(internet_pass.get('yes', 0), 1),
        'no': round(internet_pass.get('no', 0), 1)
    }

    context = {
        'total_students': total_students,
        'avg_g1': avg_g1,
        'avg_g2': avg_g2,
        'avg_g3': avg_g3,
        'pass_rate': pass_rate,
        'study_effect': study_effect,
        'internet_effect': internet_effect,
    }
    return render(request, 'visual/dashboard.html', context)




# Add this function BELOW your existing views
def predict(request):
    # Load model and encoders ONCE (you can cache them later)
    model = joblib.load('student_pass_model.pkl')
    label_encoders = joblib.load('label_encoders.pkl')

    if request.method == 'POST':
        # Get form data
        data = {
            'studytime': int(request.POST['studytime']),
            'failures': int(request.POST['failures']),
            'higher': request.POST['higher'],
            'internet': request.POST['internet'],
            'famrel': int(request.POST['famrel']),
            'goout': int(request.POST['goout']),
            'absences': int(request.POST['absences']),
        }

        # Encode categorical variables
        higher_encoded = label_encoders['higher'].transform([data['higher']])[0]
        internet_encoded = label_encoders['internet'].transform([data['internet']])[0]

        # Create feature array in correct order
        features = np.array([[
            data['studytime'],
            data['failures'],
            higher_encoded,
            internet_encoded,
            data['famrel'],
            data['goout'],
            data['absences']
        ]])

        # Predict probability of passing
        prob = model.predict_proba(features)[0][1]  # Probability of class "1" (pass)
        prediction = prob * 100

        return render(request, 'visual/predict.html', {'prediction': prediction})

    # GET request: show empty form
    return render(request, 'visual/predict.html')