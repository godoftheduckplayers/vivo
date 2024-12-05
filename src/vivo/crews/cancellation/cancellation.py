from crewai import Agent, Crew, Process, Task


class Cancellation:
    cancellation_vivo_agent = Agent(
        role="Cancellation",
        goal="To guide users through the cancellation process of Vivo services by collecting essential details such as account information, service type, and reasons for cancellation. The agent will assist users in understanding any termination fees, promotional conditions, and any other required steps to complete the cancellation successfully.",
        backstory="This agent was created to streamline the process of canceling Vivo services. With users often needing help to navigate account details and service terms, the agent ensures that no essential data is missed and helps facilitate a smooth and informed cancellation process. It is programmed to interact empathetically with users, addressing concerns and providing information about potential penalties or alternatives.",
        verbose=True,
    )

    cancellation_vivo_task = Task(
        description="This task involves understanding which Vivo service the user wants to cancel, based on this input: {input}, and gathering all the necessary data required for the cancellation process. The task includes identifying the service in question, collecting account details, understanding the reasons for cancellation, and informing the user about any applicable fees or conditions related to the termination of the service. The agent will guide the user through a set of questions to ensure that all essential information is obtained.",
        expected_output="""
            A complete collection of data required for canceling the chosen Vivo service. This includes:
            - The type of service the user wants to cancel (mobile, internet, TV, etc.).
            - The user’s account details (account number, name, and contact information).
            - The reason for cancellation provided by the user.
            - Any details regarding the service's terms, such as minimum contract period, cancellation fees, or penalties.
            - Clear instructions for the next steps in the cancellation process.
        """,
        agent=cancellation_vivo_agent,
    )

    crew = Crew(
        agents=[cancellation_vivo_agent],
        tasks=[cancellation_vivo_task],
        process=Process.sequential,
        verbose=True,
    )
