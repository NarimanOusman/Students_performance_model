# visual/views.py
import pandas as pd
from django.shortcuts import render
from pathlib import Path

def index(request):
    """Landing page"""
    return render(request, 'visual/index.html')

def dashboard(request):
    """Analytics dashboard with real student data and insights"""
    BASE_DIR = Path(__file__).resolve().parent.parent
    df = pd.read_csv(BASE_DIR / 'StudentsPerformance.csv')

    # === BASIC METRICS ===
    total_students = len(df)
    avg_math = round(df['math score'].mean(), 1)
    avg_reading = round(df['reading score'].mean(), 1)
    avg_writing = round(df['writing score'].mean(), 1)

    # Define pass if >= 60 in all subjects
    df['passed'] = (df['math score'] >= 60) & (df['reading score'] >= 60) & (df['writing score'] >= 60)
    pass_rate = round(df['passed'].mean() * 100, 1)

    # === KEY INSIGHTS ===
    # 1. Test Prep Impact
    prep_pass = df.groupby('test preparation course')['passed'].mean() * 100
    prep_effect = {
        'completed': round(prep_pass.get('completed', 0), 1),
        'none': round(prep_pass.get('none', 0), 1)
    }

 

    # Lunch Type Impact
    lunch_pass = df.groupby('lunch')['passed'].mean() * 100
    lunch_effect = {
        'standard': round(lunch_pass.get('standard', 0), 1),
        'free_reduced': round(lunch_pass.get('free/reduced', 0), 1)  # ← underscore, not slash
    }

    # 3. Top Performing Groups by Race/Ethnicity
    group_pass = df.groupby('race/ethnicity')['passed'].mean().sort_values(ascending=False) * 100
    top_groups = group_pass.head(3).round(1).to_dict()

    context = {
        'total_students': total_students,
        'avg_math': avg_math,
        'avg_reading': avg_reading,
        'avg_writing': avg_writing,
        'pass_rate': pass_rate,
        'prep_effect': prep_effect,
        'lunch_effect': lunch_effect,
        'top_groups': top_groups,
    }
    return render(request, 'visual/dashboard.html', context)