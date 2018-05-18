from flask import Flask, request
import json
import requests
from chatterbot import ChatBot

# ตรง YOURSECRETKEY ต้องนำมาใส่เองครับจะกล่าวถึงในขั้นตอนต่อๆ ไป
global LINE_API_KEY
# ห้ามลบคำว่า Bearer ออกนะครับเมื่อนำ access token มาใส่
LINE_API_KEY = 'Bearer 88QCq2PnafKdW/mfQg9Vkklmu2uCUWvH4cQytH6n0/Lyc6urYpf4fP5+uJquMuDMUSb4D/p2AlvEdIvd1TckueHqbsiqoIA2Qjc54QUulelXs4HNlX0UUkLHXrt64/bPp9pPYMnq4nJYOSoBnCbkwwdB04t89/1O/w1cDnyilFU='

app = Flask(__name__)
 
@app.route('/')
def index():
    return 'This is chatbot server.'
@app.route('/bot', methods=['POST'])

def bot():
    # ข้อความที่ต้องการส่งกลับ
    replyQueue = list()
   
    # ข้อความที่ได้รับมา
    msg_in_json = request.get_json()
    msg_in_string = json.dumps(msg_in_json)
    
    # Token สำหรับตอบกลับ (จำเป็นต้องใช้ในการตอบกลับ)
    replyToken = msg_in_json["events"][0]['replyToken']
    
    # ส่วนนี้ดึงข้อมูลพื้นฐานออกมาจาก json (เผื่อ)
    userID =  msg_in_json["events"][0]['source']['userId']
    msgType =  msg_in_json["events"][0]['message']['type']
    
    # ตรวจสอบว่า ที่ส่งเข้ามาเป็น text รึป่าว (อาจเป็น รูป, location อะไรแบบนี้ได้ครับ)
    # แต่ก็สามารถประมวลผลข้อมูลประเภทอื่นได้นะครับ
    # เช่น ถ้าส่งมาเป็น location ทำการดึง lat long ออกมาทำบางอย่าง เป็นต้น
    if msgType != 'text':
        reply(replyToken, ['Only text is allowed.'])
        return 'OK',200
    
    # ตรงนี้ต้องแน่ใจว่า msgType เป็นประเภท text ถึงเรียกได้ครับ 
    # lower เพื่อให้เป็นตัวพิมพ์เล็ก strip เพื่อนำช่องว่างหัวท้ายออก ครับ
    text = msg_in_json["events"][0]['message']['text'].lower().strip()
    

    replyQueue.append(text)
    replyQueue.append("okay")
    replyQueue.append((open("test.txt","r").readlines(0))[0])
    #MyBot = ChatBot("Pink Bot",
                    #storage_adapter='chatterbot.storage.SQLStorageAdapter',
                    #database='db.sqlite3',
                    #read_only = True) 
    #eplyQueue.append(str(MyBot.get_response(msg)))
    
    reply(replyToken, replyQueue[:5])
    
    return 'OK', 200
 
def reply(replyToken, textList):
    # Method สำหรับตอบกลับข้อความประเภท text กลับครับ เขียนแบบนี้เลยก็ได้ครับ
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': LINE_API_KEY
    }
    msgs = []
    for text in textList:
        msgs.append({
            "type":"text",
            "text":text
        })
    data = json.dumps({
        "replyToken":replyToken,
        "messages":msgs
    })
    requests.post(LINE_API, headers=headers, data=data)
    return
    
if __name__ == '__main__':
    app.run()
