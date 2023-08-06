from xia_fields import StringField
from xia_engine import Document


class Service(Document):
    """A service defined the endpoint which could be access by the end user

    * General url will be:
        * production: <service name>.x-i-a.io
        * integration test: <service name>.x-i-a.dev
        * development: <service name>.x-i-a.xyz

    * A typical service is seperated by:
        * root service: by default one, cover /
        * app service: backend api call, cover /api
        * sso service: sso based token renew/validation, cover /sso
    """
    _key_fields = ["service_name"]
    service_name: str = StringField(required=True, description="Service Name")
    app_name: str = StringField(required=True, description="Application Name")

    root_service: str = StringField(
        description="Root Service Endpoint",
        regex=r"(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)"
    )
    app_service: str = StringField(
        description="App Service Endpoint",
        regex=r"(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)"
    )
    sso_service: str = StringField(
        description="SSO Service Endpoint",
        regex=r"(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,63}$)"
    )
