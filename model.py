import keras.models as models
import keras.layers as layers
import keras.utils as utils
import keras.optimizers as optimizers
import numpy as np
import tensorflow as tf
from os.path import exists

from keras.callbacks import ModelCheckpoint
import keras.callbacks as callbacks

import data_gen
CHECKPOINT_PATH = "/model_checkpoint"
FENS_PATH = "data/fens.txt"
SCORES_PATH = "data/scores.txt"


def build_model(conv_size, conv_depth):
    board_matrix = layers.Input(shape=(14, 8, 8))

    x = board_matrix
    for _ in range(conv_depth):
        x = layers.Conv2D(filters=conv_size, kernel_size=3, padding="same", activation="relu")(x)
    x = layers.Flatten()(x)
    x = layers.Dense(64, "relu")(x)
    x = layers.Dense(1, "sigmoid")(x)

    return models.Model(inputs=board_matrix, outputs=x)


x_train, y_train = data_gen.generate_data(1024)

model = build_model(32, 4)

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.1), loss="mean_squared_logarithmic_error")
model.summary()
checkpoint_callback = ModelCheckpoint(filepath=CHECKPOINT_PATH, save_best_only=True)

model.fit(x_train, y_train,
          batch_size=1, epochs=30,
          verbose=1, validation_split=0.1,
          callbacks=[callbacks.ReduceLROnPlateau(monitor="loss", patience=10),
                     callbacks.EarlyStopping(monitor="loss", patience=15, min_delta=1e-4),
                     checkpoint_callback]
          )

board = data_gen.random_board()
print(board)
board = data_gen.to_matrix(board)
board = np.expand_dims(board, 0)
print(model(board)[0][0])
