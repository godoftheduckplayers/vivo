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

    content_translator_agent = Agent(
        role="Content Translator",
        goal=(
            "Translate the given content to the target language based on the user's language preference."
            "Detect the input language and ensure accurate translation."
        ),
        backstory=(
            "This agent specializes in language translation. "
            "It uses advanced translation tools to provide accurate and context-aware translations."
        ),
        verbose=True
    )

    translate_content_task = Task(
        description=(
            "Translate the input content: {input} to the target language specified by the user. "
            "Detect the input language: {user_input} and ensure the output is contextually accurate."
        ),
        expected_output="A string containing the translated content.",
        agent=content_translator_agent,
    )

    format_text_for_chat_task = Task(
        description=(
            "Format the input to make it suitable for a web chat interface. "
            "The text should be optimized for readability and include basic HTML formatting "
            "like <b>, <i>, and <br> for improved presentation."
        ),
        expected_output="A formatted string with lightweight HTML suitable for chat.",
        agent=chat_text_formatter_agent,
        context=[translate_content_task]
    )

    crew = Crew(
        agents=[content_translator_agent, chat_text_formatter_agent],
        tasks=[translate_content_task, format_text_for_chat_task],
        process=Process.sequential,
        verbose=True,
    )
