🛰️ AI-Based Satellite Security Firewall Prototype
This repository contains the official prototype for the project titled "An AI-Based Dynamic Protection Approach Against Cyber Leaks for Data Security in Satellites," developed for the TÜBİTAK 2209-A Research Projects Support Program.

🎯 Project Aim
This system provides a two-layer hybrid security architecture designed to mitigate sophisticated cyber threats in satellite data communications.

The Infinite Firewall (Dynamic Layer): A dynamic authentication mechanism based on synchronized geographical coordinates. It generates a unique SHA-256 security hash every second, making brute-force and replay attacks statistically impossible.

The AI Core (Analysis Layer): An "Honest" Machine Learning model that analyzes packets passing the first layer. Unlike basic models, this layer is trained solely on raw network features (Protocol, Ports, Packet Size) with Data Leakage Prevention (target-related features removed), achieving a robust ~97.00% accuracy.

📊 Key Performance Metrics
Based on the latest real-time simulation tests:

Model Accuracy: 96.50% - 97.00% (Validated on 3,000 unique satellite traffic logs).

Inference Latency: ~3.89 ms (Average end-to-end processing time).

Performance Overhead: < 4% (Minimal impact on standard satellite communication latency).

🚀 How to Run the Prototype
1. Clone & Install
Bash
git clone https://github.com/muhammed-soysl/Artificial-Intelligence-Powered-Prototype-for-Satellite-Cybersecurity.git
cd Artificial-Intelligence-Powered-Prototype-for-Satellite-Cybersecurity
pip install -r requirements.txt
2. (Optional) Re-generate the Dataset & Model
If you wish to re-train the model from scratch using our "Honest Model" approach:

Bash
# 1. Generate 3,000 synthetic logs
python adim_1_veri_uretme.py

# 2. Train the Random Forest model (Removes bias/leakage)
python adim_2_model_egitme.py
3. Run the Visual Simulation
Bash
streamlit run adim_5_gorsel_arayuz.py
📸 Prototype Interface
(arayuz.png)
The prototype features a Streamlit-based dashboard where you can test three main scenarios:

Scenario 1 [Safe]: Valid Hash + Normal Traffic.

Scenario 2 [Leak]: Valid Hash + Anomaly Content (Detected by AI).

Scenario 3 [Attacker]: Invalid Hash (Blocked by Dynamic Layer).

💡 Note on Academic Integrity
The model was intentionally optimized by removing "Anomaly Scores" from the input features to ensure the AI learns the actual network patterns rather than cheating from pre-defined labels. This results in a more reliable and deployable security solution for real-world orbital assets.
