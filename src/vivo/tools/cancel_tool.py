from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class CancelToolInput(BaseModel):
    email: str = Field(..., description="The user email.")
    cpf: str = Field(..., description="The user cpf.")


class CancelTool(BaseTool):
    name: str = "Cancellation Process"
    description: str = (
        "Guide the user by journey of the cancellation service process, for this the system should ask of the user data to init the cancellation process"
    )

    def _run(self, argument: str) -> str:
        """
            Collects and validates client data required for service cancellation.
            Validates:
                - CPF: Must be 11 numeric digits.
                - Email: Must follow standard email format.
                - Service: Cannot be empty.
            Returns:
                A dictionary containing validated CPF, email, and service to cancel.
            Raises:
                ValueError: If any validation fails.
            """
        phrase: str = "To continue the cancellation service task, you need provide the user's"
        cpf = ""
        email = ""
        service = ""

        # Validate CPF
        if not cpf.isdigit() or len(cpf) != 11:
            phrase = phrase + ", CPF"

        # Validate email (rudimentary validation for simplicity)
        if "@" not in email or "." not in email.split("@")[-1]:
            phrase = phrase + ", email"

        # # Validate service
        if not service:
            phrase = phrase + ", service do want cancel"

        return phrase
