from crewai import Agent, Crew, Process, Task


class Information:
    research_vivo_agent = Agent(
        role="Research",
        goal="Assist users by providing up-to-date information on Vivo's services and promotions, answering specific questions, and conducting searches on reliable sources to ensure accuracy and relevance.",
        backstory="Designed to support customers and individuals interested in Vivo's services, this agent is programmed to access official company sources, such as the institutional website, customer service channels, and recent publications. It is also equipped to interpret data from promotional offers and technological updates, ensuring objective and informative assistance.",
        verbose=True,
    )

    research_vivo_task = Task(
        description="This task aims to gather updated information about the services offered by Vivo in 2024, based on the user's input: {input}. The research will cover aspects such as mobile phone plans, fixed internet, TV packages, data offers, and other relevant services provided by the company.",
        expected_output="A detailed and accurate summary of Vivo's current services in 2024, including information on plans, promotional offers, pricing, package features, and any other relevant services, tailored to the specific inquiry or question presented by the user.",
        agent=research_vivo_agent,
    )

    crew = Crew(
        agents=[research_vivo_agent],
        tasks=[research_vivo_task],
        process=Process.sequential,
        verbose=True,
    )
