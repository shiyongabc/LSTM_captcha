#coding=utf-8
from train import *


import numpy as np
import tensorflow as tf

from config import *

def get_test_set():

    target_file_list = os.listdir(test_data_path)   #获取测试集路径下的所有文件
    print("预测的验证码文件:",len(target_file_list))

    #判断条件
    flag = len(target_file_list) // batch_size  #计算待检测验证码个数能被batch size 整除的次数
    batch_len = flag if flag > 0 else 1  #共有多少个batch
    flag2 = len(target_file_list) % batch_size  #计算验证码被batch size整除后的取余
    batch_len = batch_len if flag2 == 0 else batch_len + 1  #若不能整除，则batch数量加1

    print("共生成batch数:",batch_len)
    print("验证码根据batch取余:",flag2)

    batch =  np.zeros([batch_len * batch_size, time_steps, n_input])
    for i, file in enumerate(target_file_list):
        batch[i] = open_iamge(file)
    batch = batch.reshape([batch_len, batch_size, time_steps, n_input])
    return batch, target_file_list #batch_file_name

def open_iamge(file):
    img = Image.open(test_data_path + '/' + file) #打开图片
    img = np.array(img)
    if len(img.shape) > 2:
        img = np.mean(img, -1)  #转换成灰度图像:(26,80,3) =>(26,80)
        img = img / 255
    return img

def predict():
    output = crack_captcha_cnn()
    with tf.Session() as sess:
        saver = tf.train.import_meta_graph(meta_graph_path)
        saver.restore(sess, tf.train.latest_checkpoint(model_path)) #读取已训练模型

        predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
        #test_x, image = get_test_set()  #获取测试集
        test_x="wXw0"
        image=Image.open(test_data_path+"/wXw0.png")
        print("image=%s"%image)
        image = np.array(image)
        image = convert2gray(image)
        image = image.flatten() / 255

        predict_result = []
        for i in range(len(test_x)):
            batch_test_x = test_x[i]
            batch_test_y = np.zeros([batch_size, captcha_num,n_classes])    #创建空的y输入
            test_predict=sess.run(predict, feed_dict={X: [image], keep_prob: 1})
            #test_predict = sess.run(predict, feed_dict={X: batch_test_x, Y:batch_test_y})
            # print(test_predict)
            # predict_result.extend(test_predict)

            for line in test_predict[0]:    #将预测结果转换为字符
                character = ""
                for each in line:
                    character += index2char(each)
                predict_result.append(character)

        predict_result = predict_result[:len(file_list)]    #预测结果
        write_to_file(predict_result, file_list)    #保存到文件
        print("预测结果保存在：", output_path)

def write_to_file(predict_list, file_list):
    with open(output_path, 'a') as f:
        for i, res in enumerate(predict_list):
            if i == 0:
                f.write("id\tfile\tresult\n")
            f.write(str(i) + "\t" + file_list[i] + "\t" + res + "\n")


def predictFromPath(imgPath,text):# imgPath 图片路径  text真实值
    output = crack_captcha_cnn()
    saver = tf.train.Saver()
    sess = tf.Session()
    saver.restore(sess, tf.train.latest_checkpoint(model_path))

    #text, image = gen_captcha_text_and_image()
    captcha_image = Image.open(imgPath)
    image = np.array(captcha_image)

    image = convert2gray(image)
    image = image.flatten() / 255

    predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
    text_list = sess.run(predict, feed_dict={X: [image], keep_prob: 1})
    predict_text = text_list[0].tolist()


    vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
    i = 0
    for t in predict_text:
        vector[i * 63 + t] = 1
        i += 1
        # break

    print("正确: {}  预测: {}".format(text, vec2text(vector)))


def predict1():
    output = crack_captcha_cnn()
    saver = tf.train.Saver()
    sess = tf.Session()
    saver.restore(sess, tf.train.latest_checkpoint(model_path))

    while (1):

        text, image = gen_captcha_text_and_image()
        #image.write(text, test_data_path+'/'+text + '.jpg')  # 写到文件
        image = convert2gray(image)
        image = image.flatten() / 255

        predict = tf.argmax(tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
        text_list = sess.run(predict, feed_dict={X: [image], keep_prob: 1})
        predict_text = text_list[0].tolist()


        vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)
        i = 0
        for t in predict_text:
            vector[i * 63 + t] = 1
            i += 1
            # break

        print("正确: {}  预测: {}".format(text, vec2text(vector)))

if __name__ == '__main__':
    #predict1()
    predictFromPath()