#!/usr/bin/env python

import asyncio
import os

import websockets
from crewai import Crew, Agent, Task, Process
from langtrace_python_sdk import langtrace

from src.vivo.tools.cancel_tool import CancelTool
from src.vivo.tools.pdf_rag_tool import PDFRagTool

cancellation_tool = CancelTool()

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
    respect_context_window=True,
)

cancellation_vivo_agent = Agent(
    role="Cancellation",
    goal="Collect the user's data (email and CPF) to perform the cancellation procedure, use a tool to send this data via API, and ensure the user receives cancellation confirmation and best practices tips, only if all required data has been collected.",
    backstory="This agent is responsible for assisting with service cancellations, ensuring that the necessary data is securely collected and correctly sent via an API.",
    llm="azure/gpt-4o",
    allow_delegation=True,
    tools=[cancellation_tool],
    tools_results=[{"email": "email", "cpf": "cpf"}]
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
    agent=cancellation_vivo_agent
)

crew = Crew(
    agents=[vivo_info_agent, cancellation_vivo_agent],
    tasks=[task],
    # manager_agent=supervisor_agent,
    cache=True,
    verbose=True,
    # process=Process.hierarchical,
    process=Process.sequential,
    memory=True,
    share_crew=True,
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


async def chat(websocket):
    print("Connected Client!")
    try:
        async for message in websocket:
            print(f"User message: {message}")
            print(f"Crew ID: {crew.id}")
            result = await (
                crew
                .kickoff_async(inputs={"input": message})
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
