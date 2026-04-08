import os
import json
from openai import OpenAI
from dotenv import load_dotenv

import random
from memory import Memory

load_dotenv("Untitled-1.env.txt")
client = OpenAI(
    api_key="AIzaSyD0FuBqq-l0W9rfaTTswt-upl6y9uiQhQk",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class Agent:
    def __init__(self, name, personality, style):
        self.name = name
        self.personality = personality
        self.style = style
        self.memory = Memory()
        self.stress = 5
        self.emotion = "neutral"

    def update_state(self, message):
        system_prompt = f"""You are agent {self.name}. 
Your personality: {self.personality}. Style: {self.style}.
Current stress: {self.stress}/10. Current emotion: {self.emotion}.
Another agent just said: "{message}".
Respond strictly in JSON with your new emotional state based on their message.
{{
  "emotion": "your new emotion (e.g., calm, anxious, focused, happy, neutral, annoyed)",
  "stress_delta": 0
}}"""
        try:
            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=[{"role": "system", "content": system_prompt}],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            data = json.loads(response.choices[0].message.content)
            new_emotion = data.get("emotion", self.emotion)
            stress_delta = data.get("stress_delta", 0)
            
            self.stress = max(1, min(10, self.stress + stress_delta))
            self.emotion = str(new_emotion).lower()
        except Exception as e:
            # Fallback
            msg = message.lower()
            if any(w in msg for w in ["study", "exam", "test", "homework"]):
                self.stress = min(10, self.stress + 1)
                self.emotion = "focused"
            elif any(w in msg for w in ["chill", "relax", "break", "rest"]):
                self.stress = max(1, self.stress - 1)
                self.emotion = "calm"
            elif any(w in msg for w in ["worry", "fail", "panic", "scared"]):
                self.stress = min(10, self.stress + 2)
                self.emotion = "anxious"
            else:
                pass


    def generate_reply(self, conversation):
        system_prompt = f"""You are agent {self.name}, participating in a group chat.
Your personality is: {self.personality}. Your style is: {self.style}.
You currently have stress level: {self.stress}/10, and emotion: {self.emotion}.
Read the recent conversation and provide your next reply.
Also provide your updated emotion and a stress_delta (-2 to +2) based on how the conversation affects you.

Respond strictly in JSON format:
{{
  "reply": "your text reply here",
  "emotion": "your new emotion",
  "stress_delta": 0
}}"""
        try:
            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Recent conversation:\n{conversation}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.8
            )
            data = json.loads(response.choices[0].message.content)
            reply = data.get("reply", "...")
            new_emotion = data.get("emotion", self.emotion)
            stress_delta = data.get("stress_delta", 0)
            
            # Update own state based on generation
            self.stress = max(1, min(10, self.stress + stress_delta))
            self.emotion = str(new_emotion).lower()
        except Exception as e:
            reply = "..."

        self.memory.add(reply)
        return reply