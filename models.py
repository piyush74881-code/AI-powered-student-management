from pydantic import BaseModel,EmailStr
from typing import Optional
#pydantic used for autovalidation of input request data

class Student(BaseModel):
    name:str
    age:int # if 25.5=25 some data will be lost
    course:str
    email:Optional[EmailStr]=None

class Feedback(BaseModel):
    text:str