from django.db import models

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
# from PIL import Image
import io, base64

graph = tf.get_default_graph()

class Photo(models.Model):
    # 保存先ディレクトリの指定
    image = models.ImageField(upload_to='images')

    IMAGE_SIZE = 224 # 画像サイズ
    # MODEL_FILE_PATH = './bottler/ml_models/vgg16_transfer.h5' # モデルファイル
    classes = ["car", "motorbike"]
    num_classes = len(classes)

    def __str__(self):
        """ファイルのURLを返す"""
        return self.file.url
        
    # 引数から画像ファイルを参照して読み込む
    def predict(self):
        model = None
        global graph
        with graph.as_default():
            # model = load_model(self.MODEL_FILE_PATH)
            
            # img_data = self.image.read()
            # img_bin = io.BytesIO(img_data)

            # image = Image.open(img_bin)
            # image = image.convert("RGB")
            # image = image.resize((self.IMAGE_SIZE, self.IMAGE_SIZE))
            # data = np.asarray(image) / 255.0
            # X = []
            # X.append(data)
            # X = np.array(X) 

            # result = model.predict([X])[0]
            # predicted = result.argmax()
            # percentage = int(result[predicted] * 100)

            ## print(self.classes[predicted], percentage)
            # return self.classes[predicted], percentage
            return 'a', 10

    def image_src(self):
        with self.image.open() as img:
            base64_img = base64.b64encode(img.read()).decode()

            return 'data:' + img.file.content_type + ';base64,' + base64_img

    def get_image_path(self, filename):
        """カスタマイズした画像パスを取得する.

        :param self: インスタンス (models.Model)
        :param filename: 元ファイル名
        :return: カスタマイズしたファイル名を含む画像パス
        """
        prefix = 'images/'
        name = str(uuid.uuid4()).replace('-', '')
        extension = os.path.splitext(filename)[-1]
        return prefix + name + extension
