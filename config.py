#-*- coding:utf-8 -*

import os


path = os.getcwd()  #项目所在路径

captcha_path = path + '/train_data_dianwang'  #训练集-验证码所在路径
validation_path = path + '/validation_data_dianwang' #验证集-验证码所在路径
test_data_path = path + '/test_data_dianwang'    #测试集-验证码文件存放路径
output_path = path + '/result/result_dianwang.txt'   #测试结果存放路径
model_path = path + '/model/dianwang_model.ckpt' #模型存放路径

meta_graph=path+'/model/model.ckpt-5405.meta'
moudke_file=path+'/model/'

#要识别的字符
number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


batch_size = 64  #size of batch
time_steps = 50   #unrolled through 28 time steps #每个time_step是图像的一行像素 height
n_input = 100  #rows of 28 pixels  #width
image_channels = 1  # 图像的通道数
captcha_num = 4 # 验证码中字符个数
n_classes = len(number) + len(ALPHABET)+ len(alphabet)    #类别分类

learning_rate = 0.001   #learning rate for adam
num_units = 128   #hidden LSTM units
layer_num = 2   #网络层数
iteration = 10000   #训练迭代次数


