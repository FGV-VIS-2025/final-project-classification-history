import tensorflow as tf
from tensorflow.keras.models import Sequential
# Importar Activation explicitamente
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Activation # Adicionado Activation
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import numpy as np
import os

print(f"TensorFlow version: {tf.__version__}")

# --- Configuration ---
MODEL_FILENAME = 'mnist_cnn_tinyvgg_like.h5' # Novo nome para o modelo menor
EPOCHS = 10 # Number of epochs to train for (can reduce for quicker testing)
BATCH_SIZE = 32

# --- 1. Load and Preprocess MNIST Data ---
print("Loading MNIST dataset...")
(x_train, y_train), (x_test, y_test) = mnist.load_data()

print("Preprocessing data...")
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

num_classes = 10
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)

print(f"x_train shape: {x_train.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"x_test shape: {x_test.shape}")
print(f"y_test shape: {y_test.shape}")

# --- 2. Define the NEW TinyVGG-like CNN Model ---
print("Defining the new TinyVGG-like CNN model for MNIST...")
filters_block1 = 10
filters_block2 = 20 # Você pode ajustar estes valores se desejar

model = Sequential([
    # Bloco Convolucional 1
    Conv2D(filters_block1, kernel_size=(3, 3), padding='valid', name='conv_1_1', input_shape=(28, 28, 1)), # Saída: 26x26x10
    Activation('relu', name='relu_1_1'),
    Conv2D(filters_block1, kernel_size=(3, 3), padding='valid', name='conv_1_2'), # Entrada: 26x26x10, Saída: 24x24x10
    Activation('relu', name='relu_1_2'),
    MaxPooling2D(pool_size=(2, 2), name='max_pool_1'), # Entrada: 24x24x10, Saída: 12x12x10

    # Bloco Convolucional 2
    Conv2D(filters_block2, kernel_size=(3, 3), padding='valid', name='conv_2_1'), # Entrada: 12x12x10, Saída: 10x10x20
    Activation('relu', name='relu_2_1'),
    Conv2D(filters_block2, kernel_size=(3, 3), padding='valid', name='conv_2_2'), # Entrada: 10x10x20, Saída: 8x8x20
    Activation('relu', name='relu_2_2'),
    MaxPooling2D(pool_size=(2, 2), name='max_pool_2'), # Entrada: 8x8x20, Saída: 4x4x20

    # Camadas Finais
    Flatten(name='flatten'), # Entrada: 4x4x20, Saída: 320
    # A camada Dropout foi removida para simplificar e reduzir ainda mais, mas pode ser adicionada se necessário.
    # Se desejar manter uma camada densa intermediária como no seu modelo original (mas menor):
    # Dense(64, name='dense_1'), # Exemplo de camada densa menor
    # Activation('relu', name='relu_dense_1'),
    # Dropout(0.5, name='dropout_1'),
    Dense(num_classes, activation='softmax', name='output') # Entrada: 320, Saída: 10
])

# --- 3. Compile the Model ---
print("Compiling the model...")
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.summary() # Print model architecture

# --- 4. Train the Model ---
print(f"Training the model for {EPOCHS} epochs...")
history = model.fit(x_train, y_train,
                    batch_size=BATCH_SIZE,
                    epochs=EPOCHS,
                    validation_split=0.1)

# --- 5. Evaluate the Model ---
print("Evaluating the model on the test set...")
score = model.evaluate(x_test, y_test, verbose=0)
print(f"Test loss: {score[0]:.4f}")
print(f"Test accuracy: {score[1]:.4f}")

# --- 6. Save the Model ---
model.save(MODEL_FILENAME)
print(f"Model saved as {os.path.join(os.getcwd(), MODEL_FILENAME)}")
print("-----------------------------------------------------------------")
print("MNIST CNN (TinyVGG-like) training complete.")
print(f"To convert this model to TensorFlow.js format, run the following command")
print(f"from this directory ({os.getcwd()}):")
# Ajuste o nome do arquivo do modelo e o diretório de saída do tfjs conforme necessário
print(f"  tensorflowjs_converter --input_format keras {MODEL_FILENAME} ../public/mnist_model_tfjs_tiny")
print("-----------------------------------------------------------------")

if __name__ == "__main__":
    pass