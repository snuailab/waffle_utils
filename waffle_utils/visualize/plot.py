from typing import Union

import numpy as np
from matplotlib import pyplot as plt

# random 1000 colors with large variance to distinguish between continuous categories
colors = np.random.rand(1000, 3)


def _plot_scatter_1d(
    datas: np.ndarray, categories: np.ndarray, num_category: int, ax: plt.Axes
) -> plt.Axes:
    for i in range(num_category):
        idx = categories == i
        ax.scatter(
            datas[idx],
            np.zeros_like(datas[idx]),
            color=colors[i],
        )
    return ax


def _plot_scatter_2d(
    datas: np.ndarray, categories: np.ndarray, num_category: int, ax: plt.Axes
) -> plt.Axes:
    for i in range(num_category):
        idx = categories == i
        ax.scatter(
            datas[idx, 0],
            datas[idx, 1],
            color=colors[i],
        )
    return ax


def _plot_scatter_3d(
    datas: np.ndarray, categories: np.ndarray, num_category: int, ax: plt.Axes
) -> plt.Axes:
    x = datas[:, 0]
    y = datas[:, 1]
    z = datas[:, 2]
    for i in range(num_category):
        idx = categories == i
        ax.scatter(
            x[idx],
            y[idx],
            z[idx],
            color=colors[i],
        )
    return ax


def _plot_bar(datas: np.ndarray, ax: plt.Axes) -> plt.Axes:
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


def _plot_line(datas: np.ndarray, ax: plt.Axes) -> plt.Axes:
    # plot datas
    # datas shape [n, num_categories]
    # categories shape [n]
    number_of_x = datas.shape[0]

    for i in range(datas.shape[1]):
        ax.plot(np.arange(number_of_x), datas[:, i], color=colors[i])

    return ax


def plot(
    datas: Union[list[np.ndarray], np.ndarray],
    categories: Union[list[np.ndarray], np.ndarray, list] = None,
    names: list[str] = None,
    xlabel: str = None,
    xticks: list[str] = None,
    ylabel: str = None,
    yticks: list[str] = None,
    rotation: int = 0,
    title: str = None,
    ax: plt.Axes = None,
    plot_type: str = "bar",
) -> plt.Axes:
    """
    Plot bar chart

    Args:
        datas (Union[list[np.ndarray], np.ndarray]): datas to plot. shape [n, num_categories].
        categories (Union[list[np.ndarray], np.ndarray], optional): Categories. shape [n_samples]. Defaults to None.
        names (list[str], optional): Names of categories. shape [num_categories]. Defaults to None.
        xlabel (str, optional): X label. Defaults to None.
        xticks (list[str], optional): X ticks. Defaults to None.
        ylabel (str, optional): Y label. Defaults to None.
        yticks (list[str], optional): Y ticks. Defaults to None.
        rotation (int, optional): X ticks rotation. Defaults to 0.
        title (str, optional): Title. Defaults to None.
        ax (plt.Axes, optional): Axes. Defaults to None.
        plot_type (str, optional): Plot type. Defaults to "bar".

    Returns:
        plt.Axes: Axes

    """

    if isinstance(datas, list):
        datas = np.array(datas)

    if len(datas.shape) == 1:
        datas = datas.reshape(-1, 1)

    if len(datas.shape) != 2:
        raise ValueError("datas must be 2D array")

    # default settings
    if plot_type in ["bar", "line"]:
        num_samples = datas.shape[0]
        num_categories = datas.shape[1]
        if xticks is None:
            xticks = [str(i) for i in range(num_samples)]
    elif plot_type == "scatter":
        num_samples = datas.shape[0]
        num_dimensions = datas.shape[1]
        if names is None:
            names = [str(i) for i in range(max(categories) + 1)]

    if categories is None:
        categories = np.zeros(num_samples, dtype=int)
    else:
        categories = np.array(categories)

    # handle errors
    if len(categories.shape) != 1:
        raise ValueError("categories must be 1D array")
    if len(categories) != num_samples:
        raise ValueError(
            "Number of categories must be equal to number of samples.\n"
            f"Number of categories: {len(categories)}\tNumber of samples: {num_samples}"
        )

    if plot_type in ["bar", "line"]:

        if xticks is not None and len(xticks) != num_samples:
            raise ValueError(
                "Number of xticks must be equal to number of samples.\n"
                f"Number of xticks: {len(xticks)}\tNumber of samples: {num_samples}"
            )

        if names is not None and len(names) != num_categories:
            raise ValueError(
                "Number of names must be equal to number of categories.\n"
                f"Number of names: {len(names)}\tNumber of categories: {num_categories}"
            )

    # draw
    if plot_type == "bar":
        if ax is None:
            ax = plt.axes()
        ax = _plot_bar(datas, ax)
    elif plot_type == "line":
        if ax is None:
            ax = plt.axes()
        ax = _plot_line(datas, ax)
    elif plot_type == "scatter":
        if ax is None:
            ax = plt.axes(projection="3d" if num_dimensions == 3 else None)
        if datas.shape[1] == 1:
            ax = _plot_scatter_1d(datas, categories, len(names), ax)
        elif datas.shape[1] == 2:
            ax = _plot_scatter_2d(datas, categories, len(names), ax)
        elif datas.shape[1] == 3:
            ax = _plot_scatter_3d(datas, categories, len(names), ax)
        else:
            raise NotImplementedError(
                f"datas shape {datas.shape} is not supported"
            )
    else:
        raise ValueError(
            f"plot_type must be bar or line. plot_type: {plot_type}"
        )

    if names is not None:
        ax.legend(names)

    if title is not None:
        ax.set_title(title)

    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if xticks is not None:
        ax.set_xticks(np.arange(len(xticks)))
        ax.set_xticklabels(xticks, rotation=rotation)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if yticks is not None:
        ax.set_yticks(np.arange(len(yticks)))
        ax.set_yticklabels(yticks)

    return ax


