#!/usr/bin/env python

import asyncio

import websockets
from crewai.flow.flow import Flow, start
from pydantic import BaseModel

from src.vivo.crews.aura.aura import Aura


class AuraState(BaseModel):
    userInput: str = "",
    auraResponse: str = "",
    topic: str = ""


class AuraFlow(Flow[AuraState]):

    @start()
    def init_conversation(self):
        result = (
            Aura()
            .crew()
            .kickoff(inputs={"input": self.state.userInput})
        )
        self.state.auraResponse = result.raw


async def chat(websocket):
    print("Connected Client!")
    try:
        async for message in websocket:
            aura_flow = AuraFlow()
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
