# 🩺 PredictSite

PredictSite is an educational web application that uses Machine Learning to analyze selected symptoms and provide a possible health condition along with educational information.

> ⚠️ **Disclaimer:** PredictSite is an educational project and is not a medical diagnosis or treatment system. Predictions should not be used as a substitute for professional medical advice.

## 🌐 Live Demo

https://predictsite.onrender.com

## 📌 Features

- 🔐 User Signup and Login
- 🩺 Symptom-based Machine Learning prediction
- 🤖 Random Forest classification model
- 📊 Prediction confidence indicator
- 📚 Educational information about predicted conditions
- 📜 Prediction History
- 👍👎 Prediction Feedback
- 🔑 Forgot Password functionality
- 🔎 Symptom Search
- ✅ Selected Symptoms Preview
- 🌙 Dark Pixel-Art themed interface
- 📱 Responsive design
- ⚠️ Educational health disclaimer

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- Random Forest Classifier
- Joblib

### Data Processing
- Pandas

### Deployment
- Render
- Gunicorn

## 📂 Project Structure

```text
PredictSite/
│
├── app.py
├── train_model.py
├── requirements.txt
│
├── dataset/
│   ├── Training.csv
│   └── Testing.csv
│
├── model/
│   ├── disease_model.pkl
│   └── symptoms.pkl
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── forgot_password.html
│   ├── result.html
│   └── history.html
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── background.jpg
│
├── users.json
├── prediction_history.json
└── feedback.json
```
⚙️ How It Works
```text
User
  ↓
Selects Symptoms
  ↓
Flask Backend
  ↓
Machine Learning Model
  ↓
Random Forest Prediction
  ↓
Possible Condition
  ↓
Confidence Indicator
  ↓
Educational Information
```
🤖 Machine Learning Model

PredictSite uses a Random Forest Classifier trained on a symptom-based dataset.

The training process:

Load the training and testing datasets.
Separate symptoms from the target prognosis column.
Train a Random Forest classification model.
Evaluate the model using the testing dataset.
Save the trained model using Joblib.
Save the symptom list for use by the Flask application.

Run the training script with:
```text
Bash
python train_model.py
```
The trained model is saved in:
```

model/disease_model.pkl
```
and the symptom list is saved in:
```
model/symptoms.pkl
```
💻 Installation
1. Clone the repository
```
git clone https://github.com/PalakChauhan24/PredictSite.git
```
3. Open the project directory
```
cd PredictSite
```
4. Install dependencies
```
pip install -r requirements.txt
```
5. Run the application
```
python app.py
```

The application will be available locally at:
```
http://127.0.0.1:5000
```
📦 Dependencies

The project uses:
```
Flask
Pandas
Scikit-learn
Joblib
Gunicorn
🚀 Deployment
```
PredictSite is deployed using Render with Gunicorn.

Build Command
```
Bash
pip install -r requirements.txt
```
Start Command
```
gunicorn app:app
```
🔐 User Authentication

PredictSite provides:

User registration
Secure password hashing
Login/logout
Forgot password functionality

User information is currently stored locally in JSON files for this student project.

📜 Prediction History

Logged-in users can view their previous predictions along with:

Date and time
Selected symptoms
Predicted condition
Model confidence
👍 Prediction Feedback

Users can provide feedback on predictions using:

👍 Helpful
👎 Not Helpful

This feedback is stored for the application.

🎨 User Interface

PredictSite uses a dark pixel-art inspired interface designed to provide a simple and engaging user experience.

⚠️ Disclaimer

PredictSite is developed for educational and academic purposes only.

The application provides possible health conditions based on the selected symptoms using a Machine Learning model. It does not provide medical diagnosis, medical treatment, or professional medical advice.

Users should consult a qualified healthcare professional for medical concerns.

🔮 Future Improvements

Possible future improvements include:

PostgreSQL database integration
Email-based password recovery
OTP/email verification
Improved ML models
Model performance comparison
Personalized user profiles
Cloud-based persistent storage
Improved accessibility
More comprehensive health information
👩‍💻 Author

Palak Chauhan

B.Tech Computer Science

GitHub:
https://github.com/PalakChauhan24

📄 License

This project is intended for educational and academic purposes.
