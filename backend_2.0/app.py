import os
import json
# import google.generativeai as genai
from google import genai
from pymongo import MongoClient
from prompt import get_prompt
import streamlit as st

from google import genai
from pydantic import BaseModel

from typing import List


class Quiz(BaseModel):
    question: str
    answers: list[str]
    correct_answer: str


class Result(BaseModel):
    quizes: list[Quiz]
    examples: list[str]
    checklists: List[str]
    summary: str
    title: str


client = MongoClient(os.getenv("MONGO_URL"))
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

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=get_prompt("none"),
        config={
            'response_mime_type': 'application/json',
            'response_schema': Result,
        },
    )

    lesson = json.loads(response.text)
    # lesson_document = {
    #     "lesson": json.dumps(lesson)
    # }

    # lessons_collection.insert_one(lesson_document)

    return lesson


for i in range(5):
    st.json(generate_lessons())