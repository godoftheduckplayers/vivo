from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class Multilanguage:
    """Multilanguage crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def translation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['translation_agent'],
            verbose=True
        )

    @task
    def language_recognition_translation_task(self) -> Task:
        return Task(
            config=self.tasks_config['language_recognition_translation_task'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
