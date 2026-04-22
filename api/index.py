import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# 初始化客戶端 (放在全域，加速回應)
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

@app.route('/api/action', methods=['POST'])
def handle_action():
    data = request.json
    action = data.get('action')
    san = data.get('san', 100)
    corruption = data.get('corruption', 0)
    
    # --- [🌍 模組化嘗試：世界規則與污染] ---
    # 根據污染度調整「世界觀測者」的態度
    if corruption < 30:
        world_state = "規則穩定，環境尚可理解。"
    elif corruption < 70:
        world_state = "規則開始崩解，玩家感知到不屬於人類的維度。"
    else:
        world_state = "規則完全失效，觀測者已鎖定玩家，文字應充滿扭曲與惡意。"

    system_instruction = f"""
    你是一個克蘇魯風格的敘事引擎。
    當前世界狀態：{world_state}
    限制：描述必須在 30 字內，保持詭異且禁止提供答案。
    """

    prompt = f"玩家嘗試執行：{action}。目前的 SAN={san}, 污染={corruption}。請描述發生的異狀。"

    try:
        # 1. 檢查 API Key 狀態
        if not API_KEY:
            return jsonify({ "text": "錯誤：Vercel 環境變數中找不到 GEMINI_API_KEY", "san": san, "corruption": corruption })

        # 2. 呼叫 Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "system_instruction": system_instruction
            }
        )
        ai_text = response.text

    except Exception as e:
        # --- [🔧 強力除錯模式] ---
        # 這裡會吐出真正的錯誤訊息，例如：403 (地區不支援) 或 401 (金鑰無效)
        ai_text = f"（觀測中斷：{str(e)}）"

    # --- [🧪 數值邏輯] ---
    # 這裡可以根據 action 調整扣除量，先維持固定
    new_san = max(0, san - 5)
    new_corruption = min(100, corruption + 8)

    return jsonify({
        "text": ai_text,
        "san": new_san,
        "corruption": new_corruption
    })

def handler(event, context):
    return app(event, context)
        "san": new_san,
        "corruption": new_corruption
    })

def handler(event, context):
    return app(event, context)
