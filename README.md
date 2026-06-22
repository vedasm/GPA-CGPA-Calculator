# GPA & CGPA Calculator (Streamlit)

A clean Streamlit app for calculating semester GPA and cumulative CGPA.

## Features

- GPA calculator
- CGPA calculator
- Dynamic add/remove rows
- Grade scale table
- CSV download for results

## Grade Mapping

| Grade | Points |
|-------|--------|
| O     | 10 |
| A+    | 9 |
| A     | 8 |
| B+    | 7 |
| B     | 6 |
| C     | 5 |
| P     | 4 |
| F     | 0 |

## Getting Started
 
**1. Clone the repo**
```bash
git clone https://github.com/your-username/gpa-cgpa-calculator.git
cd gpa-cgpa-calculator
```
 
**2. Install dependencies**
```bash
pip install -r requirements.txt
```
 
**3. Run the app**
```bash
streamlit run app.py
```

## Deploying to Streamlit Cloud
 
1. Push the repo to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and connect your repo
3. Set the main file to `app.py`
4. Hit Deploy — that's it