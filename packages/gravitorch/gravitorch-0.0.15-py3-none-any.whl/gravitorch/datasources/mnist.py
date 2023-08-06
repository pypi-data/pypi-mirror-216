r"""This module implements a data source for MNIST dataset."""

from __future__ import annotations

__all__ = ["MnistDataSource"]

from pathlib import Path

from torch.utils.data import Dataset

from gravitorch import constants as ct
from gravitorch.creators.dataloader.base import BaseDataLoaderCreator
from gravitorch.data.datasets import MNIST
from gravitorch.data.datasets.mnist import get_default_transform
from gravitorch.datasources.dataset import DatasetDataSource
from gravitorch.utils.path import sanitize_path


class MnistDataSource(DatasetDataSource):
    r"""Implements a data source for the MNIST dataset.

    Args:
    ----
        path (str, optional): Specifies the path where to save/load
            the MNIST data.
        data_loader_creators (dict): Specifies the data loader
            creators to initialize. Each key indicates a data loader
            creator name. The value can be a ``BaseDataLoaderCreator``
            object, or its configuration, or ``None``. ``None`` means
            a default data loader will be created. Each data loader
            creator takes a ``Dataset`` object as input, so you need
            to specify a dataset with the same name. The expected
            keys are ``'train'`` and ``'eval'``.
    """

    def __init__(
        self,
        path: Path | str,
        data_loader_creators: dict[str, BaseDataLoaderCreator | dict | None],
    ) -> None:
        train_dataset, eval_dataset = create_standard_train_eval_dataset(sanitize_path(path))
        super().__init__(
            datasets={ct.TRAIN: train_dataset, ct.EVAL: eval_dataset},
            data_loader_creators=data_loader_creators,
        )


def create_standard_train_eval_dataset(path: Path) -> tuple[Dataset, Dataset]:
    r"""Creates the standard training and evaluation MNIST datasets.

    Args:
    ----
        path (``pathlib.Path``): Specifies the path where to save/load
            MNIST data.

    Returns:
    -------
        ``Dataset, Dataset``: The training (first value in the tuple)
            and evaluation (second value in the tuple) datasets.
    """
    transform = get_default_transform()
    return (
        MNIST(path.as_posix(), train=True, download=True, transform=transform),
        MNIST(path.as_posix(), train=False, download=True, transform=transform),
    )
