import tensorflow as tf
from tensorflow.keras.layers import Layer, Dense, Conv2D
from tensorflow.keras.saving import register_keras_serializable


@register_keras_serializable(package="Custom")
class CBAM(Layer):
    """
    Convolutional Block Attention Module (CBAM)

    Reference: "CBAM: Convolutional Block Attention Module"
    (Woo et al., ECCV 2018) - https://arxiv.org/abs/1807.06521

    The CBAM block applies both Channel Attention and Spatial Attention
    to refine feature maps adaptively. It consists of two sequential sub-blocks:

    1. Channel Attention Module (CAM):
       - Uses both global average and max pooling operations to generate channel descriptors.
       - Passes them through a shared MLP to produce channel-wise weights.
       - The output is a channel attention map that emphasizes meaningful channels.

    2. Spatial Attention Module (SAM):
       - Uses average and max pooling along the channel dimension to produce spatial descriptors.
       - Applies a convolution (often 7x7) to produce a spatial attention map.
       - This map emphasizes "where" to focus within each channel.

    Parameters
    ----------
    reduction_ratio : int, optional (default=16)
        Reduction ratio for the internal MLP in the channel attention module.

    spatial_kernel_size : int, optional (default=7)
        The kernel size for the spatial attention convolution.
    """

    def __init__(self, reduction_ratio=16, spatial_kernel_size=7, name=None, **kwargs):
        super(CBAM, self).__init__(name=name, **kwargs)
        self.reduction_ratio = reduction_ratio
        self.spatial_kernel_size = spatial_kernel_size

    def build(self, input_shape):
        if len(input_shape) != 4:
            raise ValueError(
                "CBAM input must be in the shape: (batch, height, width, channels)"
            )

        channels = input_shape[-1]
        reduced_channels = max(channels // self.reduction_ratio, 1)

        # Shared MLP for channel attention
        # Two Dense layers: C -> C//r -> C
        self.mlp_dense_1 = Dense(
            units=reduced_channels,
            activation="relu",
            use_bias=True,
            name="channel_mlp_1",
        )
        self.mlp_dense_2 = Dense(units=channels, use_bias=True, name="channel_mlp_2")

        # No weights needed to pre-build for the spatial attention layer
        # since we'll use a Conv2D layer directly on the fly.
        self.spatial_conv = Conv2D(
            filters=1,
            kernel_size=self.spatial_kernel_size,
            strides=1,
            padding="same",
            activation="sigmoid",
            use_bias=False,
            name="spatial_conv",
        )

        super(CBAM, self).build(input_shape)

    def call(self, inputs, training=False):
        # ----- Channel Attention -----
        # Global average pooling
        avg_pool = tf.reduce_mean(inputs, axis=[1, 2], keepdims=False)  # (batch, C)
        # Global max pooling
        max_pool = tf.reduce_max(inputs, axis=[1, 2], keepdims=False)  # (batch, C)

        # Shared MLP transforms
        avg_out = self.mlp_dense_2(
            self.mlp_dense_1(avg_pool, training=training), training=training
        )
        max_out = self.mlp_dense_2(
            self.mlp_dense_1(max_pool, training=training), training=training
        )

        # Combine and apply sigmoid
        channel_attention = tf.nn.sigmoid(avg_out + max_out)  # (batch, C)

        # Reshape to broadcast
        channel_attention = tf.reshape(
            channel_attention, [-1, 1, 1, tf.shape(inputs)[-1]]
        )
        channel_refined = inputs * channel_attention

        # ----- Spatial Attention -----
        # Avg and max along channel axis
        avg_spatial = tf.reduce_mean(
            channel_refined, axis=-1, keepdims=True
        )  # (batch, H, W, 1)
        max_spatial = tf.reduce_max(
            channel_refined, axis=-1, keepdims=True
        )  # (batch, H, W, 1)

        # Concatenate along channel axis
        spatial_concat = tf.concat(
            [avg_spatial, max_spatial], axis=-1
        )  # (batch, H, W, 2)

        # Apply spatial conv
        spatial_attention = self.spatial_conv(
            spatial_concat, training=training
        )  # (batch, H, W, 1)

        # Refine features spatially
        refined_outputs = channel_refined * spatial_attention
        return refined_outputs

    def compute_output_shape(self, input_shape):
        return input_shape

    def get_config(self):
        config = super(CBAM, self).get_config()
        config.update(
            {
                "reduction_ratio": self.reduction_ratio,
                "spatial_kernel_size": self.spatial_kernel_size,
            }
        )
        return config
