#!/usr/bin/env python

from crewai.flow.flow import Flow, listen, start, router, or_
from pydantic import BaseModel

from src.vivo.crews.aura.aura import Aura
from src.vivo.crews.multilanguage.multilanguage import Multilanguage
from src.vivo.crews.plans.plans import Plans

EXIT_MESSAGES = ['exit', 'quit']
GOODBYE_MESSAGE = "Thank you so much for contacting us! 😊 It was a pleasure helping you. If you need anything else, just reach out. I'll always be here for anything you need. 💙 See you soon!"
WELCOME_MESSAGE = "Hello! I am Aura, Vivo's virtual assistant, and I'm here to help you. 💙 Need support with your account, information about plans, or even help with technical issues? Just let me know, and together we'll find the best solution for you! 😊."
EXIT_PROMPT = "Type 'exit' to leave.\n"


class AuraState(BaseModel):
    userInput: str = "",
    auraResponse: str = "",
    topic: str = ""


class AuraFlow(Flow[AuraState]):

    @start()
    def handle_user_input(self):
        result = (
            Aura()
            .crew()
            .kickoff(inputs={"topic": self.state.userInput})
        )
        self.state.topic = result.raw

    @router(handle_user_input)
    def redirect_service(self):
        if self.state.topic in ["plans"]:
            return "plans"
        return self.state.topic

    @listen("plans")
    def process_plan(self):
        result = (
            Plans()
            .crew()
            .kickoff(inputs={"topic": self.state.userInput})
        )
        self.state.auraResponse = result.raw

    @listen(or_(redirect_service, process_plan))
    def save_dialog(self):
        result = (
            Multilanguage()
            .crew()
            .kickoff(inputs={"topic": self.state.userInput,
                             "output": self.state.auraResponse})
        )
        self.state.auraResponse = result.raw
        with open("dialog.txt", "w") as f:
            f.write("userInput:" + self.state.userInput + "\n")
            f.write("auraResponse:" + self.state.auraResponse + "\n")


def chat_mode():
    print(WELCOME_MESSAGE)
    print(EXIT_PROMPT)
    while True:
        user_input = input("User input: ").strip()
        if user_input.lower() in EXIT_MESSAGES:
            print(GOODBYE_MESSAGE)
            break
        return user_input


def kickoff():
    aura_flow = AuraFlow()
    aura_flow.kickoff()


def plot():
    aura_flow = AuraFlow()
    aura_flow.plot()


if __name__ == "__main__":
    aura_flow = AuraFlow()
    print(WELCOME_MESSAGE)
    print(EXIT_PROMPT)
    while True:
        user_input = input("User input: ").strip()
        if user_input.lower() in EXIT_MESSAGES:
            print(GOODBYE_MESSAGE)
            break
        aura_flow.kickoff(inputs={
            "userInput": user_input,
            "auraResponse": "",
            "topic": ""
        })
