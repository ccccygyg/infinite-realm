import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# 使用新版 SDK 初始化客戶端
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/action', methods=['POST'])
def handle_action():
    data = request.json
    action = data.get('action')
    current_san = data.get('san', 100)
    
    prompt = f"你是一個克蘇魯風格遊戲的敘事者。玩家執行了「{action}」，目前理智值為 {current_san}。請用一段 30 字內充滿壓迫感的文字描述玩家看到的詭異現象。"

    try:
        # 新版的生成內容語法
        response = client.models.generate_content(
            model="gemini-2.0-flash", # 使用最新的 2.0 模型，更快更穩
            contents=prompt
        )
        ai_text = response.text
    except Exception as e:
        # 如果還是失敗，我們會看到具體的錯誤原因
        ai_text = f"黑暗中傳來刺耳的磨牙聲... (錯誤原因: {str(e)})"

    new_san = max(0, current_san - 10)

    return jsonify({
        "text": ai_text,
        "san": new_san
    })

def handler(event, context):
    return app(event, context)
