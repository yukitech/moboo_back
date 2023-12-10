from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil
import tempfile
import sys

sys.path.append('..')
from predict.predict_comp import predict

app = FastAPI()

@app.get('/')
def index():
    return("Hello csi predict api")

@app.post('/predict')
def get_uploadfile(file: UploadFile = File(...)):
    # suffixは保存するファイルの拡張子を指定（今回は".stl"を指定）
    with tempfile.NamedTemporaryFile(delete=True, dir=".", suffix=".csv") as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        predict(temp_file.name, file.filename)

    return JSONResponse(content={"res": "ok", "filename": file.filename})