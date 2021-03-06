#coding=utf-8

#from train_from_genate.gen_captcha import *


import numpy as np
import tensorflow as tf
from gen_captcha import *
from config import *
import os
"""
text, image = gen_captcha_text_and_image()
print  "验证码图像channel:", image.shape  # (60, 160, 3)
# 图像大小
IMAGE_HEIGHT = 60
IMAGE_WIDTH = 160
MAX_CAPTCHA = len(text)
print   "验证码文本最长字符数", MAX_CAPTCHA  # 验证码最长4字符; 我全部固定为4,可以不固定. 如果验证码长度小于4，用'_'补齐
"""
IMAGE_HEIGHT = time_steps
IMAGE_WIDTH = n_input
MAX_CAPTCHA = captcha_num
path = os.getcwd()  #项目所在路径


# 把彩色图像转为灰度图像（色彩对识别验证码没有什么用）
def convert2gray(img):
    if len(img.shape) > 2:
        gray = np.mean(img, -1)
        # 上面的转法较快，正规转法如下
        # r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
        # gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray
    else:
        return img


"""
cnn在图像大小是2的倍数时性能最高, 如果你用的图像大小不是2的倍数，可以在图像边缘补无用像素。
np.pad(image,((2,3),(2,2)), 'constant', constant_values=(255,))  # 在图像上补2行，下补3行，左补2行，右补2行
"""

# 文本转向量
char_set = number + alphabet + ALPHABET + ['_']  # 如果验证码长度小于4, '_'用来补齐
CHAR_SET_LEN = len(char_set)


def text2vec(text):
    text_len = len(text)
    if text_len > MAX_CAPTCHA:
        raise ValueError('验证码最长4个字符')

    vector = np.zeros(MAX_CAPTCHA * CHAR_SET_LEN)

    def char2pos(c):
        if c == '_':
            k = 62
            return k
        k = ord(c) - 48
        if k > 9:
            k = ord(c) - 55
            if k > 35:
                k = ord(c) - 61
                if k > 61:
                    raise ValueError('No Map')
        return k

    for i, c in enumerate(text):
        #print text
        idx = i * CHAR_SET_LEN + char2pos(c)
        #print i,CHAR_SET_LEN,char2pos(c),idx
        vector[idx] = 1
    return vector

#print text2vec('1aZ_')

# 向量转回文本
def vec2text(vec):
    char_pos = vec.nonzero()[0]
    text = []
    for i, c in enumerate(char_pos):
        char_at_pos = i  # c/63
        char_idx = c % CHAR_SET_LEN
        if char_idx < 10:
            char_code = char_idx + ord('0')
        elif char_idx < 36:
            char_code = char_idx - 10 + ord('A')
        elif char_idx < 62:
            char_code = char_idx - 36 + ord('a')
        elif char_idx == 62:
            char_code = ord('_')
        else:
            raise ValueError('error')
        text.append(chr(char_code))
    return "".join(text)


"""
#向量（大小MAX_CAPTCHA*CHAR_SET_LEN）用0,1编码 每63个编码一个字符，这样顺利有，字符也有
vec = text2vec("F5Sd")
text = vec2text(vec)
print(text)  # F5Sd
vec = text2vec("SFd5")
text = vec2text(vec)
print(text)  # SFd5
"""

def get_batch(data_path = captcha_path, is_training = True,batch=64):
    target_file_list = os.listdir(data_path)    #读取路径下的所有文件名

    batch = batch_size if is_training else len(target_file_list)   # 确认batch 大小
    batch_x = np.zeros([batch, time_steps, n_input])   #batch 数据
    batch_y = np.zeros([batch, captcha_num, n_classes])   # batch 标签


    for i in range(batch):
        file_name = random.choice(target_file_list) if is_training else target_file_list[i] #确认要打开的文件名
        img = Image.open(data_path + '/' + file_name) #打开图片
        img = np.array(img)
        if len(img.shape) > 2:
            img = np.mean(img, -1)  #转换成灰度图像:(26,80,3) =>(26,80)
            img = img / 255   #标准化，为了防止训练集的方差过大而导致的收敛过慢问题。
            # img = np.reshape(img,[time_steps,n_input])  #转换格式：(2080,) => (26,80)
        batch_x[i] = img

        label = np.zeros(captcha_num * n_classes)
        #print("file_name=%s"%file_name)
        for num, char in enumerate(file_name.split('.')[0]):
            index = num * n_classes + char2index(char)
            label[index] = 1
        label = np.reshape(label,[captcha_num, n_classes])
        batch_y[i] = label
    return batch_x, batch_y


def char2index(c):
    k = ord(c)
    index = -1
    if k >= 48 and k <= 57: #数字索引
        index = k - 48
    if k >= 65 and k <= 90: #大写字母索引
        index = k - 55
    if k >= 97 and k <= 122: #小写字母索引
        index = k - 61
    if index == -1:
        raise ValueError('No Map')
    return index


def index2char(k):
    # k = chr(num)
    index = -1
    if k >= 0 and k < 10: #数字索引
        index = k + 48
    if k >= 10 and k < 36: #大写字母索引
        index = k + 55
    if k >= 36 and k < 62: #小写字母索引
        index = k + 61
    if index == -1:
        raise ValueError('No Map')
    return chr(index)

