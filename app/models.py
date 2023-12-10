from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from .database import Base


class PredictResult(Base):
    __tablename__ = "predict_result"

    id = Column(Integer, primary_key=True, nullable=False)
    file_name = Column(String, nullable=False)
    pred_result = Column(String, nullable=True)
    prob_result = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)