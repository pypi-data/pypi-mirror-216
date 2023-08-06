# EKYC (OCR&FaceID) API 
<!-- [![My Skills](https://skills.thijs.gg/icons?i=python&theme=light)](https://skills.thijs.gg) -->
EKYC (OCR&FaceID) API is an API developed to provide Optical Character Recognition (OCR) and Face ID functionalities. The API supports the scanning of national ID cards, motorbike registration certificates, and EVN bills. It utilizes Makesense AI for labeling data, Yolov5 for text detection, and VietOCR for text recognition.

In addition to OCR, the API also provides Face ID functionality, including face detection, face recognition, and quality checks. It utilizes SCRFD for face detection, ArcFace for face recognition, and provides face liveness detection, face quality assessment, face mask detection, and closed eyes detection.

# Scanning Card Type 🚀

+ Type Support 
  + National ID card
  + MRC (Motorbike Registation Certificate) 
  + Passport
+ OCR Techniques: 
  + Makesense AI for labeling data
  + Yolov5 for Text Detection task 
  + VietOCR for Text Recognition task
# Face ID 🚀 

+ Face Detection & Face Recognition
  + SCRFD (Sample and Computation Redistribution for Efficient) for Face Detection
  + ArcFace (From InsightFace project with high accuracy in Face Recognition)
  + Check Quality techniques:
    + Face Liveness Detection 
    + Face Quality Assessment
    + Face Mask Detection 
    + Closed Eyes Detection 

# How to install
Install Python version: 3.8.10
Clone the project and create virtual enviroment by running these lines in terminal:
``
python -m venv venv
``

``
venv\Scripts\activate
``

Install requirements by running this line in terminal
``
pip install -r requirements.txt
``

If you are using windows run this to install dlib package
``
pip install 'app\config\dlib-19.19.0-cp38-cp38-win_amd64.whl'  
``
# How to use 🏆

+ For running API in Dev Environment :

``
  uvicorn just_scan_api:app --reload
``
and run on 
``
http://127.0.0.1:8000/docs
``

+ You have to convert your image from array -> base64 by using image to base64 (ex: https://codebeautify.org/image-to-base64-converter) and then paste your base64 string into input API for running 

