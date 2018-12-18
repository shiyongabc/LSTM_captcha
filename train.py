#-*- coding:utf-8 -*


import tensorflow as tf


from computational_graph_lstm import *
from util import *
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
def train():

    # defining placeholders
    x = tf.placeholder("float",[None,time_steps,n_input], name = "x") #input image placeholder
    y = tf.placeholder("float",[None,captcha_num,n_classes], name = "y")  #input label placeholder

    # computational graph
    opt, loss, accuracy, pre_arg, y_arg = computational_graph_lstm(x, y)

    saver = tf.train.Saver()  # 创建训练模型保存类
    init = tf.global_variables_initializer()    #初始化变量值

    with tf.Session() as sess:  # 创建tensorflow session
        sess.run(init)
        step = 0
        while True:
            batch_x, batch_y = get_batch()
            sess.run(opt, feed_dict={x: batch_x, y: batch_y})   #只运行优化迭代计算图
            los, acc, parg, yarg = sess.run([loss, accuracy, pre_arg, y_arg],feed_dict={x:batch_x,y:batch_y})

            if step % 100 ==0:
                print("训练第%s,准确率为%s"%(step, acc))

            if acc > 0.94:
                saver.save(sess, model_path, global_step=step)
                print("training complete, accuracy:", acc)
                break
            step += 1
                #     break
        #    if iter % 1000 == 0:   #保存模型
        #       saver.save(sess, model_path, global_step=iter)

        # 计算验证集准确率
        valid_x, valid_y = get_batch(data_path=validation_path, is_training=False)
        print("Validation Accuracy:", sess.run(accuracy, feed_dict={x: valid_x, y: valid_y}))

        
if __name__ == '__main__':
    train()

