from crewai import Agent, Crew, Process, Task


class Tool:
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

    format_text_for_chat_task = Task(
        description=(
            "Format the input: {input} to make it suitable for a web chat interface. "
            "The text should be optimized for readability and include basic HTML formatting "
            "like <b>, <i>, and <br> for improved presentation."
        ),
        expected_output="A formatted string with lightweight HTML suitable for chat.",
        agent=chat_text_formatter_agent
    )

    crew = Crew(
        agents=[chat_text_formatter_agent],
        tasks=[format_text_for_chat_task],
        process=Process.sequential,
        verbose=True,
    )
