# utils/analyzer.py
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk import word_tokenize
import re

def _ensure_nltk():
    """
    Download NLTK data on first run (silent if already present).
    """
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", quiet=True)

    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords", quiet=True)

def _normalize(text: str):
    """
    Lowercase, tokenize, remove stopwords/non-alpha, and stem.
    Returns (stems_set, mapping stem->original words for nicer display).
    """
    _ensure_nltk()
    sw = set(stopwords.words("english"))
    stemmer = PorterStemmer()

    # Tokenize and keep alphabetic tokens
    tokens = [t.lower() for t in word_tokenize(text)]
    tokens = [re.sub(r"[^a-z]", "", t) for t in tokens]
    tokens = [t for t in tokens if t and t not in sw and len(t) > 2]

    stems = set()
    stem_to_words = {}

    for t in tokens:
        s = stemmer.stem(t)
        stems.add(s)
        stem_to_words.setdefault(s, set()).add(t)

    return stems, stem_to_words

def _pretty_words(stem_set, stem_to_words, limit=None):
    """
    Convert stems back to readable words (pick a representative for each stem).
    """
    words = []
    for s in stem_set:
        rep = sorted(stem_to_words.get(s, {s}))[0]
        words.append(rep)
    words = sorted(set(words))
    if limit:
        words = words[:limit]
    return words

def analyze_resume(resume_text: str, jd_text: str):
    """
    Simple ATS-style comparison:
    - Normalize (stopword removal + stemming)
    - Overlap between JD keywords and resume terms
    - Score = matched / JD_keywords * 100
    """
    resume_stems, resume_map = _normalize(resume_text)
    jd_stems, jd_map = _normalize(jd_text)

    if not jd_stems:
        return {
            "score": 0.0,
            "matched": [],
            "missing": [],
            "suggestions": ["Paste a longer job description to get meaningful results."]
        }

    matched = jd_stems.intersection(resume_stems)
    missing = jd_stems.difference(resume_stems)

    score = round((len(matched) / max(1, len(jd_stems))) * 100, 2)

    matched_words = _pretty_words(matched, jd_map)
    missing_words = _pretty_words(missing, jd_map)

    suggestions = []
    if score < 70:
        suggestions.append("Consider adding role-related keywords in your resume summary and skills section.")
    if missing_words:
        suggestions.append("Try to include these relevant keywords if you have experience with them: " +
                           ", ".join(missing_words[:12]) + ("..." if len(missing_words) > 12 else ""))

    return {
        "score": score,
        "matched": matched_words,
        "missing": missing_words,
        "suggestions": suggestions or ["Great match!"]
    }
