from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import SignupForm
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

@login_required
def home_view(request):
    username = request.user.username  # Get the logged-in user's username
    return render(request, 'home.html', {'username': username})

def main_page(request):
    return render(request, 'main_page.html')


def logout_view(request):
    logout(request)
    return redirect('login')

# Add these imports at the top if you haven't already
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
import joblib
import numpy as np
# Add these imports at the top if you haven't already
@login_required
def stress_predictor_view(request):
    # Load the pre-trained model and scaler (place this outside of the POST block)
    loaded_model = tf.keras.models.load_model('models/stress_prediction_model.h5')
    loaded_scaler = joblib.load('models/scaler.pkl')

    # Initialize the LabelEncoder
    label_encoder = LabelEncoder()

    if request.method == 'POST':
        # Capture form data from the user
        stress_data = {
            'name': request.POST['name'],
            'age': request.POST['age'],
            'gender': request.POST['gender'],  # 'Male' or 'Female'
            'city': request.POST['city'],
            'snoring_rate': request.POST['snoring_rate'],
            'respiratory_rate': request.POST['respiratory_rate'],
            'body_temperature': request.POST['body_temperature'],
            'limb_movements': request.POST['limb_movements'],
            'blood_oxygen': request.POST['blood_oxygen'],
            'eye_movement': request.POST['eye_movement'],
            'sleep_hours': request.POST['sleep_hours'],
            'heart_rate': request.POST['heart_rate'],
        }

        # Encode categorical 'gender' using label encoding
        gender_encoded = label_encoder.fit_transform([stress_data['gender']])[0]  # 'Male' -> 0, 'Female' -> 1

        # Prepare the input features (exclude non-essential fields like 'city' or any extra columns not used during training)
        # Ensure the correct number of features
        input_data = np.array([[ 
            stress_data['age'],
            gender_encoded,  # Encoded value of gender
            stress_data['snoring_rate'],
            stress_data['respiratory_rate'],
            stress_data['body_temperature'],
            stress_data['limb_movements'],
            stress_data['blood_oxygen'],
            stress_data['heart_rate']  # Only include 8 features as expected by the model
        ]])

        # Scale the input data using the loaded scaler
        input_data_scaled = loaded_scaler.transform(input_data)

        # Make prediction using the loaded model
        prediction = loaded_model.predict(input_data_scaled)

        # Determine the stress level based on the model's prediction
        stress_level = "Stressed" if prediction > 0.5 else "Not Stressed"

        # Pass the data and prediction result to the output page
        return render(request, 'output.html', {
            'stress_data': stress_data,
            'stress_level': stress_level
        })

    return render(request, 'stress_predictor.html')




# @login_required
# def stress_predictor_view(request):
#     if request.method == 'POST':
#         # Capture form data
#         stress_data = {
#             'name': request.POST['name'],
#             'age': request.POST['age'],
#             'gender': request.POST['gender'],
#             'city': request.POST['city'],
#             'snoring_rate': request.POST['snoring_rate'],
#             'respiratory_rate': request.POST['respiratory_rate'],
#             'body_temperature': request.POST['body_temperature'],
#             'limb_movements': request.POST['limb_movements'],
#             'blood_oxygen': request.POST['blood_oxygen'],
#             'eye_movement': request.POST['eye_movement'],
#             'sleep_hours': request.POST['sleep_hours'],
#             'heart_rate': request.POST['heart_rate'],
#         }

#         # Example logic: simple decision (modify this to integrate a ML model or logic)
#         stress_level = "Low"
#         if int(stress_data['heart_rate']) > 100 or int(stress_data['snoring_rate']) > 10:
#             stress_level = "High"

#         # Pass data to output page
#         return render(request, 'output.html', {'stress_data': stress_data, 'stress_level': stress_level})

#     return render(request, 'stress_predictor.html')
