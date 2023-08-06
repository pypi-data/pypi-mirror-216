import tensorflow as tf
import os

def VisionTransformer(input_shape, patch_size, num_classes, hidden_dim, num_heads, mlp_dim, channels, dropout_rate):
    weight_path = os.path.join(os.path.dirname(__file__), "..", "weight.h5")

    in_model = tf.keras.applications.DenseNet121(
        input_shape=input_shape,
        include_top=False,
        weights=weight_path,
        classes=num_classes
    )

    return in_model
