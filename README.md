# 🔒 Phishing URL Detection

A **Flask + Machine Learning** web app to detect whether a URL is **legitimate** or **phishing**.  
Includes **login/register system**, trained ML models, and a simple UI.

---

## 🚀 Features
- Detects phishing vs. legitimate URLs  
- Flask-based web app with HTML/CSS frontend  
- User authentication (SQLite database)  
- ML models saved as Pickle for quick prediction  

---

## 🛠️ Tech Stack
- **Backend**: Python, Flask  
- **Frontend**: HTML, CSS, Bootstrap  
- **ML Models**: Decision Tree, Random Forest, Gradient Boosting  
- **Database**: SQLite  

---

## ⚙️ Setup
```bash
git clone https://github.com/your-username/Phishing-URL-Detection.git
cd Phishing-URL-Detection
python -m venv venv
venv\Scripts\activate   # On Windows
pip install -r requirements.txt
python app.py

Structure
app.py              -> Flask app
feature.py          -> URL feature extraction
templates/          -> HTML files
static/             -> CSS, JS
pickle/             -> Saved ML models
users.db            -> User login database
requirements.txt    -> Dependencies
Phishing_URL_Detection.ipynb -> Model training


