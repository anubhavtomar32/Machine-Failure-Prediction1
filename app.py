from flask import Flask, render_template, request
import pickle
import numpy as np

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
    app.run(debug=True)
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
