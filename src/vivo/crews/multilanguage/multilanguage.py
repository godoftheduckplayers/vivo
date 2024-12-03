from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class Multilanguage:
    """Multilanguage crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def multilanguage_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['multilanguage_agent'],
            verbose=True
        )

    @task
    def aura_translation_content_task(self) -> Task:
        return Task(
            config=self.tasks_config['aura_translation_content_task'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
