🧠 KeyMood AI – Keystroke Emotion Detection (Federated Learning)

KeyMood AI is a minor project that detects a user’s emotional state using keystroke dynamics (typing behavior).
Instead of using camera or microphone, the system analyzes typing patterns such as speed, delays, and error rate to predict emotions like Happy, Calm, Neutral, and Stressed.

This project also includes the concept of Federated Learning, where models can improve collaboratively without sharing raw user data.

🚀 Features
🔐 Login System (Session-based Authentication)
⌨️ Emotion Detection using Keystroke Behavior
📊 Dashboard with Prediction History & Visualizations
🧠 Machine Learning based Emotion Prediction
🌐 Federated Learning Concept (Global Model Aggregation)
🎨 Modern Streamlit UI with animations and smooth navigation
🛡️ Privacy Focus

This project is designed with privacy in mind:

Typed text content is not stored
Only behavioral features are used (timing patterns)
Supports privacy-preserving learning using federated approach
🧩 Technologies Used
Python
Streamlit
Scikit-learn
Pandas / NumPy
Federated Learning (simulation based aggregation)
Pickle (model saving/loading)
📂 Project Structure
FederatedEmotion/
│── app.py
│── pages/
│   │── 1_Login.py
│   │── 2_Home.py
│   │── 3_Emotion_Detection.py
│   │── 4_About.py
│   │── 5_Dashboard.py
│── data/
│   │── raw/
│   │── processed/
│── member1_data/
│── member2_features/
│── member3_model/
│── member4_federated/
│── local_model.pkl
│── global_model.pkl
│── prediction_history.csv
│── predict_emotion.py
⚙️ How to Run the Project
1️⃣ Install Dependencies

Make sure Python is installed, then run:

pip install -r requirements.txt

(If requirements file is not created, install manually: streamlit, pandas, numpy, scikit-learn)

2️⃣ Run the Streamlit App

Go inside project folder and run:

streamlit run FederatedEmotion/app.py
👤 Demo Login Credentials
User ID	Password
admin	admin123
user1	1234
user2	1234
user3	1234
📌 Output Emotions

The model predicts emotions based on typing patterns:

😊 Happy
😌 Calm
😐 Neutral
😰 Stressed
📊 Dashboard

The dashboard provides:

prediction history tracking
emotion count visualization
trend analysis graphs
🌐 Federated Learning Concept

This project includes federated learning simulation where:

multiple clients train locally
only model updates are shared
global model is generated using aggregation

This improves performance without exposing user data.

📌 Project Objective

To create a low-cost and privacy-preserving system that can detect human emotions using only typing behavior, without using camera or biometric sensors.

📜 License

This project is created for academic/minor project purposes.
