from flask import Flask, render_template, request, redirect, session, send_file
import pandas as pd
import pickle
import numpy as np
import os

# ---------------- APP SETUP ---------------- #
app = Flask(__name__)
app.secret_key = "secret123"

model = pickle.load(open('model.pkl', 'rb'))

# ---------------- DATA FILE ---------------- #
DATA_FILE = "history.csv"

if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=[
        "Temperature","Vibration","Pressure","Runtime","Humidity","Prediction"
    ]).to_csv(DATA_FILE, index=False)

# ---------------- LOGIN ---------------- #
USERNAME = "admin"
PASSWORD = "1234"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['user'] = USERNAME
            return redirect('/dashboard')
    return render_template('login.html')

# ---------------- DASHBOARD ---------------- #
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('dashboard.html')

# ---------------- PREDICT ---------------- #
@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return redirect('/')

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

# ---------------- ANALYTICS ---------------- #
@app.route('/analytics')
def analytics():
    if 'user' not in session:
        return redirect('/')

    df = pd.read_csv(DATA_FILE)

    return render_template(
        "analytics.html",
        temps=list(df["Temperature"]),
        preds=list(df["Prediction"])
    )

# ---------------- DOWNLOAD ---------------- #
@app.route('/download')
def download():
    return send_file(DATA_FILE, as_attachment=True)

# ---------------- RUN ---------------- #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)