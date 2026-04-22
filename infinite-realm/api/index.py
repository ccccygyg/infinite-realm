import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# 從 Vercel 環境變數讀取金鑰
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

@app.route('/api/action', methods=['POST'])
def handle_action():
    data = request.json
    action = data.get('action')
    current_san = data.get('san', 100)
    
    # 這是給 AI 的大腦指令
    prompt = f"你是一個克蘇魯風格遊戲的敘事者。玩家執行了「{action}」，目前理智值為 {current_san}。請用一段 30 字內充滿壓迫感的文字描述玩家看到的詭異現象。"

    try:
        response = model.generate_content(prompt)
        ai_text = response.text
    except Exception as e:
        ai_text = "黑暗中傳來刺耳的磨牙聲，你無法理解發生了什麼。"

    # 每次行動扣除 10 點理智
    new_san = max(0, current_san - 10)

    return jsonify({
        "text": ai_text,
        "san": new_san
    })

def handler(event, context):
    return app(event, context)
