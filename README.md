# ❤️ Heart Disease Predictor

A Machine Learning-based web application that predicts the risk of heart disease from patient health and heart-related parameters.

The project uses **Logistic Regression** to make predictions and **Streamlit** to provide an interactive web interface where users can enter patient details and get an instant risk prediction.

## 🚀 Features

* Patient health information input
* Heart disease risk prediction using Machine Learning
* Logistic Regression model
* Feature scaling using StandardScaler
* Interactive Streamlit dashboard
* Risk probability visualization
* Input summary for the entered patient data
* Clean and responsive user interface

## 🧠 Machine Learning

The model uses parameters such as:

* Age
* Sex
* Chest Pain Type
* Resting Blood Pressure
* Cholesterol
* Fasting Blood Sugar
* Resting ECG
* Maximum Heart Rate
* Exercise-Induced Angina
* Oldpeak
* ST Slope

### Workflow

**Data → Data Cleaning → Encoding → Feature Scaling → Model Training → Model Evaluation → Model Saving → Streamlit Deployment**

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Joblib
* Streamlit
* Matplotlib / Seaborn
* Jupyter Notebook

## 📂 Project Structure

```text
Heart-Disease-Predictor/
│
├── files/
│   └── app.py
│
├── heart.csv
├── LR_heart.pkl
├── heart_scaler.pkl
├── heart_columns.pkl
├── hearta.ipynb
└── README.md
```

## ▶️ Run Locally

Install the required dependencies:

```bash
pip install streamlit pandas numpy scikit-learn joblib
```

Run the application:

```bash
python -m streamlit run files/app.py
```

The application will open in your browser.

## ⚠️ Disclaimer

This project is created for **educational and demonstration purposes only**. The prediction should not be considered a medical diagnosis or a replacement for professional medical advice.
