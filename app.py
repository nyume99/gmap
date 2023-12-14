from flask import Flask, request
import subprocess

app = Flask(__name__)


@app.route('/run_spider', methods=['POST'])
def run_spider():
    data = request.json

    print(data)

    # スパイダーをバックグラウンドで実行し、パラメータを渡す
    subprocess.Popen(['scrapy', 'crawl', data.spider, '-a', f'arg1={data.keys}'])
    return "Spider started"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
