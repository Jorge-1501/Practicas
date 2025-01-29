# Librerías 
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import RMSprop, Adam
from tensorflow.keras.callbacks import ModelCheckpoint

# Cargamos el conjunto de datos MNIST
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Redimesionamiento y normalización de las imágenes
train_images = train_images.reshape((60000, 28 * 28)) # 28*28 = 784
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype('float32') / 255

# Conversión one-hot 
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# Creación del modelo [784, 24, 10]
model = models.Sequential()
model.add(layers.Dense(784, activation='relu', input_shape=(28 * 28,)))
model.add(layers.Dense(24, activation='relu', input_shape=(28 * 28,)))
model.add(layers.Dense(10, activation='softmax'))

# Compilar el modelo
custom_optimizer = Adam(learning_rate=0.00001, beta_1=0.95, beta_2=0.999, epsilon=1e-10)

model.compile(optimizer = custom_optimizer,
              loss = 'categorical_crossentropy',
              metrics = ['accuracy'])

# Entrenar el modelo
checkpoint_mejor_modelo = ModelCheckpoint("Modelo2.keras", monitor="val_loss", save_best_only=True)

history = model.fit(train_images, train_labels, 
                    epochs=30, 
                    callbacks=[checkpoint_mejor_modelo],
                    batch_size=10, validation_split=0.2)

# Evaluación el modelo en el conjunto de prueba
test_loss, test_acc = model.evaluate(test_images, test_labels)
print('Precisión en el conjunto de prueba:', test_acc)

history_dict = history.history
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']

# Gráfica 
fig = plt.figure(figsize=(10,10))

epoch = range(1,len(loss_values)+1)

plt.plot(epoch,loss_values, 'o',label='training')
plt.plot(epoch,val_loss_values, '--',label='val')

# Ejes
plt.ylabel("Pérdida", fontsize = 16)
plt.xlabel("Épocas", fontsize = 16)
plt.title("Pérdida en training y val", fontsize = 40)

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.legend(fontsize= 10)
plt.grid(True)
plt.savefig("Modelo2.png")
plt.show