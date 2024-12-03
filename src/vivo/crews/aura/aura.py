from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class Aura:
    """Aura crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    aura_agent = Agent(
        role="Supervisor de Atendimento Vivo",
        goal="Coordenar os agentes de atendimento para resolver a solicitação do cliente: {topic}.",
        backstory="""Você é um supervisor que gerencia o fluxo de trabalho de agentes especializados nos serviços da Vivo, 
        como suporte técnico, informações sobre planos, contas e pagamentos, e resolução de problemas técnicos.
        Seu principal papel é garantir que a solicitação do cliente seja tratada de forma eficiente, alocando as tarefas para os agentes responsáveis.
        Sempre que possível, você deve priorizar o uso do agente de informações de conta e/ou o agente técnico para coletar os dados necessários.
        Após reunir as informações, delegue ao agente de resumo para compilar uma resposta clara e abrangente ao cliente.""",
        verbose=True,
        allow_delegation=True,
    )

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
            manager_agent=self.aura_agent,
            process=Process.hierarchical,
            verbose=True,
        )
