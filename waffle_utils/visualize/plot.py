from typing import Union

import numpy as np
from matplotlib import pyplot as plt

# random 1000 colors with large variance to distinguish between continuous categories
colors = np.random.rand(1000, 3)


def _plot_1d_scatter(
    datas: np.ndarray, categories: np.ndarray, labels: list[str], ax: plt.Axes
) -> plt.Axes:
    for i in range(len(np.unique(categories))):
        ax.scatter(
            datas[categories == i],
            np.zeros_like(datas[categories == i]),
            color=colors[i],
            label=labels[i],
        )
    return ax


def _plot_2d_scatter(
    datas: np.ndarray, categories: np.ndarray, labels: list[str], ax: plt.Axes
) -> plt.Axes:
    for i in range(len(np.unique(categories))):
        ax.scatter(
            datas[categories == i, 0],
            datas[categories == i, 1],
            color=colors[i],
            label=labels[i],
        )
    return ax


def _plot_3d_scatter(
    datas: np.ndarray, categories: np.ndarray, labels: list[str], ax: plt.Axes
) -> plt.Axes:
    x = datas[:, 0]
    y = datas[:, 1]
    z = datas[:, 2]
    for i in range(len(np.unique(categories))):
        ax.scatter(
            x[categories == i],
            y[categories == i],
            z[categories == i],
            color=colors[i],
            label=labels[i],
        )
    return ax


def plot_scatter(
    datas: Union[list[np.ndarray], np.ndarray],
    categories: Union[list[np.ndarray], np.ndarray] = None,
    names: list[str] = None,
    title: str = None,
    ax: plt.Axes = None,
) -> plt.Axes:
    """
    Plot 1D, 2D or 3D scatter

    Args:
        datas (Union[list[np.ndarray], np.ndarray]): 1D, 2D or 3D data to scatter. shape [n_samples, n_dimensions].
        categories (Union[list[np.ndarray], np.ndarray], optional): Categories. shape [n_samples]. Defaults to None.
        names (list[str], optional): Names of categories. shape [num_categories]. Defaults to None.
        title (str, optional): Title. Defaults to None.
        ax (plt.Axes, optional): Axes. Defaults to None.

    Returns:
        plt.Axes: Axes

    """

    if isinstance(datas, list):
        datas = np.array(datas)
    if len(datas.shape) != 2:
        raise ValueError("datas must be 2D array")

    if isinstance(categories, list):
        categories = np.array(categories)
    elif categories is None:
        categories = np.zeros(len(datas), dtype=int)
    if len(categories.shape) != 1:
        raise ValueError("categories must be 1D array")

    if names is not None:
        if len(names) != len(np.unique(categories)):
            raise ValueError(
                "Number of names must be equal to number of categories.\n"
                f"Number of names: {len(names)}\tNumber of categories: {len(np.unique(categories))}"
            )

    dimensions = datas.shape[1]

    if ax is None:
        ax = plt.axes(projection="3d" if dimensions == 3 else None)

    # map category indexes to name
    if names is not None:
        # categories to labels
        labels = [names[i] for i in categories]
    else:
        labels = [str(i) for i in categories]

    if dimensions == 1:
        ax = _plot_1d_scatter(datas, categories, labels, ax)
    elif dimensions == 2:
        ax = _plot_2d_scatter(datas, categories, labels, ax)
    elif dimensions == 3:
        ax = _plot_3d_scatter(datas, categories, labels, ax)
    else:
        raise ValueError("Datas dimension must be 1 or 2 or 3")

    ax.legend()

    if title is not None:
        ax.set_title(title)

    return ax


def _plot_bar(
    datas: np.ndarray, categories: np.ndarray, ax: plt.Axes
) -> plt.Axes:
    # plot datas
    # datas shape [n, num_categories]
    # categories shape [n]
    num_samples = datas.shape[0]
    num_categories = datas.shape[1]

    # location of bar groups within each index of x should be centered with padding
    padding = 0.1
    width = (1 - padding) / num_categories
    x = np.arange(num_samples) - (1 - padding) / 2 + width / 2

    for i in range(num_categories):
        ax.bar(x + i * width, datas[:, i], width=width, color=colors[i])

    return ax


