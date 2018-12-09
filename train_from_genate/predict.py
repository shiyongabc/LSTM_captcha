#coding=utf-8
from train import *


import numpy as np
import tensorflow as tf

from config import *
from PIL import Image
def predict():
    output = crack_captcha_cnn()
    #saver = tf.train.Saver()
    sess = tf.Session()
    print("meta_graph_path=%s,model_path=%s"%(meta_graph_path,model_path))
    saver = tf.train.import_meta_graph(meta_graph_path)
    saver.restore(sess, tf.train.latest_checkpoint(model_path))  # 读取已训练模型


    #saver.restore(sess, tf.train.latest_checkpoint('.'))

    while (1):

        text, image = gen_captcha_text_and_image()
        #image.save(text, test_data_path+'/'+text + '.jpg')  # 写到文件
        image = convert2gray(image)
        image = image.flatten() / 255

        predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
        predict_text = text_list[0].tolist()
        text_list = sess.run(predict, feed_dict={X: [image], keep_prob: 1})

        vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
        i = 0
        for t in predict_text:
            vector[i * 63 + t] = 1
            i += 1
            # break

        print("正确: {}  预测: {}".format(text, vec2text(vector)))

if __name__ == '__main__':
    predict()