from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class OptimizationMechanisms:
    """OptimizationMechanisms crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def multilanguage_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['multilanguage_agent'],
            verbose=True
        )

    @agent
    def content_refinement_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['content_refinement_agent'],
            verbose=True
        )

    @task
    def multilanguage_task(self) -> Task:
        return Task(
            config=self.tasks_config['multilanguage_task'],
        )

    @task
    def content_refinement_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_refinement_task'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
