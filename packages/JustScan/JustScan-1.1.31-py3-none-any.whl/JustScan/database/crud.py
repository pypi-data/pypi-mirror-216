import uuid
import base64
from sqlalchemy import func
from JustScan.face_id.tools.modules import byte2array
from .database import engine, Base, Session
from .data_models import FaceModel, ImageModel
from functools import wraps


class QueryData:
    def __init__(self) -> None:
        self.engine = engine
        Base.metadata.create_all(self.engine)
        self.session = Session()

    def handling_decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                print(f"Error in {func.__name__!r}: ", e)
        return wrapper

    @handling_decorator
    def register_image(self, metadata,  b64_img: base64 = None, encoded_input=None):
        """Registering an image to db"""
        with self.session as session:
            image = ImageModel(
                id=str(uuid.uuid4()),
                # image_base64=str(b64_img),
                embedded_image=encoded_input.tobytes(),
                metadata_=metadata,
                created_at=func.current_timestamp(),
                updated_at=func.current_timestamp()
            )
            session.add(image)
            session.commit()
            return image.id, image.created_at, image.updated_at

    @handling_decorator
    def register_face(self):
        """Registering a face to db"""
        with self.session as session:
            face = FaceModel(
                id=str(uuid.uuid4()),
                created_at=func.current_timestamp(),
                updated_at=func.current_timestamp()
            )
            session.add(face)
            session.commit()
            return face.id

    @handling_decorator
    def select_all_images(self) -> dict:
        """Select all images from database"""
        with self.session as session:
            rows = session.query(ImageModel)
            all_stored_predict = [byte2array(
                row.embedded_image) for row in rows]
            id = [row.id for row in rows]
            dict_result = dict(zip(id, all_stored_predict))
            return dict_result

    @handling_decorator
    def update_faceid(self, image_id, face_id) -> None:
        """Update face_id in images table"""
        with self.session as session:
            row = session.query(ImageModel).filter(
                ImageModel.id == image_id).first()
            row.face_id = face_id
            session.commit()

    @handling_decorator
    def get_matched_faceid(self, image_id) -> uuid:
        """Get face_id by image id"""
        with self.session as session:
            row = session.query(ImageModel).filter(
                ImageModel.id == image_id).first()
            face_id = row.face_id
            return face_id

    @handling_decorator
    def get_image_b64(self, image_id) -> base64:
        """Select b64 image from id"""
        with self.session as session:
            row = session.query(ImageModel).filter(
                ImageModel.id == image_id).first()
            image_b64 = row.image_base64
            return image_b64

    @handling_decorator
    def select_imageid(self, image_id: uuid) -> dict:
        """Get information from image_id"""
        with self.session as session:
            row = session.query(ImageModel).filter(
                ImageModel.id == image_id).first()
            image_info = {
                'image_id': row.id,
                'face_id': row.face_id,
                'metadata': row.metadata_,
                'created_at': row.created_at,
                'updated_at': row.updated_at,
                # 'images': row.image_base64,
            }
            return image_info

    @handling_decorator
    def select_predict_result(self) -> list:
        """Get predict result from image table"""
        with self.session as session:
            rows = session.query(ImageModel).all()
            row_data = [row.embedded_image for row in rows]
            return row_data

    @handling_decorator
    def update_face_updated_time(self, face_id, updated_at) -> None:
        """Update updated_at in face table"""
        with self.session as session:
            row = session.query(FaceModel).filter(FaceModel.id==face_id).first()
            row.updated_at = updated_at
            session.commit()

def main():
    query = QueryData()
    print((query.select_predict_result()[1]))