def plot_bar(
    datas: Union[list[np.ndarray], np.ndarray],
    categories: Union[list[np.ndarray], np.ndarray] = None,
    names: list[str] = None,
    title: str = None,
    ax: plt.Axes = None,
) -> plt.Axes:
    """
    Plot bar chart

    Args:
        datas (Union[list[np.ndarray], np.ndarray]): datas to plot. shape [n, num_categories].
        categories (Union[list[np.ndarray], np.ndarray], optional): Categories. shape [n_samples]. Defaults to None.
        names (list[str], optional): Names of categories. shape [num_categories]. Defaults to None.
        title (str, optional): Title. Defaults to None.
        ax (plt.Axes, optional): Axes. Defaults to None.

    Returns:
        plt.Axes: Axes

    """

    if isinstance(datas, list):
        datas = np.array(datas)
    if len(datas.shape) != 2:
        raise ValueError("datas must be 2D array")

    num_samples = datas.shape[0]
    num_categories = datas.shape[1]

    if isinstance(categories, list):
        categories = np.array(categories)
    elif categories is None:
        categories = np.zeros(num_categories, dtype=int)

    if len(categories.shape) != 1:
        raise ValueError("categories must be 1D array")
    if len(categories) != num_samples:
        raise ValueError(
            "Number of categories must be equal to number of samples.\n"
            f"Number of categories: {len(categories)}\tNumber of samples: {num_samples}"
        )

    if names is not None:
        if len(names) != num_categories:
            raise ValueError(
                "Number of names must be equal to number of categories.\n"
                f"Number of names: {len(names)}\tNumber of categories: {num_categories}"
            )

    if ax is None:
        ax = plt.axes()

    ax = _plot_bar(datas, categories, ax)

    if names is not None:
        ax.legend(names)

    if title is not None:
        ax.set_title(title)

    return ax


def _plot_line(
    datas: np.ndarray, categories: np.ndarray, ax: plt.Axes
) -> plt.Axes:
    # plot datas
    # datas shape [n, num_categories]
    # categories shape [n]
    number_of_x = datas.shape[0]

    for i in range(datas.shape[1]):
        ax.plot(np.arange(number_of_x), datas[:, i], color=colors[i])

    return ax


def plot_line(
    datas: Union[list[np.ndarray], np.ndarray],
    categories: Union[list[np.ndarray], np.ndarray] = None,
    names: list[str] = None,
    title: str = None,
    ax: plt.Axes = None,
) -> plt.Axes:
    """
    Plot line chart

    Args:
        datas (Union[list[np.ndarray], np.ndarray]): datas to plot. shape [n, num_categories].
        categories (Union[list[np.ndarray], np.ndarray], optional): Categories. shape [n_samples]. Defaults to None.
        names (list[str], optional): Names of categories. shape [num_categories]. Defaults to None.
        title (str, optional): Title. Defaults to None.
        ax (plt.Axes, optional): Axes. Defaults to None.

    Returns:
        plt.Axes: Axes

    """

    if isinstance(datas, list):
        datas = np.array(datas)
    if len(datas.shape) != 2:
        raise ValueError("datas must be 2D array")

    num_samples = datas.shape[0]
    num_categories = datas.shape[1]

    if isinstance(categories, list):
        categories = np.array(categories)
    elif categories is None:
        categories = np.zeros(num_categories, dtype=int)

    if len(categories.shape) != 1:
        raise ValueError("categories must be 1D array")
    if len(categories) != num_samples:
        raise ValueError(
            "Number of categories must be equal to number of samples.\n"
            f"Number of categories: {len(categories)}\tNumber of samples: {num_samples}"
        )

    if names is not None:
        if len(names) != num_categories:
            raise ValueError(
                "Number of names must be equal to number of categories.\n"
                f"Number of names: {len(names)}\tNumber of categories: {num_categories}"
            )

    if ax is None:
        ax = plt.axes()

    ax = _plot_line(datas, categories, ax)

    if names is not None:
        ax.legend(names)

    if title is not None:
        ax.set_title(title)

    return ax
