import tensorflow as tf
import os

def VisionTransformer(input_shape, patch_size, num_classes, hidden_dim, num_heads, mlp_dim, channels, dropout_rate):

    in_model = tf.keras.applications.DenseNet121(
        input_shape=input_shape,
        include_top=False,
        weights="weight.h5",
        classes=2
    )

    return in_model