# 生成一个训练batch
def get_next_batch(batch_size=128):
    batch_x = np.zeros([batch_size, IMAGE_HEIGHT * IMAGE_WIDTH])
    batch_y = np.zeros([batch_size, MAX_CAPTCHA * CHAR_SET_LEN])

    # 有时生成图像大小不是(50, 100, 3)
    def wrap_gen_captcha_text_and_image():
        while True:
            text, image = gen_captcha_text_and_image()
            if image.shape == (50, 100, 3):
                return text, image

    for i in range(batch_size):
        text, image = wrap_gen_captcha_text_and_image()
        image = convert2gray(image)

        batch_x[i, :] = image.flatten() / 255  # (image.flatten()-128)/128  mean为0
        batch_y[i, :] = text2vec(text)

    return batch_x, batch_y


####################################################################

X = tf.placeholder(tf.float32, [None, IMAGE_HEIGHT * IMAGE_WIDTH])
Y = tf.placeholder(tf.float32, [None, MAX_CAPTCHA * CHAR_SET_LEN])
keep_prob = tf.placeholder(tf.float32)  # dropout


# 定义CNN
def crack_captcha_cnn(w_alpha=0.01, b_alpha=0.1):
    x = tf.reshape(X, shape=[-1, IMAGE_HEIGHT, IMAGE_WIDTH, 1])

    # w_c1_alpha = np.sqrt(2.0/(IMAGE_HEIGHT*IMAGE_WIDTH)) #
    # w_c2_alpha = np.sqrt(2.0/(3*3*32))
    # w_c3_alpha = np.sqrt(2.0/(3*3*64))
    # w_d1_alpha = np.sqrt(2.0/(8*32*64))
    # out_alpha = np.sqrt(2.0/1024)

    # 3 conv layer  N = (W − F + 2P )/S+1
    w_c1 = tf.Variable(w_alpha * tf.random_normal([3, 3, 1, 32]))
    b_c1 = tf.Variable(b_alpha * tf.random_normal([32]))
    conv1 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(x, w_c1, strides=[1, 1, 1, 1], padding='SAME'), b_c1))
    conv1 = tf.nn.max_pool(conv1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv1 = tf.nn.dropout(conv1, keep_prob)
   # print(conv1.shape)

    w_c2 = tf.Variable(w_alpha * tf.random_normal([3, 3, 32, 64]))
    b_c2 = tf.Variable(b_alpha * tf.random_normal([64]))
    conv2 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv1, w_c2, strides=[1, 1, 1, 1], padding='SAME'), b_c2))
    conv2 = tf.nn.max_pool(conv2, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')
    conv2 = tf.nn.dropout(conv2, keep_prob)
    print(conv2.shape)

    w_c3 = tf.Variable(w_alpha * tf.random_normal([3, 3, 64, 64]))
    b_c3 = tf.Variable(b_alpha * tf.random_normal([64]))
    conv3 = tf.nn.relu(tf.nn.bias_add(tf.nn.conv2d(conv2, w_c3, strides=[1, 1, 1, 1], padding='SAME'), b_c3))
    conv3 = tf.nn.max_pool(conv3, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1], padding='SAME')
    print(conv3.shape)
    conv3 = tf.nn.dropout(conv3, keep_prob)
    print(conv3.shape)

    # Fully connected layer  8 * 32 * 40  10240  5120   372736
    w_d = tf.Variable(w_alpha * tf.random_normal([7*13*64, 1024]))
    b_d = tf.Variable(b_alpha * tf.random_normal([1024]))
    dense = tf.reshape(conv3, [-1, w_d.get_shape().as_list()[0]])


    dense = tf.nn.relu(tf.add(tf.matmul(dense, w_d), b_d))
    dense = tf.nn.dropout(dense, keep_prob)




    w_out = tf.Variable(w_alpha * tf.random_normal([1024, MAX_CAPTCHA * CHAR_SET_LEN]))
    b_out = tf.Variable(b_alpha * tf.random_normal([MAX_CAPTCHA * CHAR_SET_LEN]))
    out = tf.add(tf.matmul(dense, w_out), b_out)
    print(out.shape)
    # out = tf.nn.softmax(out)
    return out


# 训练
def train_crack_captcha_cnn():
    import time
    start_time=time.time()
    output = crack_captcha_cnn()
    # loss
    #loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(output, Y))
    loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=output, labels=Y))
    # 最后一层用来分类的softmax和sigmoid有什么不同？
    # optimizer 为了加快训练 learning_rate应该开始大，然后慢慢衰
    optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

    predict = tf.reshape(output, [-1, MAX_CAPTCHA, CHAR_SET_LEN])
    max_idx_p = tf.argmax(predict, 2)
    max_idx_l = tf.argmax(tf.reshape(Y, [-1, MAX_CAPTCHA, CHAR_SET_LEN]), 2)
    correct_pred = tf.equal(max_idx_p, max_idx_l)
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        step = 0
        while True:
            batch_x, batch_y = get_batch()

            _, loss_ = sess.run([optimizer, loss], feed_dict={X: batch_x, Y: batch_y, keep_prob: 0.75})
            #print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),step, loss_)

            # 每100 step计算一次准确率
            if step % 100 == 0:
                batch_x_test, batch_y_test = get_batch(data_path = captcha_path, is_training = True,batch=100)
                acc = sess.run(accuracy, feed_dict={X: batch_x_test, Y: batch_y_test, keep_prob: 1.})
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), step, loss_)
                print(u'***************************************************************第%s次的准确率为%s'%(step, acc))
                # 如果准确率大于50%,保存模型,完成训练
                if acc > 0.001:                  ##我这里设了0.9，设得越大训练要花的时间越长，如果设得过于接近1，很难达到。如果使用cpu，花的时间很长，cpu占用很高电脑发烫。
                    saver.save(sess, model_path, global_step=step)
                    print(time.time()-start_time)
                    break

            step += 1



if __name__ == '__main__':
    train_crack_captcha_cnn()