from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class Aura:
    """Aura crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def classification_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['classification_agent'],
            verbose=True
        )

    @task
    def classification_task(self) -> Task:
        return Task(
            config=self.tasks_config['classification_task'],
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
