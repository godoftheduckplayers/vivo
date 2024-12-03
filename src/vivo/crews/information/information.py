from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools.tools.serper_dev_tool.serper_dev_tool import SerperDevTool


@CrewBase
class Information:
    """Information crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def vivo_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['vivo_researcher'],
            verbose=True,
            tools=[SerperDevTool()]
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
