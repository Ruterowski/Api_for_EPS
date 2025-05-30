import io

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/echo-image")
async def echo_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    return StreamingResponse(io.BytesIO(image_bytes), media_type=file.content_type)
    

@app.post("/recognition/m1")
async def GetRecognizePiecesModel1(file:  UploadFile = File(...)):

    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    model = YOLO("model/my_model1.pt")

    result = model.predict(image)

    detections = []
    for r in result:
        for box in r.boxes:
            cls_id = int(box.cls[0].item())
            label = model.names[cls_id]
            conf = float(box.conf[0].item())
            xyxy = box.xyxy[0].tolist()
            detections.append({
                "label": label,
                "confidence": conf,
                "box": xyxy
            })

    return JSONResponse(content={"detections": detections})

@app.post("/recognition/m2")
async def GetRecognizePiecesModel2(file:  UploadFile = File(...)):

    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    model = YOLO("model/my_model2.pt")

    result = model.predict(image)

    detections = []
    for r in result:
        for box in r.boxes:
            cls_id = int(box.cls[0].item())
            label = model.names[cls_id]
            conf = float(box.conf[0].item())
            xyxy = box.xyxy[0].tolist()
            detections.append({
                "label": label,
                "confidence": conf,
                "box": xyxy
            })

    return JSONResponse(content={"detections": detections})
