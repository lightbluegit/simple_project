from flask import Flask, render_template, request, jsonify  # Flask核心功能
import random  # 随机打乱单词顺序
app = Flask(__name__)# 创建Flask应用实例

# 文件路径配置
WORDS_PATH = 'recite word app/words.txt'
def load_words():
    try:
        with open(WORDS_PATH, 'r', encoding='utf-8') as f:
            words = []
            for line in f:
                try:
                    if line.strip() and not line.startswith('#'):
                        parts = line.strip().split(':')
                        words.append(parts)
                except Exception as e:
                    print(f"Error parsing line: {line}, error: {e}")
            # print(words)
            return words
    except Exception as e:
        print(f"Error loading words: {e}")
        return []


@app.route('/')
def index():
    return render_template('index.html')#渲染HTML模板

@app.route('/api/words', methods=['GET'])
def get_words():
    words = load_words()
    random_mode = True
    if random_mode:
        random.shuffle(words)
    return jsonify(words)

if __name__ == '__main__':
    print("正在启动Flask服务...")
    
    try:
        print(f"服务将在 http://10.152.213.20:5000 启动")
        app.run(host='10.152.213.20', port=5000, debug=True)
    except Exception as e:
        print(f"启动失败: {str(e)}")
        print("尝试使用其他端口...")
        app.run(host='10.152.213.20', port=5001, debug=True)
