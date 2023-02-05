import time
from towhee.dc2 import pipe, ops, DataCollection
from flask import Flask, request
from flask import jsonify
app = Flask(__name__)


'''
1、 通过flask启动一个python服务，输入入参为图片的url地址，输出为特征的float数组
2、 通过towhee，提取图片向量特征，参考：https://towhee.io/image-text-embedding/taiyi
'''

# towhee 流水线提取图片特征
img_pipe = (
    pipe.input('url')
    .map('url', 'img', ops.image_decode.cv2_rgb())
    .map('img', 'vec',
         ops.image_text_embedding.taiyi(model_name='taiyi-clip-roberta-102m-chinese', modality='image'))
    .output('vec')
)


@app.route('/get_feature', methods=['POST'])
def number_classify():
    start = time.time()
    # 从测试集中取出一张图片
    request_body = request.json
    image_url = request_body['image_url']
    print(image_url)

    data = DataCollection(img_pipe(image_url))
    print(data[0]['vec'])
    print(time.time() - start)

    # 返回
    response = {'feature': data[0]['vec'].tolist()}

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888)