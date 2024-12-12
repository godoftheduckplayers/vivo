import os
import smtplib
from email.message import EmailMessage
from typing import Type

from crewai.tools import BaseTool, tool
from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""

    argument: str = Field(..., description="Description of the argument.")


class MyCustomTool(BaseTool):
    name: str = "Name of my tool"
    description: str = (
        "Clear description for what this tool is useful for, you agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return "this is an example of a tool output, ignore it and move along."


@tool("email_tool")
def send_email_tool():
    """Send email tool."""
    print("send_email_tool Tool!")
    to_email = "evelyn.neves.barreto@nttdata.com"
    subject = "Complaint Resolution"
    content = "Your complaint has been resolved successfully."

    if not to_email or not subject or not content:
        return {"status": "error", "message": "Missing required parameters: to_email, subject, or content"}

    email = EmailMessage()
    email["From"] = os.getenv("EMAIL_SENDER")
    email["To"] = to_email
    email["Subject"] = subject
    email.set_content(content)

    try:
        with smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
            server.login(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PASSWORD"))
            server.send_message(email)
        return {"status": "success", "message": "Email sent successfully."}
    except smtplib.SMTPAuthenticationError:
        return {"status": "error", "message": "Authentication failed. Check your email credentials."}
    except smtplib.SMTPConnectError:
        return {"status": "error", "message": "Failed to connect to the SMTP server. Check your network connection."}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}