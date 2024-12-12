import os
from typing import List

from crewai.tools import BaseTool
from crewai_tools.tools.pdf_search_tool.pdf_search_tool import PDFSearchTool

pdf_tool_config = config = dict(
    llm=dict(
        provider="azure_openai",
        config=dict(
            model="gpt-4o",
        ),
    ),
    embedder=dict(
        provider="azure_openai",
        config=dict(
            api_key="eee842323c1e4556b1a7f0ddef120c5a",
            model="text-embedding-3-small",
        ),
    ),
)


class PDFRagTool:
    path = os.environ["PDF_RAG_DIR"]

    doc1 = PDFSearchTool(
        pdf=path + "\\manual-de-boas-praticas.pdf",
        config=pdf_tool_config
    )

    doc2 = PDFSearchTool(
        pdf=path + "\\Planos_e_Servicos_Vivo_2024.pdf",
        config=pdf_tool_config
    )

    doc3 = PDFSearchTool(
        pdf=path + "\\recarga_digital.pdf",
        config=pdf_tool_config
    )

    doc4 = PDFSearchTool(
        pdf=path + "\\regulamento_relampago.pdf",
        config=pdf_tool_config
    )

    doc5 = PDFSearchTool(
        pdf=path + "\\regulamento-controle-I.pdf",
        config=pdf_tool_config
    )

    doc6 = PDFSearchTool(
        pdf=path + "\\regulamento-vivo-controle.pdf",
        config=pdf_tool_config
    )

    doc7 = PDFSearchTool(
        pdf=path + "\\Relato_Integrado_2023_Vfinal.pdf",
        config=pdf_tool_config
    )

    doc8 = PDFSearchTool(
        pdf=path + "\\SCM-006-Banda-Larga-50Mb.pdf",
        config=pdf_tool_config
    )

    doc9 = PDFSearchTool(
        pdf=path + "\\ValoresCheiosFev23.pdf",
        config=pdf_tool_config
    )

    tools: List[BaseTool] = [doc1, doc2, doc3, doc4, doc5, doc6, doc7, doc8, doc9]
