from flask import Flask, render_template, request
from utils.parser import extract_text_from_file
from utils.analyzer import analyze_resume

import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    # Get inputs
    resume_file = request.files.get("resume")
    jd_text = (request.form.get("jd") or "").strip()

    if not resume_file or not jd_text:
        return render_template("result.html", error="Please upload a resume and paste a job description.")

    # Save the uploaded file to a temp path
    filename = secure_filename(resume_file.filename)
    temp_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    resume_file.save(temp_path)

    try:
        resume_text = extract_text_from_file(temp_path)
    except Exception as e:
        return render_template("result.html", error=f"Could not read the file: {e}")
    finally:
        # Clean up (optional): remove uploaded file
        try:
            os.remove(temp_path)
        except Exception:
            pass

    # Analyze
    result = analyze_resume(resume_text, jd_text)

    return render_template(
        "result.html",
        score=result["score"],
        matched=result["matched"],
        missing=result["missing"],
        sample_suggestions=result["suggestions"]
    )

if __name__ == "__main__":
    # Tip: set debug=False for production
    app.run(debug=True)
