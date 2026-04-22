import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/api/action', methods=['POST'])
def handle_action():
    data = request.json
    action = data.get('action')
    san = data.get('san', 100)
    corruption = data.get('corruption', 0) # 新增污染值
    
    # 動態調整 AI 的壓迫程度
    system_instruction = "你是一個詭異世界的敘事引擎。必須展現壓迫感與不合理性。"
    if corruption > 50:
        system_instruction += "注意：玩家已被嚴重污染，請在描述中加入一些亂碼、重複的字，或描述玩家身體的異變。"

    prompt = f"""
    {system_instruction}
    玩家動作：{action}
    目前數值：SAN={san}, 污染度={corruption}
    請用 30 字內描述結果。
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        ai_text = response.text
    except Exception as e:
        ai_text = "（系統被強烈干擾，無法解析觀測結果...）"

    # 邏輯計算
    new_san = max(0, san - 5)
    new_corruption = min(100, corruption + 8) # 每次行動增加污染

    return jsonify({
        "text": ai_text,
        "san": new_san,
        "corruption": new_corruption
    })

def handler(event, context):
    return app(event, context)
