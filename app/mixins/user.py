from secrets import token_urlsafe

from pydantic import Field, field_validator
from pymongo import IndexModel

from app.mixins.general import BaseDocument


def random_password():
    return token_urlsafe(10)


class User(BaseDocument):
    __keyword_fields__ = ["first_name", "last_name", "tckn"]
    first_name: str = Field(title="Ad", default="Ahmet", max_length=32)
    last_name: str = Field(title="Soyad", default="Yılmaz", max_length=32)
    tckn: int = Field(title="T.C. Kimlik No", default=11111111111)
    password: str = Field(
        default_factory=random_password, title="Şifre", max_length=32, repr=False
    )
    phone: int = Field(ge=10**9, lt=10**10, title="GSM", default=5000000000)

    class Settings:
        indexes = [
            IndexModel(
                [("SchoolCode", 1), ("tckn", 1)],
                unique=True,
            )
        ]

    @field_validator("first_name", "last_name", "password", mode="before")
    def transform_id_to_str(cls, value) -> str:
        return str(value)
