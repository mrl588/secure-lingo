def get_prompt(sum):
    return f"""
    Give me a lesson focused on ONE topic on online security based on the following criteria:
        - Keep in mind the following past lessons, but do not repeat, overlap, or closely mirror any of the 
        information from them: {sum}
        - Curate the lesson for people who aren't familiar with technology.
        - Focus on possible online scams, password management, social engineering, secure browsing, phishing, etc.
        - Make the response a concise but detailed paragraph, with examples separate from the paragraphs.
        - The said examples can include case studies, statistics, historical hacks, etc. 
        - Make the tone educational and conversational.
        - Provide a checklist with key takeaways
        - Don't ask a question at the end

    After you generate the lesson, generate a multiple choice quiz based on the following criteria:
        - Produce a total of 4 questions strictly based on the information given in the lesson.
        - Each question will have 4 answers, with the answers having assigned letters a, b, c, and d in order. These letters are placed one space over to the left of the answer.
        - Be sure to store the correct answer in correct_answer.
        
    """
