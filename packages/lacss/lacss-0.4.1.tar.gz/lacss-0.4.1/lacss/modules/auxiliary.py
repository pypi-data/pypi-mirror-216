import typing as tp

import flax.linen as nn
import jax
import jax.numpy as jnp

from .common import *
from .unet import UNet


class AuxInstanceEdge(nn.Module):
    conv_spec: tp.Sequence[int] = (24, 64, 64)
    n_groups: int = 1
    # share_weights: bool = False

    @nn.compact
    def __call__(
        self, x: jnp.ndarray, *, category: tp.Optional[jnp.ndarray] = None
    ) -> jnp.ndarray:
        for n in self.conv_spec:
            x = nn.Conv(n, (3, 3), use_bias=False)(x)
            x = nn.GroupNorm(num_groups=None, group_size=1, use_scale=False)(
                x[None, ...]
            )[0]
            x = jax.nn.relu(x)

        x = nn.Conv(self.n_groups, (3, 3))(x)
        c = category.astype(int).squeeze() if category is not None else 0
        x = x[..., c]

        # x = jax.nn.sigmoid(x)

        return dict(
            edge_pred=x,
        )


class AuxForeground(nn.Module):
    conv_spec: tp.Sequence[int] = (24, 64)
    patch_size: tp.Sequence[int] = 1
    n_groups: int = 1
    share_weights: bool = False
    # use_attention: bool = False

    @nn.compact
    def __call__(
        self,
        x: jnp.ndarray,
        *,
        category: tp.Optional[jnp.ndarray] = None,
    ) -> jnp.ndarray:
        assert category is not None or self.n_groups == 1

        net = UNet(self.conv_spec, self.patch_size)
        _, decoder_out = net(x)

        y = decoder_out[str(net.start_level)]

        c = category.astype(int).squeeze() if category is not None else 0

        fg = nn.Conv(self.n_groups, (3, 3))(y)
        fg = fg[..., c]

        if fg.shape != x.shape[:-1]:
            fg = jax.image.resize(fg, x.shape[:-1], "linear")

        output = dict(fg_pred=fg)

        if self.share_weights:
            edge = nn.Conv(self.n_groups, (3, 3))(y)
            edge = edge[..., c]

            if edge.shape != x.shape[:-1]:
                edge = jax.image.resize(edge, x.shape[:-1], "linear")

            output.update(
                dict(
                    edge_pred=edge,
                )
            )

        return output
