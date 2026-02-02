# 🛰️ AI-Based Satellite Security Firewall Prototype

Official prototype for the TÜBİTAK 2209-A Research Projects Support Program. Project Title: "An AI-Based Dynamic Protection Approach Against Cyber Leaks for Data Security in Satellites"

🎯 Project Aim
This system provides a two-layer hybrid security architecture designed to mitigate sophisticated cyber threats in satellite data communications.

1. The Infinite Firewall (Dynamic Layer)
A dynamic authentication mechanism based on synchronized geographical coordinates. It generates a unique SHA-256 security hash every second, making brute-force and replay attacks statistically impossible.

2. The AI Core (Analysis Layer)
An "Honest" Machine Learning model that analyzes packets passing the first layer.

Features: Trained solely on raw network features (Protocol, Ports, Packet Size).

Method: Data Leakage Prevention (target-related features removed).

Performance: Achieving a robust ~97.00% accuracy.
 

<img width="772" height="280" alt="image" src="https://github.com/user-attachments/assets/ada247cd-d51e-4c57-8485-cbca8b9901e9" />

 

🚀 How to Run the Prototype
1️⃣ Clone & Install
Bash
## Clone the repository
git clone https://github.com/muhammed-soysl/Artificial-Intelligence-Powered-Prototype-for-Satellite-Cybersecurity.git

## Enter the directory
cd Artificial-Intelligence-Powered-Prototype-for-Satellite-Cybersecurity

## Install dependencies
pip install -r requirements.txt

2️⃣ (Optional) Re-generate the Dataset & Model
If you wish to re-train the model from scratch using our "Honest Model" approach:

Bash
## 1. Generate 3,000 synthetic logs
python adim_1_veri_uretme.py

## 2. Train and save the AI model
python adim_2_model_egitme.py

3️⃣ Run the Visual Simulation
Bash
streamlit run adim_5_gorsel_arayuz.py

📸 Prototype Interface
<p align="center"> <img width="90%" alt="arayuz" src="https://github.com/user-attachments/assets/6195b305-7d65-4dee-b216-f280140deedc" /> </p>

The prototype features a Streamlit-based dashboard to test three main scenarios:

Scenario 1 [Safe]: Valid Hash + Normal Traffic.

Scenario 2 [Leak]: Valid Hash + Anomaly Content (Detected by AI).

Scenario 3 [Attacker]: Invalid Hash (Blocked by Dynamic Layer).

💡 Note on Academic Integrity
[!IMPORTANT] The model was intentionally optimized by removing "Anomaly Scores" from the input features. Bu sayede yapay zeka hazır etiketlerden kopya çekmek yerine gerçek ağ örüntülerini öğrenmeye zorlanmıştır. This results in a more reliable and deployable security solution for real-world orbital assets.
