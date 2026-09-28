from backend.app.services.resume_analyzer import analyze_resume

text = """
KAMRAN AHMED
AI/ML ENGINEER
email: kamran.ahmed8277@gmail.com
phone: 03105407177

Experience
CodeCelix
AI/ML Developer
Apr 2026 – Present

• Developed AI-powered application components and backend workflows using Python.
• Built chatbot, AI automation, REST API integration, and data-processing workflows.
• Contributed to AI-powered solutions including Zaiqa Bot and Tezz Delivery.
• Implemented API and backend functionality.
• Used Git and GitHub for version control.

Digitech Offering
AI/ML Intern
Feb 2026 – Jun 2026

• Developed machine learning and deep learning solutions using Python.
• Built ML pipelines covering data preprocessing and model training.
• Developed classification and regression models.
• Built an end-to-end Titanic Survival Prediction application.

Projects
Zaiqa Bot — AI Chatbot

Skills
Python, SQL, FastAPI

Education
PMAS-Arid Agriculture University
Bachelor of Science in Computer Science
Rawalpindi, Pakistan
2021 – 2025
"""
analysis = analyze_resume(text)

print(analysis)