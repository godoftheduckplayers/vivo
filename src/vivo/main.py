#!/usr/bin/env python

import asyncio

import websockets
from crewai.flow.flow import Flow, listen, start, router, or_
from pydantic import BaseModel

from src.vivo.crews.aura.aura import Aura
from src.vivo.crews.information.information import Information
from src.vivo.crews.optimizationmechanisms.optimizationmechanisms import OptimizationMechanisms

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
    def classified_user_intent(self):
        result = (
            Aura()
            .crew()
            .kickoff(inputs={"topic": self.state.userInput})
        )
        self.state.topic = result.raw

    @router(classified_user_intent)
    def redirect_service(self):
        if self.state.topic.__contains__("information"):
            return "information"
        return self.state.topic

    @listen("information")
    def process_information(self):
        result = (
            Information()
            .crew()
            .kickoff(inputs={"topic": self.state.userInput})
        )
        self.state.auraResponse = result.raw

    @listen(or_(process_information))
    def optimization_mechanisms(self):
        result = (
            OptimizationMechanisms()
            .crew()
            .kickoff(inputs={"topic": self.state.userInput,
                             "output": self.state.auraResponse})
        )
        self.state.auraResponse = result.raw


async def chat(websocket):
    print("Connected Client!")
    try:
        async for message in websocket:
            aura_flow = AuraFlow()
            print(f"Received message: {message}")
            await aura_flow.kickoff_async(inputs={
                "userInput": message,
                "auraResponse": "",
                "topic": ""
            })
            await websocket.send(aura_flow.state.auraResponse)
    except websockets.ConnectionClosed:
        print("Close connection!")


async def main():
    async with websockets.serve(chat, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
