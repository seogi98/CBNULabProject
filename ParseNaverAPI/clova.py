import requests
import uuid
import time
import json
import configparser
import sys

# image_file = './ParseNaverAPI/sampleImage/sample.jpg'
sample_image_file = './ParseNaverAPI/sampleImage/sample.jpg'
sample_json = './ParseNaverAPI/sampleImage/sampleResult/sample.json'

# ClovaOCR 이용해서 결과값 받아오기
def ClovaParse():
    config = configparser.ConfigParser()
    config.read('./ParseNaverAPI/config.ini')

    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo'
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [
        ('file', open(sample_image_file, 'rb'))
    ]
    headers = {
        'X-OCR-SECRET': config['CLOVA']['SECRET_KEY']
    }

    response = requests.request(
        "POST", config['CLOVA']['API_URL'], headers=headers, data=payload, files=files)
    response = json.loads(response.text.encode('utf8'))
    return response

# 결과 저장
def SaveResult(response):
    with open(sample_json, 'w', encoding='utf-8') as file:
        json.dump(response, file, indent=4, ensure_ascii=False)

# 저장된 json 통계 보여주기
def StatResult():
    with open(sample_json, 'r', encoding='utf-8') as file:
        result = json.load(file)
    print("Image Name = {}\nWord Num = {}".format(
        result['images'][0]['name'], len(result['images'][0]['fields'])))
    inferTextList = []
    avgInferConfidence = 0
    for field in result['images'][0]['fields']:
        inferTextList.append(field['inferText'])
        avgInferConfidence += field['inferConfidence']
    avgInferConfidence /= len(result['images'][0]['fields'])
    print("Average InferConfidence = {}".format(avgInferConfidence))
    print("Word List = {}".format(inferTextList))


if __name__ == '__main__':
    # response = ClovaParse()
    # SaveResult(response)
    StatResult()
