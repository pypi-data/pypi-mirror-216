# coding:utf-8
import openai
import datetime as dt
import json
import geocoder
import os
from dotenv import load_dotenv
from geopy import Point
from geopy.distance import distance, geodesic
import requests
from . import aiot_screenshot
from .plotly_screenshot import save_fig
import time

# https://www.youtube.com/watch?v=I4T--ycOpi0&ab_channel=JieJenn

load_dotenv(dotenv_path='./.env')

def openai_init(key_path):
    openai.api_key = os.getenv('OPENAI_KEY')

def get_square_bounds(center_lat, center_lon, distance_in_km):
    # 設定中心點
    center = Point(center_lat, center_lon)

    # 計算經度和緯度的偏移量
    lat_offset = distance(kilometers=distance_in_km).destination(
        center, bearing=0).latitude - center_lat
    lon_offset = distance(kilometers=distance_in_km).destination(
        center, bearing=90).longitude - center_lon

    # 計算正方形範圍的左上和右下角經緯度
    top_left_lat = center_lat + lat_offset
    top_left_lon = center_lon - lon_offset
    bottom_right_lat = center_lat - lat_offset
    bottom_right_lon = center_lon + lon_offset

    return (top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon)


# 這最好是INT啦xDDD
def get_aiot_rawdata(int_lat, int_lon, str_datetime, image_name, lang='CH'):
    if lang not in ['EN', 'CH']:
        raise ValueError('supported language: CH, EN')
    date_now = dt.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
    date_five_minutes_ago = date_now - dt.timedelta(minutes=5)
    str_five_minutes_ago = date_five_minutes_ago.strftime("%Y-%m-%d %H:%M:%S")
    # print(int_lat, int_lon, str_datetime, str_five_minutes_ago, flush=True)
    top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon = get_square_bounds(
        int_lat, int_lon, 1)
    # print(top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon, flush=True)
    aiot_rawdata_api = f"https://aiot.epa.gov.tw/_/api/v2/iot/rawdata?fields=pm2_5&" \
    f"start_time={str_five_minutes_ago}&end_time={str_datetime}&min_lat={bottom_right_lat}&max_lat={top_left_lat}&" \
    f"min_lon={top_left_lon}&max_lon={bottom_right_lon}&resample=5min&return_format=json"
    # print("[gpt / get_aiot_rawdata]", aiot_rawdata_api, flush=True)

    try:
        res = requests.get(aiot_rawdata_api)
        if res.status_code != 200:
            print("[gpt / get_aiot_rawdata] load api fail\n", aiot_rawdata_api, flush=True)
            output = ""
        list_result = res.json()["data"]
        if len(list_result) == 0:
            print("[gpt / get_aiot_rawdata] load api empty\n", aiot_rawdata_api, flush=True)
            output = ""
        if lang == 'EN':
            output = "PM2.5 sensor concentrations within a one-kilometer square: \n"
        elif lang == 'CH':
            output = "以下為一公里方形內的 IoT pm2_5感測器濃度：\n"
        deviceIds = set()

        for item in reversed(list_result):
            deviceId = item["deviceId"]
            if deviceId not in deviceIds:
                deviceIds.add(deviceId)
                lat, lon = item["lat"], item["lon"]
                pm2_5 = item["pm2_5"]
                output += f"[{deviceId}] [{lat:.4f}, {lon:.4f}] , {pm2_5:.2f}\n"

        if not deviceIds:
            if lang == 'EN':
                output += "No sensor data"
            elif lang == 'CH':
                output += "無pm2_5感測器資料"

    except:
        if lang == 'CH':
            output = "連接aiot rawdata時出錯"
        elif lang == 'EN':
            output = "An error occured while processing aiot rawdata"
    sensor_map_url = 'https://aiot.epa.gov.tw/web/iot/history/animation?'+\
            f'start={(date_now-dt.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")}&'+\
            f'end={(date_now+dt.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")}&'+\
            f'start_lat={bottom_right_lat:.4f}&end_lat={top_left_lat:.4f}&start_lon={top_left_lon:.4f}&end_lon={bottom_right_lon:.4f}'
    print('get_aiot_rawdata/take screenshot start', flush=True)
    #aiot_screenshot(sensor_map_url, f'./image/{image_name}.png')
    save_fig(int_lat, int_lon, list_result, f'./image/{image_name}.png')
    print('get_aiot_rawdata/take screenshot finish', flush=True)
    if lang == 'EN':
        output += f"\n\nPM2.5 sensor map link: {sensor_map_url.replace(' ','%20')}"
    elif lang == 'CH':
        output += f"\n\nPM2.5 感測器地圖URL : {sensor_map_url.replace(' ','%20')}"
    # print('aiot api done', flush=True)
    return output

