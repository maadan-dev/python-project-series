# agent.py
from dotenv import load_dotenv
from groq import Groq
import os
from storage import save_history, load_history

load_dotenv()

SYSTEM_INSTRUCTION = "You are an AI study planner agent. Your job is to help user plan the topic requested. you can search the internet when its neccessary and provide materials or simply explain the concept. Act like friendly teacher, be firm when you need to and guide the user."


class Agent:
    def __init__(self):
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        self.model = "openai/gpt-oss-20b"
        loaded = load_history()
        self.history = loaded if loaded else [{"role": "system", "content": SYSTEM_INSTRUCTION}]


    def chat(self, user_message):
        try:
            self.history.append({"role": "user", "content": user_message})
            response = self.client.chat.completions.create(
                model = self.model,
                messages = self.history
            )
            
        except Exception as e:
            print(f"Error: {e}")
            return
        
        self.history.append({"role": "assistant", "content": response.choices[0].message.content})
        save_history(self.history)
        print(response.choices[0].message.content)

    def reset(self):
        self.history = [{"role": "system", "content": SYSTEM_INSTRUCTION}]
        save_history(self.history)

    def get_topic(self):
        temp_history = self.history + [{"role": "user", "content": "list the topics the user has asked about, one per line"}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=temp_history
        )
        print(response.choices[0].message.content)