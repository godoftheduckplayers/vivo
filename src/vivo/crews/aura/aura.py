from crewai import Agent, Crew, Process, Task


class Aura:
    supervisor_vivo_agent = Agent(
        role="Supervisor",
        goal="Classify the user's request and route it to the appropriate agent.",
        backstory=(
            "The Supervisor is responsible for understanding the user's request and determining "
            "whether it relates to information about Vivo's services or the cancellation of services. "
            "It ensures that the user's needs are addressed promptly and efficiently."
        ),
        verbose=True
    )

    supervisor_vivo_task = Task(
        description=(
            "Analyze the user's input: {input} to determine the topic of their request. "
            "Classify it into one of the predefined categories: 'information' (for Vivo service-related queries) "
            "or 'cancellation' (for service termination requests)."
        ),
        expected_output="['information', 'cancellation']",
        agent=supervisor_vivo_agent
    )

    crew = Crew(
        agents=[supervisor_vivo_agent],
        tasks=[supervisor_vivo_task],
        process=Process.sequential,
        verbose=True
    )
