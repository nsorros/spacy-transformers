# Stubs for torch.optim.sgd (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from .optimizer import Optimizer, required
from typing import Any, Optional

class SGD(Optimizer):
    def __init__(self, params: Any, lr: Any = ..., momentum: int = ..., dampening: int = ..., weight_decay: int = ..., nesterov: bool = ...) -> None: ...
    def step(self, closure: Optional[Any] = ...): ...