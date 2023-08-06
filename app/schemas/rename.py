from typing import Optional

from pydantic import BaseModel, validator

from datetime import datetime


class RenameBase(BaseModel):
    usename: str

    @validator('usename')
    def simple_validator(cls, v):
        if v == 'bad name':
            raise ValueError('Bad name')
        return v


class RenameCreate(RenameBase):
    passwd: str


class RenameInDB(RenameCreate):
    usesysid: int
    usecreatedb: bool
    usesuper: bool
    userepl: bool
    usebypassrls: bool
    passwd: str
    valuntil: Optional[datetime] = None
    useconfig: Optional[str] = None


class RenameUpdate(RenameBase):
    pass
