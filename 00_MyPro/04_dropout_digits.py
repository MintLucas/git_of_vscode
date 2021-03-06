import tensorflow as tf
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

# load data
digits = load_digits()
X = digits.data
y = digits.target
y = LabelBinarizer().fit_transform(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)

def add_layer(inputs,in_size,out_size,activation_function=None):
    Weights = tf.Variable(tf.random_normal([in_size,out_size]))
    biases = tf.Variable(tf.zeros([1,out_size])+0.1)
    Wx_plus_b = tf.matmul(inputs,Weights) + biases
    Wx_plus_b = tf.nn.dropout(Wx_plus_b,keep_prob)#keep_prob这里不用设值
    if activation_function == None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs

keep_prob = tf.placeholder(tf.float32)
xs = tf.placeholder(tf.float32,[None,64])
ys = tf.placeholder(tf.float32,[None,10])

l1 = add_layer(xs,64,50,activation_function=tf.nn.tanh)
prediction = add_layer(l1,50,10,activation_function=tf.nn.softmax)

loss = tf.reduce_mean(-tf.reduce_sum(ys*tf.log(prediction),axis = 1))
tf.summary.scalar('loss',loss)
train = tf.train.GradientDescentOptimizer(0.5).minimize(loss)

sess = tf.Session()
merged = tf.summary.merge_all()
train_writer = tf.summary.FileWriter('logs/03_train',sess.graph)
test_writer = tf.summary.FileWriter('logs/03_test',sess.graph)
sess.run(tf.global_variables_initializer())

for step in range(0,1001):
    sess.run(train,feed_dict={xs: X_train, ys: y_train, keep_prob: 1})
    if step%20 == 0:
        train_result = sess.run(merged, feed_dict={xs: X_train, ys: y_train, keep_prob: 1})
        test_result = sess.run(merged, feed_dict={xs: X_test, ys: y_test, keep_prob: 1})
        train_writer.add_summary(train_result, step)
        test_writer.add_summary(test_result, step)
