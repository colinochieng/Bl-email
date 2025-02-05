from quart import Quart
from app.models import QuotationForm, ContactUsForm
from app.dependencies import valid_json, get_settings, send_contact_us_email, send_quotation_email
from pydantic import ValidationError
from quart_cors import cors
from http import HTTPStatus



def create_app():
    app = Quart(__name__)

    app.url_map.strict_slashes = False

    app = cors(
        app,
        allow_origin=get_settings().cors_allow_origin,
        # allow_methods=["GET", "POST", "OPTIONS"],
        # allow_headers=["Content-Type", "Authorization"],
        )

    @app.post("/contact-us")
    @valid_json
    async def contact_us(body):
        """
        Contact us endpoint

        Send an email to the admin email address
        :param body: request body
        """
        try:
            form = ContactUsForm(**body)
        except ValidationError as e:
            return {"error": e.errors()}, HTTPStatus.BAD_REQUEST.value

        await send_contact_us_email(
            get_settings().admin_email,
            get_settings().admin_password,
            get_settings().admin_email, # Admin is the sender and recipient
            form.subject,
            **form.model_dump(),
        )
        return {"message": "Message sent successfully"}, HTTPStatus.OK.value


    @app.post("/quotation")
    @valid_json
    async def quotation(body):
        """
        Quotation endpoint

        Send an email to the admin email address
        :param body: request body
        """
        try:
            form = QuotationForm(**body)
        except ValidationError as e:
            return {"error": e.errors()}, HTTPStatus.BAD_REQUEST.value

        await send_quotation_email(
            get_settings().admin_email,
            get_settings().admin_password,
            get_settings().admin_email, # Admin is the sender and recipient
            form.subject,
            **form.model_dump(),
        )
        return {"message": "Message sent successfully"}, HTTPStatus.OK.value

    return app
