import os
import json
import google.generativeai as genai
from pymongo import MongoClient
from prompt import get_prompt

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

prompt_to_json_model = genai.GenerativeModel(
    "gemini-2.0-flash", generation_config={"response_mime_type": "application/json"})


client = MongoClient(os.getenv("MONGODB_URI"))
db = client.get_database('SecurityFilterDb')
lessons_collection = db.get_collection('Lesson')


def fetch_past_lessons():
    Lesson = []
    for lesson in lessons_collection.find():
        Lesson.append(lesson.get('content', ''))
    return Lesson


def generate_lessons():

    past_lessons = fetch_past_lessons()

    formatted_lessons = "\n".join([lesson for lesson in past_lessons])

    prompt = get_prompt(formatted_lessons)

    response = prompt_to_json_model.generate_content(prompt)
    lesson = json.loads(response.text)

    lesson_document = {
        "lesson": json.dumps(lesson)
    }

    lessons_collection.insert_one(lesson_document)

    return lesson


print(generate_lessons())