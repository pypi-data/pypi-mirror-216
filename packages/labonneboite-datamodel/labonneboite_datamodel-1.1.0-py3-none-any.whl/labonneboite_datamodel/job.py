from sqlmodel import Field
from typing import Optional
from .base import BaseMixin
from pydantic import validator


class Job(BaseMixin, table=True):
    """This table hosts the mapping between ROME and AF to be able to make a ROME search correspond to a SIRET

    Attributes:
        id:
        naf:
        rome:
        domain:
        granddomain:
        label_granddomain:
        label_domain:
        label_naf:
        label_rome:
        hirings: number of hirings this rome as seen (This is the part of the original mapping in labonneboite)
    """
    id: Optional[int] = Field(
        default=None, primary_key=True, nullable=False)

    naf: str
    rome: str
    domain: Optional[str] = Field(default=None, nullable=False)
    granddomain: Optional[str] = Field(default=None, nullable=False)

    label_granddomain: Optional[str] = Field(default=None, nullable=False)
    label_domain: Optional[str] = Field(default=None, nullable=False)
    label_naf: str
    label_rome: str

    hirings: int

    @validator("naf", pre=True)
    def is_naf(cls, v):
        """Validator for `naf`

        Rules:
            - should be made up of 2 numbers

        Raises:
            ValueError:

        """
        error = "a NAF should be made up of 2 numbers"
        v = str(v)

        if len(v) != 2:
            raise ValueError(error)

        if not v.isdigit():
            raise ValueError(error)

        return v

    @validator("rome", pre=True)
    def is_rome(cls, v):
        """Validator for `rome`

        Rules:
            - should be made up of 5 characters
            - the last 4 values should be numeric
            - the first value should be a letter

        Raises:
            ValueError:

        """
        error = "a ROME should be made up of 4 numbers and a letter"
        if len(v) != 5:
            raise ValueError(error)

        if not v[1:4].isdigit():
            raise ValueError(error)

        if v[0].isdigit():
            raise ValueError(error)
        return v


class Naf(BaseMixin, table=True):
    """This table hosts the Naf labels

    Attributes:
        id:
        naf:
        label:
    """
    id: Optional[int] = Field(
        default=None, primary_key=True, nullable=False)

    naf: str
    label: str

    @validator("naf", pre=True)
    def is_naf(cls, v):
        """Validator for `naf`

        Rules:
            - should be 5 characters long
            - the first 4 values should be numeric
            - The last value should be a letter

        Raises:
            ValueError:

        """
        # A valid NAF is composed 4 numbers and a letter (could be a regex ^\d{4}\D{1}$)
        error = "a NAF should be made up of 4 numbers and a letter"
        if len(v) != 5:
            raise ValueError(error)

        if not v[:4].isdigit():
            raise ValueError(error)

        if v[-1].isdigit():
            raise ValueError(error)
        return v
