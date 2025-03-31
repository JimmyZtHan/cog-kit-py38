import pytest
import torch
from cogkit.finetune.utils import MeanFilter


def test_mean_filter_basic():
    mean_filter = MeanFilter(kernel_size=2)

    x = torch.tensor(
        [
            [
                [1.0, 2.0, 3.0, 4.0],
                [5.0, 6.0, 7.0, 8.0],
                [9.0, 10.0, 11.0, 12.0],
                [13.0, 14.0, 15.0, 16.0],
            ]
        ],
        dtype=torch.float32,
    )

    output = mean_filter(x)

    expected = torch.tensor([[[3.5, 5.5], [11.5, 13.5]]], dtype=torch.float32)

    assert output.shape == (1, 2, 2), f"Expected shape (1, 2, 2), but got {output.shape}"
    assert torch.allclose(output, expected), f"Expected {expected}, but got {output}"


def test_mean_filter_batch():
    mean_filter = MeanFilter(kernel_size=2)

    x = torch.tensor(
        [
            [
                [1.0, 2.0, 3.0, 4.0],
                [5.0, 6.0, 7.0, 8.0],
                [9.0, 10.0, 11.0, 12.0],
                [13.0, 14.0, 15.0, 16.0],
            ],
            [
                [2.0, 4.0, 6.0, 8.0],
                [10.0, 12.0, 14.0, 16.0],
                [18.0, 20.0, 22.0, 24.0],
                [26.0, 28.0, 30.0, 32.0],
            ],
        ],
        dtype=torch.float32,
    )

    output = mean_filter(x)

    expected = torch.tensor(
        [[[3.5, 5.5], [11.5, 13.5]], [[7.0, 11.0], [23.0, 27.0]]], dtype=torch.float32
    )

    assert output.shape == (2, 2, 2), f"Expected shape (2, 2, 2), but got {output.shape}"
    assert torch.allclose(output, expected), f"Expected {expected}, but got {output}"


def test_mean_filter_invalid_size():
    mean_filter = MeanFilter(kernel_size=2)

    x = torch.ones((1, 3, 4), dtype=torch.float32)

    with pytest.raises(ValueError) as exc_info:
        mean_filter(x)
    assert "must be divisible by kernel_size=2" in str(exc_info.value)

    x = torch.ones((1, 4, 3), dtype=torch.float32)

    with pytest.raises(ValueError) as exc_info:
        mean_filter(x)
    assert "must be divisible by kernel_size=2" in str(exc_info.value)


def test_mean_filter_larger_kernel():
    mean_filter = MeanFilter(kernel_size=4)

    x = torch.arange(64, dtype=torch.float32).reshape(1, 8, 8)

    output = mean_filter(x)

    assert output.shape == (1, 2, 2), f"Expected shape (1, 2, 2), but got {output.shape}"

    expected = torch.tensor([[[13.5, 17.5], [45.5, 49.5]]], dtype=torch.float32)
    assert torch.allclose(output, expected), f"Expected {expected}, but got {output}"


def test_mean_filter_weight_initialization():
    kernel_size = 3
    mean_filter = MeanFilter(kernel_size=kernel_size)

    assert mean_filter.weight.shape == (1, 1, kernel_size, kernel_size)

    expected_value = 1.0
    assert torch.allclose(
        mean_filter.weight, torch.full((1, 1, kernel_size, kernel_size), expected_value)
    )

    assert not mean_filter.weight.requires_grad, "Weight should not be trainable"
