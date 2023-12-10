from datetime import datetime
from pydantic import BaseModel

class PredictResultBase(BaseModel):
  file_name: str
  pred_result: str
  prob_result: str


class PredictResultCreate(PredictResultBase):
  pass

class PredictResult(PredictResultBase):
  id: int
  created_at: datetime

  class Config:
    orm_mode = True