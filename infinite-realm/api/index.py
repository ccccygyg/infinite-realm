from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/action', methods=['POST'])
def handle_action():
    data = request.json
    action = data.get('action')
    current_san = data.get('san', 100)
    
    # 這裡未來可以接入 AI (Gemini/OpenAI)
    # 現在我們先用簡單的邏輯模擬
    new_san = current_san
    response_text = ""

    if action == "observe":
        response_text = "你觀察四周，發現牆壁上有無數隻眼睛在眨動。"
        new_san -= 10
    elif action == "think":
        response_text = "你試圖思考目前的處境，但腦袋裡充滿了刺耳的蟬鳴聲。"
        new_san -= 5
    
    return jsonify({
        "text": response_text,
        "san": max(0, new_san),
        "status": "OBSERVED" if new_san < 50 else "STABLE"
    })

# Vercel 需要這個
def handler(event, context):
    return app(event, context)