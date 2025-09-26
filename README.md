# 🤖 AI-Powered Resume Analyzer + Job Role Matcher 💼

## 📌 Project Overview
The **AI-Powered Resume Analyzer** is a web application that allows users to **upload their resume (PDF/DOCX)** and automatically:
- Extracts key information (skills, education, experience).  
- Analyzes the resume using **Natural Language Processing (NLP)**.  
- Matches the candidate with the most suitable **job roles**.  

This project combines **Machine Learning, NLP, and Flask Web Development** into a practical and useful tool for students and job seekers.  

---

## 🚀 Features
- 📂 Upload resume (PDF/DOCX).  
- 🧠 Extracts keywords (skills, degrees, roles) using **NLP**.  
- 🎯 Matches candidate profile with predefined job roles.  
- 📊 Displays similarity scores and best-fit roles.  
- 🌐 Deployed as a Flask web application with a simple UI.  

---

## 🛠️ Tech Stack
- **Python** (core logic)  
- **Flask** (backend framework)  
- **HTML, CSS, JS** (frontend)  
- **spaCy / NLTK** (for NLP feature extraction)  
- **scikit-learn / XGBoost** (ML classification & matching)  
- **pandas & numpy** (data handling)  
- **SQLite / CSV** (for storing job roles & mappings)  

---

## 📂 Project Structure
resume-analyzer/
│── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── utils.py
│   ├── nlp_pipeline.py
│
│── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── images/logo.png
│
│── templates/
│   ├── index.html
│   └── result.html
│
│── data/job_roles.csv
│   └── sample_resumes/
│
│── models/model.pkl
│   └── vectorizer.pkl
│
│── notebooks/resume_analysis.ipynb
│── train_model.py
│── app.py
│── utils.py
│── requirements.txt
│── README.md
│── .gitignore

