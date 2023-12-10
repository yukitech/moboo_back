from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import desc

def get_all(db: Session):
  return db.query(models.PredictResult).all()

def get_predict_result(db: Session):
  result = db.query( models.PredictResult.id, models.PredictResult.pred_result).order_by(desc(models.PredictResult.created_at)).first()
  res = dict(id=result.id, pred_result=result.pred_result)
  return res

def get_prob_result(id: int, db: Session):
  result = db.query(models.PredictResult.id, models.PredictResult.prob_result).filter(models.PredictResult.id == id).first()
  res = dict(id=result.id, pred_result=result.prob_result)
  return res

def save_predict_result(db: Session, result: schemas.PredictResultCreate):
  new_result = models.PredictResult(**result.dict())
  db.add(new_result)
  db.commit()
  db.refresh(new_result)