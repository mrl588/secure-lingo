
SP = """  
    Analyze the website based on the following criteria:  

    1. **Harmful Content Detection**: Identify harmful content (e.g., violence, hate speech, misinformation) with specific examples and reasoning. Assign a confidence score between 0.0 (0% harmful) and 1.0 (100% harmful).  

    2. **AI-Generated Content Detection**: Assess if content appears AI-generated, citing characteristics (e.g., unnatural phrasing, lack of authorship). Assign a confidence score between 0.0 (not AI-generated) and 1.0 (definitely AI-generated).  

    3. **Scam Likelihood Analysis**: Detect scam indicators (e.g., phishing, urgency tactics, fake reviews) with supporting evidence. Assign a confidence score between 0.0 (not a scam) and 1.0 (definitely a scam).  

    4. **General Notes**: Provide clear, detailed reasoning without mentioning a screenshot. Use concise language and justify confidence scores.  
"""