# Resume-Analyzer-project
ATS Resume Analyzer using Python & Flask
# Resume Analyzer (ATS Checker)

A simple ATS (Applicant Tracking System) Resume Analyzer built with Python, Flask, and NLP.
This tool helps job seekers check how well their resume matches a given job description by highlighting ATS score, matched keywords, and missing keywords.
# Features

- Upload PDF/DOCX/TXT resumes
- Paste any Job Description (JD)
- Get an ATS Score (%) instantly
- See matched keywords between resume & JD
- Identify missing keywords to improve resume
- Suggestions to increase ATS score
- Simple web interface built with Flask
# Tech Stack

-Backend: Python, Flask
-NLP: NLTK (tokenization, stopword removal, stemming)
-Frontend: HTML, CSS (Flask Templates)
-File Handling: PyPDF2, docx2txt
# Installation & Usage
1️⃣ Clone Repository
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer

2️⃣ Setup Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows
OR
source venv/bin/activate   # Mac/Linux

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Application
python app.py

Open your browser → http://127.0.0.1:5000/
# Sample Output
![Home Page](screenshots/home.png)
![Result Page](screenshots/result.png)
# Future Improvements

- Add charts/visualizations for ATS score
- Export analysis as PDF report
- Weight keywords based on importance (skills > soft skills)
- Deploy to Render/Heroku for public access
