from pydantic import BaseModel
from typing import Dict,List



class TranslationRequest(BaseModel):
    text:str
    languages:List[str]

class TaskResponse(BaseModel):
    task_id:int

class TranslationStatus(BaseModel):
    task_id:int
    status:str
    translation:Dict[str,str]