from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import LoginForm, RegistrationForm
from .models import User
from . import db, bcrypt
from flask_login import login_user, login_required, logout_user, current_user
import pickle
import numpy as np
import pandas as pd
import sklearn
import os
from datetime import datetime


main = Blueprint('main', __name__)

# Get the directory where this script resides
basedir = os.path.abspath(os.path.dirname(__file__))

# Adjust the path to the pickle files based on the directory of this script
model_path = os.path.join(basedir, 'model.pkl')
scaler_path = os.path.join(basedir, 'standscaler.pkl')
minmaxscaler_path = os.path.join(basedir, 'minmaxscaler.pkl')

model = pickle.load(open(model_path, 'rb'))
sc = pickle.load(open(scaler_path, 'rb'))
mx = pickle.load(open(minmaxscaler_path, 'rb'))

def get_greeting():
    current_time = datetime.now().time()
    if current_time < datetime.strptime('12:00:00', '%H:%M:%S').time():
        return "Good morning"
    elif current_time < datetime.strptime('18:00:00', '%H:%M:%S').time():
        return "Good afternoon"
    else:
        return "Good evening"


@main.route('/')
def home():
    return render_template('home.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
    return render_template('login.html', form=form)


@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    greeting = get_greeting()
    return render_template('dashboard.html', first_name=current_user.first_name, greeting=greeting)


@main.route("/predict", methods=['POST'])
def predict():
        N = request.form['Nitrogen']
        P = request.form['Phosporus']
        K = request.form['Potassium']
        temp = request.form['Temperature']
        humidity = request.form['Humidity']
        ph = request.form['Ph']
        rainfall = request.form['Rainfall']

        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)

        mx_features = mx.transform(single_pred)
        sc_mx_features = sc.transform(mx_features)
        prediction = model.predict(sc_mx_features)

        crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                    8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                    14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                    19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

        if prediction[0] in crop_dict:
            crop = crop_dict[prediction[0]]
            result = "{} is the best crop to be cultivated right there".format(crop)
        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
            
        greeting =get_greeting()    
        return render_template('dashboard.html',result = result, first_name=current_user.first_name, greeting=greeting)


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route('/crops', methods=['GET','POST'])
def crops():
    return render_template('crops.html')