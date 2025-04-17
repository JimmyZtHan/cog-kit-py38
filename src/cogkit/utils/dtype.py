# -*- coding: utf-8 -*-


import torch
from typing import Union


def cast_to_torch_dtype(dtype: Union[str, torch.dtype]) -> torch.dtype:
    if isinstance(dtype, torch.dtype):
        return dtype
    
    if dtype == "bfloat16":
        return torch.bfloat16
    elif dtype == "float16":
        return torch.float16
    else:
        raise ValueError(f"Unsupported dtype: {dtype}")
