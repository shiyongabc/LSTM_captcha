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
        #predict_text = text_list[0].tolist()
        test_predict = sess.run(predict, feed_dict={X: [image], keep_prob: 1})
        predict_result = []
        vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
        for line in test_predict[0]:  # 将预测结果转换为字符
            character = ""
            for each in line:
                character += index2char(each)
            predict_result.append(character)
        predict_result = predict_result[:len(file_list)]    #预测结果
        write_to_file(predict_result, file_list)    #保存到文件

def write_to_file(predict_list, file_list):
    with open(output_path, 'a') as f:
        for i, res in enumerate(predict_list):
            if i == 0:
                f.write("id\tfile\tresult\n")
            f.write(str(i) + "\t" + file_list[i] + "\t" + res + "\n")
    print("预测结果保存在：",output_path)


if __name__ == '__main__':
    predict()