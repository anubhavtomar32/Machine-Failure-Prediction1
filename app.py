from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__)

# Load trained model
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    features = [float(x) for x in request.form.values()]
    final_features = [np.array(features)]
    
    prediction = model.predict(final_features)

    result = "⚠️ Failure Likely" if prediction[0] == 1 else "✅ No Failure"
    
    return render_template('result.html', prediction_text=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)                                                                                  
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
                           
