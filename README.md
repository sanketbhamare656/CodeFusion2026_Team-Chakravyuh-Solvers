# 🛡️ PhishNet — AI-Powered Phishing Detection & URL Scanner Tool
![PhishNet Banner](/static/img/home.png)
PhishNet is a web-based tool designed to detect and warn users about suspicious or potentially harmful URLs. It’s part of our ongoing mission to combat phishing and online scams using intelligent automation, powered by AI and Machine Learning to analyze web content, URL behavior, and detect phishing patterns more accurately.

---

## 📖 Learn More About How PhishNet Works

🔹 [Read How PhishNet Works](README-HOW-PHISHNET-WORKS.md)  
(A complete explanation of detection methods, workflow, and internal logic.)

---
### Demo Video
- https://youtu.be/oXZewQhu7u0

### PPT (Google Drive)
- https://docs.google.com/presentation/d/1bbXIMMhH1BKsZJV8bAPLOV2QD7iQrtvU/edit?usp=sharing&ouid=113191716539863542421&rtpof=true&sd=true







---

### ScreenShots

 ![PhishNet Banner](/static/img/home-2.png) 


 ![PhishNet Banner](/static/img/home-3.png)


 ![PhishNet Banner](/static/img/home-4.png)

 ![PhishNet Banner](/static/img/home-5.png)


 ![PhishNet Banner](/static/img/home-6.png)

 ![PhishNet Banner](/static/img/home-7.png)

## 📦 How to Run the Project Locally
- The latest `top-1m.csv` can be downloaded from Tranco List(https://tranco-list.eu/) (this CSV is updated every month). 
- In this `onetimescript.py`, we read the file `/static/data/top-1m.csv`, populate data, and store it into a sorted list (`sorted-top1million.txt`) and a - - JSON file (`domain-rank.json`) for easy access while assessing URLs.

- If you want to update the list and JSON on your local machine, follow these steps:
- 1. Download the `top-1m.csv` file from Tranco List (https://tranco-list.eu/)
- 2. Copy it to the `/static/data/` directory.
- 3. Execute the `onetimescript.py` file. It takes about 10-20 seconds to execute the script.

### 🔁 Step-by-step Setup

```bash
# 1. Clone the repository
git clone https://github.com/sanketbhamare656/CodeFusion2026_Team-Chakravyuh-Solvers.git
cd phishnet

# 2. Create and activate virtual environment
python -m venv venve
source venv/bin/activate   # or on Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download Dataset Manually (important)
# Visit: https://tranco-list.eu/
# Download the latest top-1m.csv and place it in: /static/data/

# 5. Run one-time data processing
python onetimescript.py

# 6. Start the Flask app
python app.py

'''
