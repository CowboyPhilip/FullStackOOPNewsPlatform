import emails
from jinja2 import Environment, FileSystemLoader, TemplateNotFound, TemplateError
from app.config.config import settings
from abc import ABC
import logging
from typing import Any, Optional
from pydantic import EmailStr, BaseModel


class Command(ABC):
    # @abstractmethod
    def execute(self):
        pass


class Invoker:

    def __init__(self):
        self.invokers = [Command()]

    def addInvoker(self, command: Command):
        return self.invokers.append(command)

    def run(self):
        for invoker in self.invokers:
            invoker.execute()


class EmailOptions(BaseModel):
    template_name: str
    email_to: EmailStr
    to:str
    subject:str
    app_name: str = settings.PROJECT_NAME
    link: Optional[str | None] = None
    otp: Optional[str | None] = None
    token: Optional[str | None] = None


class SendEmail(Command):

    def __init__(self, props: EmailOptions):
        self.emailTo = props.email_to
        self.smtp_options: dict[str, Any] = {}
        self.message = ()
        self.context = {
            "appName": props.app_name,
            "link": props.link,
            "otp": props.otp,
            "token": props.token,
            "to":props.to
        }
        self.template_name = props.template_name
        self.subject = props.subject

    def renderTemplate(self) -> str:
        env = Environment(loader=FileSystemLoader(settings.EMAILS_DIRECTORY))
        template = env.get_template(self.template_name)
        return template.render(self.context)

    @property
    def smtpOptions(self):
        try:
            if settings.SMTP_HOST and settings.SMTP_PORT:
                self.smtp_options["host"] = settings.SMTP_HOST
                self.smtp_options["port"] = settings.SMTP_PORT
                if settings.SMTP_TLS:
                    self.smtp_options["tls"] = settings.SMTP_TLS
        except Exception:
            logging.error(
                "something went wrong during the configuration of smtp options"
            )
        else:
            try:
                self.smtp_options["user"] = settings.SMTP_USER
                self.smtp_options["password"] = settings.SMTP_PASSWORD
                return self.smtp_options
            except Exception:
                logging.error(
                    "something went wrong during the configuration of smtp credentials"
                )

    def execute(self):
        try:
            html_content = self.renderTemplate()

            smtp_options = self.smtpOptions

            self.message = emails.html(
                subject=self.subject,
                html=html_content,
                mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
            )

        except TemplateNotFound and TemplateError:
            logging.error("error gathering the path about the template provided")
        else:
            try:
                res = self.message.send(to=self.emailTo, smtp=smtp_options)
            except Exception as e:
                logging.error(e)
            else:
                print(
                    f"email has been sent to {self.emailTo} successfully: {res.status_code}"
                )




# email_verification = SendEmail(
#             EmailOptions(
#                 subject=settings.PROJECT_NAME + " subject",
#                 template_name="template.html",
#                 email_to='user@example.com',
#                 link=settings.FRONTEND_MAIN_ORIGIN,
#                 to='example name',
#             )
#         )
# email_verification.execute()