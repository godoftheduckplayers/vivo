from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class Plans:
    """Plans crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def vivo_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['vivo_researcher'],
            verbose=True
        )

    @task
    def vivo_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['vivo_research_task'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
