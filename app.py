from flask import Flask, request
import subprocess
import json

app = Flask(__name__)


@app.route('/run_spider', methods=['POST'])
def run_spider():
    data = request.get_json()
    spider = data['spider']
    array = data['keys']


    #print(request.spider)

    # スパイダーをバックグラウンドで実行し、パラメータを渡す
    subprocess.Popen(['scrapy', 'crawl', spider, '-a', f'array={json.dumps(array)}'])
    return "Spider started"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
