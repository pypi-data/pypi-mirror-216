from ...commons.SpoofingNID import SpoofingNIDModel
from fastapi import HTTPException
from JustScan.config.logger import setup_logger

logging = setup_logger(__name__)


def check_spoof_nid(image):
    label_spoof, confidence_spoof = SpoofingNIDModel().predict(image)
    try:
        result = [{
            'nonLiveNID': True if label_spoof == 0 else False,
            'confidence': confidence_spoof,
            'toBeReview': True if confidence_spoof < 0.5 else False
        }]
        return result
    except:
        logging.error(f'error at running {check_spoof_nid.__name__}, ID card not found')
        raise HTTPException(status_code=404,
                            detail={
                                'status': 404,
                                'code': 'ID_CARD_NOT_FOUND',
                                'error': 'ID card not found. Please try again'
                            }
                            )
