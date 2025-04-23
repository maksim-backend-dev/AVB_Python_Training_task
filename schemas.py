from pydantic import BaseModel

class URLRequest(BaseModel):
    """
    Model for an incoming URL shortening request.
    Contains one field 'url' - a string with the original address.
    """
    url: str