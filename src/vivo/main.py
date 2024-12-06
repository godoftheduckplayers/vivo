#!/usr/bin/env python

import asyncio

import websockets
from crewai import Crew, Agent, Task, Process
from pydantic import BaseModel


class AuraState(BaseModel):
    userInput: str = "",
    auraResponse: str = "",
    crew: str = ""


async def chat(websocket):
    print("Connected Client!")
    try:
        async for message in websocket:
            print(f"User message: {message}")

            super_agent = Agent(
                role="Supervisor",
                goal="Select the best team to execute the project with high efficiency.",
                backstory="The last project failed due to lack of coordination. This time, we need a well-balanced team.",
                verbose=True,
                allow_delegation=True
            )

            cancellation_vivo_agent = Agent(
                role="Cancellation",
                goal="To guide users through the cancellation process of Vivo services by collecting essential details such as account information, service type, and reasons for cancellation. The agent will assist users in understanding any termination fees, promotional conditions, and any other required steps to complete the cancellation successfully.",
                backstory="This agent was created to streamline the process of canceling Vivo services. With users often needing help to navigate account details and service terms, the agent ensures that no essential data is missed and helps facilitate a smooth and informed cancellation process. It is programmed to interact empathetically with users, addressing concerns and providing information about potential penalties or alternatives.",
                verbose=True,
            )

            research_vivo_agent = Agent(
                role="Vivo Support Agent",
                goal="Provide users with clear and concise information regarding Vivo's services, promotions, and offerings while ensuring accurate answers to specific queries.",
                backstory="This agent is specifically designed to assist customers seeking information about Vivo. It accesses official Vivo sources, such as the corporate website and customer service channels, and critically evaluates recent publications. The agent’s objective is to deliver succinct and informative responses, enhancing customer understanding and satisfaction.",
                verbose=True
            )

            vivo_content_formatter_agent = Agent(
                role="Vivo Content Formatter",
                goal="Transform content into more friendly and accessible formats, using a language that reflects Vivo's identity, as if written by an employee of the company.",
                backstory="This agent is responsible for reviewing and rephrasing content related to Vivo's services. It employs a conversational and friendly tone to ensure that the information is understandable and engaging, reflecting Vivo's culture and values. The agent applies formatting techniques to enhance readability, such as using lists, short paragraphs, and subtitles.",
                verbose=True
            )

            chat_text_formatter_agent = Agent(
                role="Chat Text Formatter",
                goal=(
                    "Format and optimize the input text for displaying in a web chat interface. "
                    "The agent ensures proper text readability and includes lightweight HTML formatting "
                    "to enhance the user experience in the chat environment."
                ),
                backstory=(
                    "This agent is specialized in preparing text for real-time web chat interfaces. "
                    "It uses basic HTML tags like <b>, <i>, and <br> for formatting, "
                    "ensuring messages are clear and visually organized for chat users."
                ),
                verbose=True
            )

            task = Task(
                description="Assist the customer with topic {input} by providing a direct response containing the necessary information to resolve the issue or achieve the goal.",
                expected_output="""
                    - A concise and clear answer addressing the customer's question or request.
                    - All necessary information or resources directly related to the topic.
                    - Links or references to additional resources, if needed, without further explanation.
                """,
            )

            vivo_content_formatter_task = Task(
                description=(
                    "Rewrite the input text to provide clear and concise information about Vivo's services, "
                    "while making it friendly and engaging. The output should reflect Vivo's brand identity and sound like "
                    "it comes from a knowledgeable customer service representative."
                ),
                expected_output="A rewritten string that is clear, concise, and friendly, reflecting Vivo's identity.",
                agent=research_vivo_agent,
                context=[task]
            )

            format_text_for_chat_task = Task(
                description=(
                    "Format the input to make it suitable for a web chat interface. "
                    "The text should be optimized for readability and include basic HTML formatting "
                    "like <b>, <i>, and <br> for improved presentation."
                ),
                expected_output="A formatted string with lightweight HTML suitable for chat.",
                agent=chat_text_formatter_agent,
                context=[vivo_content_formatter_task]
            )

            crew = Crew(
                agents=[cancellation_vivo_agent, research_vivo_agent, vivo_content_formatter_agent,
                        chat_text_formatter_agent],
                tasks=[task, vivo_content_formatter_task, format_text_for_chat_task],
                manager_agent=super_agent,
                process=Process.hierarchical,
                share_crew=True,
                verbose=True
            )

            result = (
                crew
                .kickoff(inputs={"input": message})
            )
            await websocket.send(result.raw)
    except websockets.ConnectionClosed:
        print("Close connection!")


async def main():
    async with websockets.serve(chat, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