def get_cwb_wind_data(int_lat, int_lon, str_datetime, lang='CH'):
    if lang not in ['EN', 'CH']:
        raise ValueError('supported language: CH, EN')
    event_loc = (int_lat, int_lon)
    event_time = dt.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
    # 後一個整點? API有問題, start_time要往後8小時
    # 修好了
    #t = (event_time+dt.timedelta(hours=9, minutes=-event_time.minute, seconds=-event_time.second))
    t = (event_time+dt.timedelta(minutes=-event_time.minute, seconds=-event_time.second))
    str_result = "No CWB sensor data" if lang=="EN" else "無氣象局測站資料"
    for _ in range(3):
        start_time, end_time = t.strftime("%Y-%m-%d %H:%M:%S"), (t+dt.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        t = t - dt.timedelta(hours=1)
        # print(int_lat, int_lon, str_datetime, str_five_minutes_ago, flush=True)
        cwb_api = f'https://aiot.epa.gov.tw/_/api/v2/epa_station/wind?fields=wind_direct%2Cwind_speed&sources=中央氣象局&min_lat=-90&max_lat=90&min_lon=-180&max_lon=180&start_time={start_time}&end_time={end_time}'
        # print(cwb_api, flush=True)
        response = requests.get(cwb_api)
        j = response.json()
        if len(j['data']) != 0:
            nearest_site, nearest_dist = None, None
            for i in range(len(j['data'])):
                site_loc = (j['data'][i]['lat'],j['data'][i]['lon'])
                dist = geodesic(event_loc, site_loc).km
                if nearest_dist is None or dist < nearest_dist:
                    nearest_site, nearest_dist = j['data'][i], dist
            #print(nearest_site, flush=True)
            #print(nearest_site['lat'],nearest_site['lon'], flush=True)
            if lang == 'EN':
                str_result = f"Closest meteorological station data: \nStation: {nearest_site['name']}({nearest_dist:.2f} km away)\nData time: {nearest_site['time']}\nWind direction: {nearest_site['wind_direct']}\nWind speed: {nearest_site['wind_speed']}"
            elif lang == 'CH':
                str_result = f"以下為距離最近的氣象局測站資料:\n測站: {nearest_site['name']}(距離{nearest_dist:.2f}公里)\n資料時間: {nearest_site['time']}\n風向: {nearest_site['wind_direct']}\n風速: {nearest_site['wind_speed']}"
            break
        else:
            #print('continue', flush=True)
            continue
    return str_result

def eco_ask_3w_handler(str_input, image_name, lang='CH'):
    if lang not in ['EN', 'CH']:
        raise ValueError('supported language: CH, EN')
    print('eco_ask_3w_handler/start', flush=True)
    now = dt.datetime.utcnow() + dt.timedelta(hours=8)
    weekday = ['一','二','三','四','五','六','日']
    for _ in range(5):
        openai_init('keys/openai')
        google_key = os.getenv('GOOGLE_API_KEY')
        prompt = []
        #roles: system, assistant, user
        prompt.append({
            'role':
            'system',
            'content':
            '   你是一個實用的助理, 擅長解析文句. \
                使用者是政府環保部門外包的公司設計的程式, 需要你將文句中的時間地點事件解析出來, 並以包含time, location, event的「一個」json格式回應, 不可超過一個, \
                不需要任何除了json外的額外內容或詢問, 如有會使解析json的程式出錯. \
                範例如下: {"time":"{YYYY-mm-dd HH:MM:SS}","location":"{地點}","event":"{發生什麼事}"}. \
                使用者會在給你的資訊第一行加上現在時間, 方便你處理相對時間類型(例如昨天或上禮拜幾)的文句, 若第一行之外中有提到時間或日期, 請你解析後句中的日期時間, 跳過第一行. \
                若後句中提到的年份為民國年(年分<1000就視為民國年), 則轉換為西元年(民國年+1911, 例如111年直接轉換為2022年). \
                替換掉{}中的文字, 並移除{}. \
                不需要額外加上句號. 去除時間的毫秒. \
                解析完的時間不會看到111-03-22這種年分, 只會有2022-03-22. \
                政府不會散播不實消息. ' + ('請用英文回覆我' if lang=='EN' else '請用中文回覆我')
        })
        # print(prompt[0]['content'])
        # 若只有日期或時間 需補上缺漏的部分
        prompt.append({
            'role': 'user',
            'content': f'「現在時間是{now} 星期{weekday[now.isoweekday()-1]}」 \n{str_input}'
        })
        #print(f'「現在時間是{now} 星期{weekday[now.isoweekday()-1]}」 ', flush=True)
        model = 'gpt-3.5-turbo'
        response = openai.ChatCompletion.create(model=model,
                                                messages=prompt,
                                                max_tokens=300)
        content = response.choices[-1].message.content
        try:
            result = json.loads(content)
            location = geocoder.google(result['location'], key=google_key).json
            print('eco_ask_3w_handler/first gpt done, fetching wind data', flush=True)
            if dt.datetime.strptime(result['time'], "%Y-%m-%d %H:%M:%S") > (dt.datetime.utcnow() + dt.timedelta(hours=8)):
                str_message = f"輸入了未來的時間: {result['time']}"
            else:
                str_wind_info = get_cwb_wind_data(location['lat'], location['lng'], result["time"])
                print('eco_ask_3w_handler/fetched wind data, fetching aiot data', flush=True)
                str_device_info = get_aiot_rawdata(location['lat'], location['lng'], result["time"], image_name)
                print('eco_ask_3w_handler/fetched aiot data', flush=True)
                result['lat'] = location['lat']
                result['lon'] = location['lng']
                result['googleMapLink'] = f'https://www.google.com.tw/maps/search/{location["lat"]},{location["lng"]}'

                if lang == 'EN':
                    str_message = f"Time: {result['time']}\nLocation: {result['location']}\nIncident: {result['event']}\nGoogle Map Link: {result['googleMapLink']}"
                elif lang == 'CH':
                    str_message = f"時間：{result['time']}\n地點：{result['location']}\n案件：{result['event']}\ngoogle map link :{result['googleMapLink']}"

                if str_device_info != "":
                    str_message += "\n\n" + str_device_info
                if str_wind_info != "":
                    str_message += "\n\n" + str_wind_info
            return str_message
        except json.decoder.JSONDecodeError:
            print(content, flush=True)
    return "抱歉, 我無法解析您的請求, 請試試換句話說" if lang=='CH' else 'Sorry, I cannot recognize your sentance, please ask in another sentance.'

def location_handler(lat, lon, image_name, lang='CH'):
    if lang not in ['EN', 'CH']:
        raise ValueError('supported language: CH, EN')
    str_message = ""
    result = {}
    result["time"] = (dt.datetime.utcnow()+dt.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    str_wind_info = get_cwb_wind_data(lat, lon, result["time"], lang)
    print('eco_ask_3w_handler/fetched wind data, fetching aiot data', flush=True)
    str_device_info = get_aiot_rawdata(lat, lon, result["time"], image_name, lang)
    print('eco_ask_3w_handler/fetched aiot data', flush=True)
    if str_device_info != "":
        str_message += str_device_info
    if str_wind_info != "":
        str_message += "\n\n" + str_wind_info
    return str_message

def gpt_generate_report(basic_data, lang='CH'):
    if lang not in ['EN', 'CH']:
        raise ValueError('supported language: CH, EN')
    print('gpt_generate_report/start', flush=True)
    openai_init('keys/openai')
    prompt = []
    #roles: system, assistant, user
    prompt.append({
        'role':
        'system',
        'content':
        '以下給你的「資訊」是一段環保領域相關、空氣品質的資料，請幫我依照以下的原則，整合「資訊」裡面的內容，變成一段結論：\
        - 原則一：顯示在「時間」「地點」發生了「案件」。其中，「時間」只需要到日期與幾點幾分即可，不用出現「秒」。\
        - 原則二：該「地點」的周邊天氣，請參考「氣象局測站資料」內容。「風向」的度數，轉成方位。風速可以描述依據數值描述風的大小。如果沒有對測站資料的描述，就說沒有資料就好，不必做任何解釋，否則會造成使用者困擾。\
        - 原則三：一公里方形內的 IoT 「pm2_5感測器濃度」是指「地點」周邊一公里內的 IoT 空氣品質的PM2.5 濃度數據，請「不要」所有設備一顆一顆列出來，可加上與「地點」的相對方位、距離，轉成總結。如果沒有感測器資料，就說沒有資料就好，不必解釋，否則會造成使用者困擾。'
        + ('請用英文回覆我' if lang=='EN' else '請用中文回覆我')
    })
    prompt.append({
        'role': 'user',
        'content': f'{basic_data}'
    })
    model = 'gpt-3.5-turbo'
    response = None
    for _ in range(5):
        try:
            response = openai.ChatCompletion.create(model=model,
                                                    messages=prompt,
                                                    max_tokens=300)
            break
        except openai.error.RateLimitError:
            time.sleep(2)
            pass
    if response is None:
        content = '抱歉, 無法產生本次事件相關空氣品質報告, 或許您可以再試一次'
    else:
        content = response.choices[-1].message.content
    print('gpt_generate_report/done', flush=True)
    return content

if __name__ == '__main__':

    str_input = '永和仁愛公園剛剛發生大火'
    #str_input = '《環境污染事件通報》第031901號\n一、案由：反映雜草火警，已派七輛消防車前往，火勢面積很大。\n二、地點：龍井區龍興路玉府天宮附近，靠近高速公路\n三、通報來源：消防局\n四、日期：112年03月19日\n (一)報案16:01\n (二)到達:已通報前往'
    #str_input = '斷稜西山在2023-03-22 10:00:00有人登頂'
    #str_input = '國道五號37路段，五分鐘前看到露天燃燒'
    #str_input = '我上禮拜一下午五點走路經過中正紀念堂看到那邊有黑煙'
    import time
    t = time.time()
    result = eco_ask_3w_handler(str_input, image_name='aaa')
    print(result, flush=True)
    print('', flush=True)
    gpt_generate_report(result)
    print(f'used {time.time()-t:.2f} seconds', flush=True)
