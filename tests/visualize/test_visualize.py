import matplotlib.pyplot as plt
import numpy as np
import pytest

from waffle_utils.visualize import plot_bar, plot_line, plot_scatter


@pytest.fixture
def embedding_1d():
    return np.random.rand(100, 1)


@pytest.fixture
def embedding_2d():
    return np.random.rand(100, 2)


@pytest.fixture
def embedding_3d():
    return np.random.rand(100, 3)


@pytest.fixture
def categories():
    return np.random.randint(0, 2, 100)


def test_plot_scatter(embedding_1d, embedding_2d, embedding_3d, categories):
    ax = plot_scatter(
        datas=embedding_1d,
        categories=categories,
        names=None,
        title=None,
        xlabel=None,
    )
    assert len(ax.get_legend().get_texts()) == categories.max() + 1

    plot_scatter(
        datas=embedding_2d,
        categories=categories,
        names=None,
        title=None,
        xlabel=None,
    )
    assert len(ax.get_legend().get_texts()) == categories.max() + 1

    plot_scatter(
        datas=embedding_3d,
        categories=categories,
        names=None,
        title=None,
        xlabel=None,
    )
    assert len(ax.get_legend().get_texts()) == categories.max() + 1


def test_plot_bar(embedding_1d, embedding_2d, embedding_3d, categories):
    plot_bar(
        datas=embedding_1d,
        categories=categories,
        names=None,
        title=None,
        xticks=None,
    )

    plot_bar(
        datas=embedding_2d,
        categories=categories,
        names=None,
        title=None,
        xticks=None,
    )

    plot_bar(
        datas=embedding_3d,
        categories=categories,
        names=None,
        title=None,
        xticks=None,
    )


def test_plot_line(embedding_1d, embedding_2d, embedding_3d, categories):
    plot_line(
        datas=embedding_1d,
        categories=categories,
        names=None,
        title=None,
        xticks=None,
    )

    plot_line(
        datas=embedding_2d,
        categories=categories,
        names=None,
        title=None,
        xticks=None,
    )

    plot_line(
        datas=embedding_3d,
        categories=categories,
        names=None,
        title=None,
        xticks=None,
    )
