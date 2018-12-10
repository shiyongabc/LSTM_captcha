#-*- coding:utf-8 -*

import os


path = os.getcwd()  #项目所在路径

test_data_path=path + '/test_data'
output_path=path + '/result'
meta_graph_path = path + '/model/crack_capcha.model-37100.meta'   #测试结果存放路径 meta_graph
model_path = path + '/model/' #模型存放路径

batch_size = 64  #size of batch
time_steps = 50   #unrolled through 28 time steps #每个time_step是图像的一行像素 height
n_input = 100  #rows of 28 pixels  #width
image_channels = 1  # 图像的通道数
captcha_num = 4 # 验证码中字符个数






