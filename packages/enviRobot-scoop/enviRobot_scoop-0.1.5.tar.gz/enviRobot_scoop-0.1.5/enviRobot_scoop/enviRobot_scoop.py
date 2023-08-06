import asyncio
import json
from .upload_to_imgur import upload_to_imgur
from . import gpt
import random
import string
import os
import re
import sys
import contextlib

os.makedirs('./image', exist_ok=True)

async def async_send_text(websocket, content):
    await websocket.send_text(json.dumps(content))

def async_send(websocket, dic):
    if websocket is None:
        print(dic['message'])
        print('')
    else:
        asyncio.run(async_send_text(websocket, dic))

def random_letters(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))

def find_url(text):
    URL_REGEX = re.compile(r'''((?:mailto:|ftp://|https://)[^\s<>'"{}|\\^`[\]]*)''')
    return URL_REGEX.sub(r'<a href="\1">\1</a>', text)


def text_handler(question:str):
    with contextlib.redirect_stdout(None):
        return_message = []
        image_name = random_letters(10)
        content = gpt.eco_ask_3w_handler(question, image_name)
        return_message.append(find_url(content))
        image_url = upload_to_imgur(f'./image/{image_name}.png')
        os.remove(f'./image/{image_name}.png')
        if '輸入了未來的時間' not in content:
            return_message.append(gpt.gpt_generate_report(content))
            return_message.append(f"<img src={image_url}>")
    return return_message

def location_handler(lat, lon):
    with contextlib.redirect_stdout(None):
        return_message = []
        image_name = random_letters(10)
        content = gpt.location_handler(lat, lon, image_name)
        return_message.append(find_url(content))
        image_url = upload_to_imgur(f'./image/{image_name}.png')
        os.remove(f'./image/{image_name}.png')
        if '輸入了未來的時間' not in content:
            return_message.append(gpt.gpt_generate_report(content))
            return_message.append(f"<img src={image_url}>")
    return return_message

def handle_enviRobot(dic_params, question, websocket):
    #ai_response = f'你好，我是JC，很高興為你服務。你剛剛提問了: {question}。而且妳給我了參數是 {json.dumps(dic_params)}'
    async_send(websocket, {"message":'您好，我是您的AI助手。為了能提供您最精確的服務，我正在仔細解析您的需求。這可能需要大約三分鐘的時間，請您耐心等待，我將儘快回覆您。'})
    try:
        question = json.loads(question)
        if question.get('type')=='coordinates':
            ai_response = location_handler(question.get('lat'), question.get('lon'))

    except json.decoder.JSONDecodeError:
        ai_response = text_handler(question)

    for response in ai_response:
        async_send(websocket, {"message": response})

if __name__ == "__main__":
    str_input = '《環境污染事件通報》第031901號\n一、案由：反映雜草火警，已派七輛消防車前往，火勢面積很大。\n二、地點：龍井區龍興路玉府天宮附近，靠近高速公路\n三、通報來源：消防局\n四、日期：112年03月19日\n (一)報案16:01\n (二)到達:已通報前往'
    #str_input = '永和仁愛公園剛剛發生大火'
    #str_input = '斷稜西山在2023-03-22 10:00:00有人登頂'
    #str_input = '國道五號37路段，五分鐘前看到露天燃燒'
    #str_input = '我上禮拜一下午五點走路經過中正紀念堂看到那邊有黑煙'
    #str_input = '卡米爾有限公司正在開會'

    d, q, w = None, str_input, None
    location = """{
"type": "coordinates",
"lat": 24.191,
"lon": 120.553
}"""
    handle_enviRobot(d, q, w)
    print('\n\n')
    handle_enviRobot(d, location, w)