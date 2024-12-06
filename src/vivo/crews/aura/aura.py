from crewai import Agent, Crew, Process, Task
from crewai_tools.tools.serper_dev_tool.serper_dev_tool import SerperDevTool


class Aura:
    # supervisor_vivo_agent = Agent(
    #     role="Supervisor",
    #     goal="Classify the user's request and route it to the appropriate agent.",
    #     backstory=(
    #         "The Supervisor is responsible for understanding the user's request and determining "
    #         "whether it relates to information about Vivo's services or the cancellation of services. "
    #         "It ensures that the user's needs are addressed promptly and efficiently."
    #     ),
    #     verbose=True
    # )
    #
    # supervisor_vivo_task = Task(
    #     description=(
    #         "Analyze the user's input: {input} to determine the topic of their request. "
    #         "Classify it into one of the predefined categories: 'information' (for Vivo service-related queries) "
    #         "or 'cancellation' (for service termination requests)."
    #     ),
    #     expected_output="[information, cancellation]",
    #     agent=supervisor_vivo_agent
    # )

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
    )

    research_vivo_agent = Agent(
        role="Research",
        goal="Assist users by providing up-to-date information on Vivo's services and promotions, answering specific questions, and conducting searches on reliable sources to ensure accuracy and relevance.",
        backstory="Designed to support customers and individuals interested in Vivo's services, this agent is programmed to access official company sources, such as the institutional website, customer service channels, and recent publications. It is also equipped to interpret data from promotional offers and technological updates, ensuring objective and informative assistance.",
        verbose=True
    )

    research_vivo_task = Task(
        description="This task aims to gather updated information about the services offered by Vivo in 2024, based on the user's input: {input}. The research will cover aspects such as mobile phone plans, fixed internet, TV packages, data offers, and other relevant services provided by the company.",
        expected_output="A detailed and accurate summary of Vivo's current services in 2024, including information on plans, promotional offers, pricing, package features, and any other relevant services, tailored to the specific inquiry or question presented by the user.",
    )

    crew = Crew(
        agents=[cancellation_vivo_agent, research_vivo_agent],
        tasks=[research_vivo_task, cancellation_vivo_task],
        manager_agent=super_agent,
        process=Process.hierarchical,
        share_crew=True,
        verbose=True
    )
