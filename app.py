from flask import send_file
import pandas as pd

DATA_FILE = "history.csv"

# Create file if not exists
try:
    pd.read_csv(DATA_FILE)
except:
    pd.DataFrame(columns=["Temperature","Vibration","Pressure","Runtime","Humidity","Prediction"]).to_csv(DATA_FILE, index=False)


app.route('/predict', methods=['POST'])
def predict():
    features = [float(x) for x in request.form.values()]
    prediction = model.predict([np.array(features)])
    result = "Failure" if prediction[0] == 1 else "No Failure"

    # Save data
    df = pd.read_csv(DATA_FILE)
    new_row = {
        "Temperature": features[0],
        "Vibration": features[1],
        "Pressure": features[2],
        "Runtime": features[3],
        "Humidity": features[4],
        "Prediction": result
    }
    df = pd.concat([df, pd.DataFrame([new_row])])
    df.to_csv(DATA_FILE, index=False)

    return render_template('result.html', prediction_text=result)


@app.route('/analytics')
def analytics():
    df = pd.read_csv(DATA_FILE)

    return render_template(
        "analytics.html",
        temps=list(df["Temperature"]),
        preds=list(df["Prediction"])
    )


@app.route('/download')
def download():
    return send_file(DATA_FILE, as_attachment=True)
    from flask import Flask, render_template, request, redirect, session
import pickle, numpy as np, os

app = Flask(__name__)
app.secret_key = "secret123"

model = pickle.load(open('model.pkl', 'rb'))

# Dummy login
USERNAME = "admin"
PASSWORD = "1234"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['user'] = USERNAME
            return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    features = [float(x) for x in request.form.values()]
    prediction = model.predict([np.array(features)])
    result = "Failure Likely" if prediction[0] == 1 else "No Failure"
    return render_template('result.html', prediction_text=result)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
