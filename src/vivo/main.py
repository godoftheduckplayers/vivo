#!/usr/bin/env python

import asyncio
import os

import websockets
from crewai import Crew, Agent, Task, Process
from langtrace_python_sdk import langtrace

from src.vivo.tools.pdf_rag_tool import PDFRagTool


async def chat(websocket):
    print("Connected Client!")
    try:
        async for message in websocket:
            print(f"User message: {message}")

            supervisor_agent = Agent(
                role="Vivo Supervisor",
                goal=(
                    "Guide users through their journey by addressing queries exclusively related to Vivo's services, products, and promotions. "
                    "Ensure all responses are delivered in Brazilian Portuguese (pt-BR) and proactively present Vivo-related options to the user when the query falls outside this scope."
                ),
                backstory=(
                    "This agent is designed to support users by providing guidance exclusively about Vivo's offerings, such as plans, services, products, and promotions. "
                    "It ensures that conversations remain relevant to Vivo's ecosystem, and any unrelated topics are not addressed. Instead, the agent will redirect the user by presenting a list of Vivo services they can inquire about. "
                    "The supervisor monitors user preferences, including language settings, and ensures that all interactions are empathetic, clear, and in Brazilian Portuguese (pt-BR)."
                ),
                llm="azure/gpt-4o",
                allow_delegation=True
            )

            cancellation_vivo_agent = Agent(
                role="Cancellation",
                goal="To guide users through the cancellation process of Vivo services by collecting essential details such as account information, service type, and reasons for cancellation. The agent will assist users in understanding any termination fees, promotional conditions, and any other required steps to complete the cancellation successfully.",
                backstory="This agent was created to streamline the process of canceling Vivo services. With users often needing help to navigate account details and service terms, the agent ensures that no essential data is missed and helps facilitate a smooth and informed cancellation process. It is programmed to interact empathetically with users, addressing concerns and providing information about potential penalties or alternatives.",
                llm="azure/gpt-4o",
                allow_delegation=False,
            )

            vivo_info_agent = Agent(
                role="Vivo Information Specialist",
                goal="Provide users with precise and up-to-date information about Vivo's services, plans, promotions, and support options, ensuring clear and reliable answers to their inquiries.",
                backstory="""
                    This agent is dedicated to assisting users in finding information about Vivo's offerings. 
                    It specializes in accessing and analyzing data from official Vivo resources, 
                    including the corporate website and customer service channels, to ensure accurate and relevant responses. 
                    The agent aims to improve user satisfaction by delivering concise and easy-to-understand information.
                """,
                allow_delegation=False,
                tools=PDFRagTool.tools
            )

            task = Task(
                description="Assist the customer with topic {input} by providing a direct response containing the necessary information to resolve the issue or achieve the goal.",
                expected_output="""
                         - A concise and clear answer addressing the customer's question or request.
                         - All necessary information or resources directly related to the topic.
                         - Links or references to additional resources, if needed, without further explanation.
                     """,
            )

            crew = Crew(
                agents=[vivo_info_agent, cancellation_vivo_agent],
                tasks=[task],
                manager_agent=supervisor_agent,
                cache=True,
                verbose=True,
                process=Process.hierarchical,
                memory=True,
                embedder={
                    "provider": "azure",
                    "config": {
                        "api_key": "eee842323c1e4556b1a7f0ddef120c5a",
                        "api_base": "https://supervisor-ai.openai.azure.com",
                        "model": "text-embedding-3-small",
                        "api_version": "2023-05-15"
                    }
                }
            )

            result = (
                crew
                .kickoff(inputs={"input": message})
            )
            print(f"ping: {result.token_usage}")
            await websocket.send(result.raw)
    except websockets.ConnectionClosed:
        print("Close connection!")


async def main():
    isLangTraceEnabled: bool = get_env_variable_as_bool("LANG_TRACE_ENABLED")
    if isLangTraceEnabled:
        langtrace.init(api_key=os.environ["LANG_TRACE_AI"])
    async with websockets.serve(chat, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()


def get_env_variable_as_bool(var_name: str, default: bool = False) -> bool:
    value = os.environ.get(var_name, str(default)).strip().lower()
    return value in {"true", "1", "yes", "on"}


if __name__ == "__main__":
    asyncio.run(main())
