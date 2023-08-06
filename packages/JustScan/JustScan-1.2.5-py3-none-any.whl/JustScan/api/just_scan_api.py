from fastapi import File, FastAPI
from typing import List, Dict
from JustScan.face_id.libraries.face_detection import selfie_face_check, check_image_quality, multi_face_check, \
    check_image_qual
from JustScan.database.crud import QueryData
from JustScan.ocr.core.tools.functional import get_result_id_card, get_alignment_image
from JustScan.ocr.core.modules.id_card_classification.classify import process_classification
from JustScan.config.pydantic_models import IdOutput, DetectOutput, RegisterOutput, \
    RecognizeOutputResult, \
    CompareResult, \
    ImageQualityResult, \
    SelfieCheckResult, \
    SpoofingOutput, \
    MultiFacesCheckResult, \
    NIDQualityLivenessResult
from JustScan.config.config import processing_image
from JustScan.face_id.libraries.face_id import get_register, get_recognize, comparing_faces, detect_user
from JustScan.ocr.core.modules.mrc.mrc_detection import get_mrc, get_mrc_alignment
from JustScan.ocr.core.modules.passport.passport import PassportAutoAlign
from JustScan.ocr.core.modules.passport.utils import get_passport
from JustScan.ocr.core.modules.spoofing_nid.spoofing import check_spoof_nid
from JustScan.config.logger import setup_logger, timeit
from JustScan.ocr.core.modules.quality_liveness_nid_checking.nid_quality_liveness_check import NIDQualityLivenessCheck
import uvicorn

logging = setup_logger(__name__)

db = QueryData()

app = FastAPI(title='ITC AI', swagger_ui_parameters={
    "defaultModelsExpandDepth": -1}
              # docs_url="/", redoc_url=None
              )


@app.post("/ocr/id-card/", tags=['Scanning Card Type'], response_model=IdOutput,
          description='Extract Information from national Id card')
async def extract_information_id_card(image: str = File(...)):
    labels, confidences, images = process_classification(get_alignment_image(processing_image(image)))
    return {'result': get_result_id_card(image_alignment=images,
                                         label_classify=labels, confidence=confidences)}


@app.post("/ocr/nid-liveness-check/", tags=['Scanning Card Type'], response_model=SpoofingOutput,
          description='NID Liveness Check')
async def nid_liveness_check(image: str = File(...)):
    image_alignment = get_alignment_image(processing_image(image))
    return {'result': check_spoof_nid(image_alignment)}


@app.post("/ocr/id-card-quality-check/", response_model=ImageQualityResult, tags=['Scanning Card Type'])
async def id_card_quality_check(image: str = File(...)):
    image_alignment = get_alignment_image(processing_image(image))
    return {"result": check_image_qual(image_alignment)}


@app.post("/ocr/id-card-quality-liveness-check/", response_model=NIDQualityLivenessResult, tags=['Scanning Card Type'])
async def id_card_quality_liveness_check(image: str = File(...)):
    return {"result": NIDQualityLivenessCheck().nid_spoof_quality_check(processing_image(image))}


@app.post("/ocr/mrc-card/", tags=['Scanning Card Type'], response_model=IdOutput,
          description='Extract Information from MRC card')
async def extract_information_mrc(image: str = File(...)):
    image_alignment = get_mrc_alignment(processing_image(image))
    return {'result': get_mrc(image=image_alignment)}


@app.post("/ocr/passport/", tags=['Scanning Card Type'], response_model=IdOutput,
          description='Extract Information from Passport')
async def extract_information_passport(image: str = File(...)):
    image_alignment = PassportAutoAlign(processing_image(image))
    return {'result': get_passport(image_alignment)}


@app.post("/scan/face-id/detect-users/", response_model=DetectOutput, tags=['FaceID'])
async def detect_face(New_image: str = File(...)):
    input_image = processing_image(New_image)
    return {'result': detect_user(image=input_image)}


@app.post("/scan/face-id/register/", response_model=RegisterOutput, tags=['FaceID'],
          description='Registing new user to system')
async def register(image: str = File(...), metadata: str = None):
    input_image = processing_image(image)
    return get_register(input_image, metadata)


@timeit(logging)
@app.post("/scan/face-id/recognize/", response_model=RecognizeOutputResult, tags=['FaceID'])
async def recognize(input_image: str = File(...)) -> Dict[str, List[Dict[str, any]]]:
    image = processing_image(input_image)
    return get_recognize(image)


@app.post("/scan/face-id/compare/", response_model=CompareResult, tags=['FaceID'])
async def compare(input1: str = File(...), input2: str = File(...)):
    process_input1 = processing_image(input1)
    process_input2 = processing_image(input2)
    return comparing_faces(process_input1, process_input2)


@app.post("/scan/face-id/selfie-check/", response_model=SelfieCheckResult, tags=['FaceID'])
async def selfie_check(image: str = File(...)):
    img = processing_image(image)
    return selfie_face_check(img)


@app.post("/scan/face-id/face-quality-assessment/", response_model=ImageQualityResult, tags=['FaceID'])
async def face_quality_assessment(image: str = File(...)):
    img = processing_image(image)
    return check_image_quality(img)


@app.post("/scan/face-id/multi-face-check/", response_model=MultiFacesCheckResult, tags=['FaceID'])
async def multiple_face_check(image: str = File(...)):
    img = processing_image(image)
    return multi_face_check(img)


# def run_api(command_line):
#     uvicorn.run(command_line, host="127.0.0.1", reload=True, port=8000)
#
#
# if __name__ == "__main__":
#     run_api(command_line='just_scan_api:app')
