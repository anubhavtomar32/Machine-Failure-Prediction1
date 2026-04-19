# Machine Failure Prediction 🚀

A web application for predicting machine failures using machine learning. Built with Flask, scikit-learn, and Bootstrap.

## 🔧 Features
- **Machine Learning Model**: Random Forest classifier trained on sensor data
- **Web Interface**: User-friendly dashboard with Bootstrap styling
- **Authentication**: Simple login system
- **Prediction**: Input sensor values to predict failure
- **Analytics**: Visualize prediction history with charts
- **Data Export**: Download prediction history as CSV

## 📊 Dataset
The model uses the following sensor parameters from manufacturing machines:
- **Air Temperature (K)**: Ambient air temperature around the machine
- **Process Temperature (K)**: Internal process temperature during operation
- **Rotational Speed (rpm)**: Spindle or motor speed in revolutions per minute
- **Torque (Nm)**: Torque applied by the machine in Newton-meters
- **Tool Wear (min)**: Cumulative tool wear time in minutes

**Machine Type**: This system is designed for predictive maintenance of CNC milling machines, lathes, and similar industrial manufacturing equipment.

## 📝 How to Use the Prediction Form

1. **Input Real-time Sensor Data**: Enter current readings from your machine's sensors
2. **Temperature Units**: All temperatures must be in Kelvin (Celsius + 273.15)
3. **Simultaneous Readings**: Use measurements taken at the same time for accuracy
4. **Test Scenarios**: Use sample buttons to test different failure conditions

### Sample Input Scenarios:

#### ✅ Normal Operation (Should predict NO FAILURE):
- Air Temperature: 298.1 K (25°C)
- Process Temperature: 308.6 K (35.5°C)
- Rotational Speed: 1551 rpm
- Torque: 42.8 Nm
- Tool Wear: 0 min

#### ⚠️ High Torque Issue (Should predict FAILURE):
- Air Temperature: 298.9 K (26°C)
- Process Temperature: 309.0 K (36°C)
- Rotational Speed: 1410 rpm
- Torque: 65.7 Nm ← **High torque detected**
- Tool Wear: 191 min

#### 🚨 High Speed Failure (Should predict FAILURE):
- Air Temperature: 298.9 K (26°C)
- Process Temperature: 309.1 K (36°C)
- Rotational Speed: 2861 rpm ← **Abnormally high speed**
- Torque: 4.6 Nm
- Tool Wear: 143 min

#### 🔧 Tool Wear Failure (Should predict FAILURE):
- Air Temperature: 298.8 K (26°C)
- Process Temperature: 308.9 K (36°C)
- Rotational Speed: 1455 rpm
- Torque: 41.3 Nm
- Tool Wear: 208 min ← **High tool wear time**

### Understanding Results:
- **No Failure**: All parameters within normal range
- **Failure**: Specific issues identified with recommendations for action

## ▶️ How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the Model**:
   ```bash
   python model.py
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the App**:
   Open your browser and go to `http://localhost:10000`

5. **Login**:
   - Username: `admin`
   - Password: `1234`

## 🏗️ Project Structure
```
├── app.py                 # Flask application
├── model.py               # Model training script
├── requirements.txt       # Python dependencies
├── Procfile               # For deployment
├── dataset/
│   ├── machine failure.csv  # Training data
├── static/
│   └── style.css          # Custom styles
├── templates/
│   ├── login.html         # Login page
│   ├── dashboard.html     # Main dashboard
│   ├── result.html        # Prediction result
│   ├── analytics.html     # Analytics page
└── README.md
```

## 🚀 Deployment
This app can be deployed on platforms like Heroku, Render, or any Flask-compatible service.

For Heroku:
- Set `PORT` environment variable
- Use `Procfile` for process definition

## 🤝 Contributing
Feel free to submit issues and enhancement requests!