from pydantic import AfterValidator, BaseModel, Field, EmailStr
from typing import Annotated
import re
from app.dependencies import validate_phone_number


class UserMessageDetails(BaseModel):
    """
    User message details
    """
    # personal details
    fullName: Annotated[str, AfterValidator(lambda x: " ".join(
        [name.title() for name in x.split()]))] = Field(..., title="Full name")
    email: EmailStr = Field(..., title="Email address")
    phone: Annotated[str, AfterValidator(
        validate_phone_number)] = Field(..., title="Phone number")

    # message details
    subject: Annotated[str, AfterValidator(
        str.strip)] = Field(..., title="Message subject")
    message: Annotated[str, AfterValidator(
        str.strip)] = Field(..., title="Message content")


class ContactUsForm(UserMessageDetails):
    """
    Contact us form
    """
    pass


class QuotationForm(UserMessageDetails):
    """
    Quotation form
    """
    city: Annotated[str, AfterValidator(str.strip), AfterValidator(
        str.title)] = Field(..., title="City or town")
    address: Annotated[str, AfterValidator(
        str.strip)] = Field(..., title="Physical Address")