def plot_bar(
    datas: Union[list[np.ndarray], np.ndarray],
    categories: Union[list[np.ndarray], np.ndarray] = None,
    names: list[str] = None,
    xlabel: str = None,
    xticks: list[str] = None,
    ylabel: str = None,
    yticks: list[str] = None,
    rotation: int = 0,
    title: str = None,
    ax: plt.Axes = None,
) -> plt.Axes:
    """
    Plot bar chart

    Args:
        datas (Union[list[np.ndarray], np.ndarray]): datas to plot. shape [n, num_categories].
        categories (Union[list[np.ndarray], np.ndarray], optional): Categories. shape [n_samples]. Defaults to None.
        names (list[str], optional): Names of categories. shape [num_categories]. Defaults to None.
        xlabel (str, optional): X label. Defaults to None.
        xticks (list[str], optional): X ticks. Defaults to None.
        ylabel (str, optional): Y label. Defaults to None.
        yticks (list[str], optional): Y ticks. Defaults to None.
        rotation (int, optional): X ticks rotation. Defaults to 0.
        title (str, optional): Title. Defaults to None.
        ax (plt.Axes, optional): Axes. Defaults to None.

    Returns:
        plt.Axes: Axes

    """

    return plot(
        datas,
        categories,
        names,
        xlabel,
        xticks,
        ylabel,
        yticks,
        rotation,
        title,
        ax,
        plot_type="bar",
    )


def plot_line(
    datas: Union[list[np.ndarray], np.ndarray],
    categories: Union[list[np.ndarray], np.ndarray] = None,
    names: list[str] = None,
    xlabel: str = None,
    xticks: list[str] = None,
    ylabel: str = None,
    yticks: list[str] = None,
    rotation: int = 0,
    title: str = None,
    ax: plt.Axes = None,
) -> plt.Axes:
    """
    Plot line chart

    Args:
        datas (Union[list[np.ndarray], np.ndarray]): datas to plot. shape [n, num_categories].
        categories (Union[list[np.ndarray], np.ndarray], optional): Categories. shape [n_samples]. Defaults to None.
        names (list[str], optional): Names of categories. shape [num_categories]. Defaults to None.
        xlabel (str, optional): X label. Defaults to None.
        xticks (list[str], optional): X ticks. Defaults to None.
        ylabel (str, optional): Y label. Defaults to None.
        yticks (list[str], optional): Y ticks. Defaults to None.
        rotation (int, optional): X ticks rotation. Defaults to 0.
        title (str, optional): Title. Defaults to None.
        ax (plt.Axes, optional): Axes. Defaults to None.

    Returns:
        plt.Axes: Axes

    """

    return plot(
        datas=datas,
        categories=categories,
        names=names,
        xlabel=xlabel,
        xticks=xticks,
        ylabel=ylabel,
        yticks=yticks,
        rotation=rotation,
        title=title,
        ax=ax,
        plot_type="line",
    )


def plot_scatter(
    datas: Union[list[np.ndarray], np.ndarray],
    categories: Union[list[np.ndarray], np.ndarray] = None,
    names: list[str] = None,
    xlabel: str = None,
    ylabel: str = None,
    title: str = None,
    ax: plt.Axes = None,
) -> plt.Axes:
    """
    Plot scatter chart

    Args:
        datas (Union[list[np.ndarray], np.ndarray]): datas to plot. shape [n, num_categories].
        categories (Union[list[np.ndarray], np.ndarray], optional): Categories. shape [n_samples]. Defaults to None.
        names (list[str], optional): Names of categories. shape [num_categories]. Defaults to None.
        xlabel (str, optional): X label. Defaults to None.
        ylabel (str, optional): Y label. Defaults to None.
        title (str, optional): Title. Defaults to None.
        ax (plt.Axes, optional): Axes. Defaults to None.

    Returns:
        plt.Axes: Axes

    """

    return plot(
        datas=datas,
        categories=categories,
        names=names,
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
        ax=ax,
        plot_type="scatter",
    )
