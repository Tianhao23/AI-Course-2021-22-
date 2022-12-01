import tensorflow as tf
import time
# Tianhao Chen, pd.4

a = time.time()
(x,y), (x_test, y_test) = tf.keras.datasets.mnist.load_data() #dataset of images

x, x_test = tf.keras.utils.normalize(x, axis = 1),tf.keras.utils.normalize(x_test, axis = 1) #normalizing

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)), #flattens input
  tf.keras.layers.Dense(512, activation='relu'), #densely-connected NN layer, relu = rectified linear unit activation 
  tf.keras.layers.Dense(144, activation='relu'), 
  tf.keras.layers.Dense(10, activation = 'softmax') #softmax converts vector of values to a probability distribution, output vecotr range (0,1), sum to 1
])
model.compile(optimizer = 'adam', #name of optimizer, implements Adam algorithm
                loss = "sparse_categorical_crossentropy", #loss function
                metrics = ['accuracy']) #metrics to be evaluated
model.fit(x, y, epochs = 6)

f = open('weights.txt', 'w')
loss, acc = model.evaluate(x_test, y_test)
#print(loss, acc)
weights = []
for layer in model.layers[1::]: weights.append(list(layer.get_weights()[0].flatten()))
for weight in weights:
    f.write(str(weight))
    if weights.index(weight) != 2: f.write('\n')
f.close()
model.summary()
b = time.time()-a
print(f'Time taken: {b} sec')
# Tianhao Chen, pd. 4, 2023