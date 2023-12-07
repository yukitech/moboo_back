from fastapi import FastAPI, File, UploadFile
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

@app.post('/uploadfile')
def get_uploadfile(file: UploadFile = File(...)):
    # suffixは保存するファイルの拡張子を指定（今回は".stl"を指定）
    with tempfile.NamedTemporaryFile(delete=True, dir=".", suffix=".csv") as temp_file:
        shutil.copyfileobj(file.file, temp_file)

        # with内であればtemp_file.nameでファイル名指定が可能
        print(temp_file.name)

        # ↓内部処理↓
        predict(temp_file)

    return {
        'filename': file.filename
    }