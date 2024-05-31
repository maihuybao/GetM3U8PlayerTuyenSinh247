import re
import requests
import json
from Crypto.Cipher import AES
import base64
import binascii


config = json.load(open("config.json"))

def get_link(key_hex, iv_hex, b64_data):
    key = binascii.unhexlify(key_hex)
    iv = binascii.unhexlify(iv_hex)
    encrypted_data = base64.b64decode(b64_data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    decrypted_data = decrypted_data.rstrip(b'\0')
    
    return decrypted_data.decode('utf-8')


def getTopicID(url):
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8,nl;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://tuyensinh247.com',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
    }

    response = requests.get(url, headers=headers)


    findtopicid= re.findall(r'"topicHeader viewTopicDetail" data-id="(.+?)"', response.text)
    #class="topicTitle bold textBlue">Chuyên đề 2. Vectơ và hệ trục toạ độ trong không gian</a>
    findnametopic= re.findall(r'class="topicTitle bold textBlue">(.+?)</a>', response.text)
    result = {}
    for i in range(len(findtopicid)):
        result[findtopicid[i]] = findnametopic[i]
    return result




# print(getTopicID("https://tuyensinh247.com/s1-thay-chinh-toan-12-ket-noi-tri-thuc-voi-cuoc-song-nam-2025-k2995.html"))


def getTopicInfo(id):
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8,nl;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': config["cookie"], 
        'dnt': '1',
        'origin': 'https://tuyensinh247.com',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'topicId': id,
    }

    response = requests.post('https://tuyensinh247.com/eLessonOnline/loadTopicInfo', headers=headers, data=data)
    #print json beutify
    # open("topic.json", "w",encoding="utf-8").write(json.dumps(response.json(), indent=4))
    return response.json()

# print(getTopicInfo("16412"))
# exit()
def getPartLession(data):
    url = "https://tuyensinh247.com" + data["url"]
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'vi,en-US;q=0.9,en;q=0.8,nl;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': config["cookie"], 
        'dnt': '1',
        'origin': 'https://tuyensinh247.com',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
    }
    response = requests.get(url, headers=headers)
    # open("test.html", "w",encoding="utf-8").write(response.text)
    # """<li id="video_178402" data-order="1" data-id="178402" data-time=""
    #                             data-origin-video-id="46647" class="active">
    #                             <p>1. Phần 1</p>
    #                             <p>27:33</p>
    #                         </li>"""
    id_lesson = re.findall(r'<li id="video_(.+?)"', response.text)
    name = re.findall(r'<p>(.+?)</p>', response.text)
    
    # m3u8player = 
    result = {}
    idx = "rnd_idx_" + re.findall(r"#rnd_idx_(.+?)", response.text)[0]
    #<input type="hidden" value="525472337e545e10fe3b49a05fefb4662035b985f38b2f040eb408412018b51e" id="rnd_idx_0">
    key_hex = re.findall(r'<input type="hidden" value="(.+?)" id="'+idx+'">', response.text)[0]
    iv_hex = "31333537393234363830363534333231"
    # print(idx,key_hex, iv_hex)
    
    videolink = ""
    type = 1
    if ("if (1 === 1) {" in response.text):
        type = 0
    
    for i in range(len(id_lesson)):
        videolink = re.findall(r"hlsVideoLink\["+id_lesson[i]+"\] = '(.+?)';", response.text)[type]
        hdvideolink = re.findall(r"hdHlsVideoLink\["+id_lesson[i]+"\] = '(.+?)';", response.text)
        if hdvideolink != []:
            videolink = hdvideolink[type]
        #rnd_idx_0
        result[id_lesson[i]] = {"name":name[i*2],"url":get_link(key_hex, iv_hex, videolink)}
        
    # print(result)
    return result;
    
listurl = open("url.txt", "r").read().split("\n")
for url in listurl:
    topicid = getTopicID(url)
    output = ""
    for topic in topicid:
        datatopic = getTopicInfo(topic)["msg"]
        # print(datatopic)
        # print(topicid[topic])
        output += f"{topicid[topic]}\n"
        print(f"{topicid[topic]}")
        for lession in datatopic:
            # print(lession)
            output += f"{lession['title']}\n"
            print(lession['title'])
            if ((lession["number_ask"] == None) and (lession["total_video"] != "0") and (lession["release_label"] == "Đã phát hành")):
                # print(lession["title"])
                
                listpart = getPartLession(lession)
                # print(listpart)
                for part in listpart:
                    # print(listpart[part])
                    output += f"{listpart[part]['name']}|{listpart[part]['url']}\n"
                    print(f"{listpart[part]['name']}|{listpart[part]['url']}")
                    
                    

open("output.txt", "w",encoding="utf-8").write(output)