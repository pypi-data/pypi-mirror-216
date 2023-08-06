from __future__ import annotations
from typing import List, Union, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class DetectFacial(BaseModel):
    startX: int
    startY: int
    endX: int
    endY: int


class QualityType(BaseModel):
    type: str
    result: bool
    confidence: float


class QualityCheck(BaseModel):
    check: bool
    detail: List[QualityType]


class DetectLanmarks(BaseModel):
    right_eye: List[int]
    left_eye: List[int]
    nose: List[int]
    mouth_right: List[int]
    mouth_left: List[int]


class DectectFormat(BaseModel):
    # quality: QualityCheck
    # face: str
    facial_area: DetectFacial
    confidence: float
    landmarks: DetectLanmarks
    faces_b64: str


class DetectOutput(BaseModel):
    result: List[DectectFormat]


class MatchedImage(BaseModel):
    id: UUID
    distance: float
    confidence: float


class RegisterFormat(BaseModel):
    # quality: bool
    image_id: UUID
    face_id: UUID
    metadata: Optional[str]
    created_at: datetime
    updated_at: datetime
    image: str
    matched_image: Optional[List[MatchedImage]]


class RegisterOutput(BaseModel):
    result: List[RegisterFormat]


# Face Recognize Models
class RecognizeImagesOutput(BaseModel):
    image_id: UUID
    distance: float
    confidence: float
    metadata: Optional[str]
    created_at: datetime
    updated_at: datetime
    # image: Optional[str]


class RecognizeFaceOutput(BaseModel):
    recognized: bool
    face_id: Optional[UUID]
    images: Union[List[RecognizeImagesOutput], str]


class RecognizeOutputResult(BaseModel):
    result: List[RecognizeFaceOutput]


class IdCardLocation(BaseModel):
    x: int
    y: int
    w: int
    h: int


class IdInfo(BaseModel):
    type: str
    value: str
    confidence: float
    location: Optional[IdCardLocation]


class IdOutput(BaseModel):
    result: List[IdInfo]


class SpoofingNID(BaseModel):
    nonLiveNID: bool
    confidence: float
    toBeReview: bool


class SpoofingOutput(BaseModel):
    result: List[SpoofingNID]


class VerificationResult(BaseModel):
    match: bool
    distance: float
    confidence: float
    toBeReviewed: bool


class CompareFaces(BaseModel):
    verification_result: VerificationResult = Field(
        ..., alias='verification_result')
    input_image_1: str
    input_image_2: str


class CompareResult(BaseModel):
    result: CompareFaces


class ImageQuality(BaseModel):
    sharpness: float
    contrast: float
    brightness: float
    blur: float
    quality: bool
    reason: List[Optional[str]]


class ImageQualityResult(BaseModel):
    result: ImageQuality


class QualityLiveness(BaseModel):
    liveness: bool
    confidence: float
    toBeReview: bool
    sharpness: float
    contrast: float
    brightness: float
    blur: float
    quality: bool
    reason: List[Optional[str]]


class NIDQualityLivenessResult(BaseModel):
    result: QualityLiveness


class FaceLiveness(BaseModel):
    live: bool
    confidence: float
    toBeReview: bool


class Occlusion(BaseModel):
    occluded: bool
    type: List[Optional[str]]
    confidence: List[float]
    toBeReview: bool


class SelfieCheckItem(BaseModel):
    liveness: FaceLiveness
    occlusion: Occlusion


class SelfieCheckResult(BaseModel):
    result: List[SelfieCheckItem]

    class Config:
        schema_extra = {
            "example": {
                "result": [
                    {
                        "liveness": {
                            "live": True,
                            "confidence": 0.8752402067184448,
                            "toBeReview": False
                        },
                        "occlusion": {
                            "isOccluded": True,
                            "type": [
                                "eyes",
                                'mask'
                            ],
                            "confidence": [
                                1,
                                0.9999998211860657
                            ],
                            "toBeReview": False
                        }
                    }
                ]
            }
        }


class MultiFacesCheck(BaseModel):
    isMultipleFaces: bool


class MultiFacesCheckResult(BaseModel):
    result: MultiFacesCheck
