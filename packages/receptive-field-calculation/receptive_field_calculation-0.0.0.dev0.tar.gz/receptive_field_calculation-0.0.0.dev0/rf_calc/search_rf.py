import torch
import numpy as np
from copy import deepcopy


def search_rf(layer:callable, input_shape:tuple, rf_range:np.ndarray=None, log:bool=False):
    """search rf.

    Args:
        layer (callable): torch.nn.Module
        input_shape (tuple): [C, T], make sure T is much larger than rf.
        rf_range (np.ndarray): possible range for rf, make sure the rf lies in the range
    """
    input = torch.rand(input_shape).numpy()
    output = layer(torch.tensor(input)).detach().numpy()
    start = 7 # magic number
    _input = deepcopy(input)
    _input[:, :start] = -1
    if rf_range is None:
        rf_range = np.arange(1, input_shape[1])
    for i in rf_range:
        if i == 0:
            continue
        _input = deepcopy(input)
        _input[:, :start] = -1
        _input[:, start + i:] = -1
        _output = layer(torch.tensor(_input)).detach().numpy()
        unchanged = np.where((output == _output).mean(0) == 1)[0]
        if len(unchanged) > 0:
            if log:
                print(f"[{start}:{start+i}] => [{unchanged[0]}:{unchanged[-1]+1}] => RF: {i}")
            return i
    print("Can not find rf!")


