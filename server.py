from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# ⚠️ 这里填入你在连接AI平台的密钥、接口和模型名
API_KEY = "sk-c2e15e482347b7fe37f303bd1b0dda3dd6c92c8085e679b9427a68f491f8c776"
API_URL = "https://lianjieai.top/v1/chat/completions"
MODEL_NAME = "gpt-5.6-sol"
IMAGE_PATH = "cao.jpg"


@app.route('/api/scan', methods=['POST'])
def scan():
    data = request.json
    base64_image = data.get('image')

    if not base64_image:
        return jsonify({"error": "没有收到图片"}), 400

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": "请识别图片里的车牌号和车型，请用 JSON 格式输出，例如：{\"车牌号\": \"川C·12345\", \"车型\": \"吉利几何\"}。只返回JSON。"},
                    {"type": "image_url", "image_url": {"url": base64_image}}
                ]
            }
        ],
        "max_tokens": 150
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"AI平台报错: {response.text}"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # 监听 5000 端口
    app.run(host='0.0.0.0', port=5000)