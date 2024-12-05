#!/usr/bin/env python

import asyncio

import websockets
from crewai.flow.flow import Flow, start, listen
from pydantic import BaseModel

from src.vivo.crews.aura.aura import Aura
from src.vivo.crews.cancellation.cancellation import Cancellation
from src.vivo.crews.information.information import Information
from src.vivo.crews.tool.tool import Tool

crews = {
    "information": {
        "crew": Information().crew,
        "after_kickoff": [
            Tool().crew
        ]
    },
    "cancellation": {
        "crew": Cancellation().crew,
        "after_kickoff": [
            Tool().crew
        ]
    }
}


class AuraState(BaseModel):
    userInput: str = "",
    auraResponse: str = "",
    crew: str = ""


class AuraFlow(Flow[AuraState]):

    @start()
    def classification(self):
        result = (
            Aura()
            .crew
            .kickoff(inputs={"input": self.state.userInput})
        )
        self.state.crew = result.raw

    @listen(classification)
    def process(self):
        result = (
            crews[self.state.crew]['crew']
            .kickoff(inputs={"input": self.state.userInput})
        )
        self.state.auraResponse = result.raw

    @listen(process)
    def after_kickoff(self):
        crew = crews[self.state.crew]
        for after in crew['after_kickoff']:
            result = (
                after
                .kickoff(inputs={"input": self.state.auraResponse,
                                 "user_input": self.state.userInput})
            )
            self.state.auraResponse = result.raw


async def chat(websocket):
    print("Connected Client!")
    try:
        async for message in websocket:
            aura_flow = AuraFlow()
            print(f"User message: {message}")
            await aura_flow.kickoff_async(inputs={
                "userInput": message,
                "auraResponse": "",
                "crew": ""
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
