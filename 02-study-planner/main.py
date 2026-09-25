# main.py

from agent import Agent

agent = Agent()


while True:
    message = input("You: ")
    if message.lower() in ["quit", "exit"]:
        break
    elif message == "/reset":
        agent.reset()
        continue
    elif message == "/help":
        print('''
/reset: reset the conversation history
/topics: list all topics
''')
        continue
    elif message == "/topics":
        agent.get_topic()
        continue
    agent.chat(message)