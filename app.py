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
        "Air Temperature (K)", "Process Temperature (K)", "Rotational Speed (rpm)", "Torque (Nm)", "Tool Wear (min)", "Prediction"
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

    try:
        features = [float(x) for x in request.form.values()]
        prediction = model.predict([np.array(features)])
        result = "Failure" if prediction[0] == 1 else "No Failure"

        # Save data
        df = pd.read_csv(DATA_FILE)
        new_row = {
            "Air Temperature (K)": features[0],
            "Process Temperature (K)": features[1],
            "Rotational Speed (rpm)": features[2],
            "Torque (Nm)": features[3],
            "Tool Wear (min)": features[4],
            "Prediction": result
        }
        df = pd.concat([df, pd.DataFrame([new_row])])
        df.to_csv(DATA_FILE, index=False)

        return render_template('result.html', 
                               prediction_text=result,
                               air_temp=features[0],
                               process_temp=features[1], 
                               rot_speed=features[2],
                               torque=features[3],
                               tool_wear=features[4])
    except Exception as e:
        return render_template('result.html', prediction_text=f"Error: {str(e)}")

# ---------------- ANALYTICS ---------------- #
@app.route('/analytics')
def analytics():
    if 'user' not in session:
        return redirect('/')

    df = pd.read_csv(DATA_FILE)

    return render_template(
        "analytics.html",
        temps=list(df["Air Temperature (K)"]),
        preds=list(df["Prediction"])
    )

# ---------------- DOWNLOAD ---------------- #
@app.route('/download')
def download():
    return send_file(DATA_FILE, as_attachment=True)

# ---------------- LOGOUT ---------------- #
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

# ---------------- RUN ---------------- #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)