from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import shutil
import tempfile

from .predict.predict_comp import predict
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def index():
    return("Hello csi predict api")

@app.post('/predict')
def save_predict(db: Session = Depends(get_db), file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=True, dir=".", suffix=".csv") as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        pred_result, prob_result = predict(temp_file.name, file.filename)

        result = schemas.PredictResultCreate(file_name=file.filename, pred_result=pred_result, prob_result=prob_result)
        crud.save_predict_result(db=db,result=result)

    return JSONResponse(content={"res": "ok", "filename": file.filename})

@app.get('/get_pred_result')
def get_pred_result(db: Session = Depends(get_db)):
    return crud.get_predict_result(db=db)

@app.get('/get_prob_result/{id}')
def get_prob_result(id, db: Session = Depends(get_db)):
    return crud.get_prob_result(id=id, db=db)

@app.get('/all')
def get_all(db: Session = Depends(get_db)):
    return crud.get_all(db=db)