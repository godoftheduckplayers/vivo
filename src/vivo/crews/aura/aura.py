from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class Aura:
    """Aura crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def research_vivo_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['research_vivo_agent'],
            verbose=True,
        )

    @task
    def research_vivo_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_vivo_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Aura crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
