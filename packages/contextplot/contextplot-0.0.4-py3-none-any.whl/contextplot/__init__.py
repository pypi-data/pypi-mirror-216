"""Context-manager based API for making Matplotlib plots in a Jupyter notebook.

See `example.ipynb`.
"""

# pylint: disable=invalid-name

import contextlib
import dataclasses
import functools
import io
import os
import subprocess
import tempfile
import typing as t
from typing import Any

from IPython.core.interactiveshell import InteractiveShell

import IPython.display
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

_SCREEN_DPI = 115

COLORS = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
    '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
]


@dataclasses.dataclass
class _AxesWrapper:

    _ax: plt.Axes

    def __getattr__(self, name: str) -> Any:
        method = getattr(self._ax, name)

        if callable(method):

            @functools.wraps(method)
            def wrapped_method(*args, **kwargs):
                method(*args, **kwargs)

            return wrapped_method
        return method


@dataclasses.dataclass
class _ContextPlot:
    figure: plt.Figure
    axes: np.ndarray[plt.Axes]
    _active_flat_index: int = 0

    def next(self):
        """Move to the next subplot"""
        self._active_flat_index += 1

    def funcplot(self, func, x0, x1, *args, num_points=300, **kwargs):
        """Plot a function, generating an array of points automatically.
        
        (For convenience.)
        """
        x = np.linspace(x0, x1, num_points)
        y = func(x)
        self.ax.plot(x, y, *args, **kwargs)

    @property
    def ax(self):
        """Use this to access (a wrapper around) the underlying `plt.Axes` object
        
        Automatically swallows anything returned by a method. For use with 
        `InteractiveShell.ast_node_interactivity = "all"`.
        """
        return _AxesWrapper(_ax=self.axes.flat[self._active_flat_index])

    @property
    def ax_raw(self):
        """Use this to access the underlying `plt.Axes` object"""
        return self.axes.flat[self._active_flat_index]


@contextlib.contextmanager
def context_plot(*args, size_inches=None, dpi=400, **kwargs):
    """A context manager-based API for making Matplotlib plots in Jupyter notebooks"""
    figure, axes = plt.subplots(*args,
                                squeeze=False,
                                constrained_layout=True,
                                **kwargs)
    yield _ContextPlot(figure=figure, axes=axes)

    if size_inches:
        figure.set_size_inches(*size_inches)

    _display(figure, dpi=dpi)


def set_defaults():
    """Use a nice default set of MPL styles.
    
    Also set `InteractiveShell.ast_node_interactivity = "all"`, so that every
    statement in a cell yields an output other than those that return `None`.
    """
    InteractiveShell.ast_node_interactivity = "all"

    line_width = 0.7
    major_tick_size = 3
    minor_tick_size = 1.5

    mpl.rcParams['figure.figsize'] = (6, 3)
    mpl.rcParams['font.size'] = 10
    mpl.rcParams['font.family'] = 'Roboto'
    mpl.rcParams['font.weight'] = 'normal'
    mpl.rcParams['axes.labelsize'] = mpl.rcParams['font.size']
    mpl.rcParams['axes.titlesize'] = mpl.rcParams['font.size'] + 1
    mpl.rcParams['legend.fontsize'] = mpl.rcParams['font.size'] - 2
    mpl.rcParams['xtick.labelsize'] = mpl.rcParams['font.size'] - 1
    mpl.rcParams['ytick.labelsize'] = mpl.rcParams['font.size'] - 1
    mpl.rcParams['xtick.major.size'] = major_tick_size
    mpl.rcParams['xtick.minor.size'] = minor_tick_size
    mpl.rcParams['xtick.major.width'] = line_width
    mpl.rcParams['xtick.minor.width'] = line_width
    mpl.rcParams['ytick.major.size'] = major_tick_size
    mpl.rcParams['ytick.minor.size'] = minor_tick_size
    mpl.rcParams['ytick.major.width'] = line_width
    mpl.rcParams['ytick.minor.width'] = line_width
    mpl.rcParams['axes.grid'] = True
    mpl.rcParams['axes.axisbelow'] = True
    mpl.rcParams['axes.linewidth'] = line_width
    mpl.rcParams['grid.alpha'] = 0.3
    mpl.rcParams['grid.linestyle'] = '-'
    mpl.rcParams['axes.prop_cycle'] = plt.cycler('color', COLORS)
    mpl.rcParams['legend.framealpha'] = 0.75
    mpl.rcParams['legend.frameon'] = True
    mpl.rcParams['legend.loc'] = 'upper right'
    mpl.rcParams['savefig.dpi'] = 400


@dataclasses.dataclass
class _ContextVideo:
    _args: list[t.Any]
    _kwargs: dict[t.Any, t.Any]

    _size_inches: t.Tuple[float, float]

    frames: list[bytes]

    @contextlib.contextmanager
    def next_frame(self) -> t.Generator[_ContextPlot, None, None]:
        """Generate the next frame's subplots"""
        figure, axes = plt.subplots(*self._args,
                                    squeeze=False,
                                    constrained_layout=True,
                                    **self._kwargs)
        yield _ContextPlot(figure=figure, axes=axes)

        if self._size_inches:
            figure.set_size_inches(*self._size_inches)

        with io.BytesIO() as f:
            figure.savefig(f, format='png', dpi=100)
            plt.close(figure)

            self.frames.append(f.getvalue())


@contextlib.contextmanager
def context_video(
    output_path,
    *args,
    frame_rate_hz=20,
    size_inches=None,
    **kwargs,
):
    """Context manager-based API for generating videos using Matplotlib plots"""
    size_inches = size_inches or (5, 4)
    video = _ContextVideo(
        frames=[],
        _args=args,
        _kwargs=kwargs,
        _size_inches=size_inches,
    )
    yield video

    with tempfile.TemporaryDirectory() as temp_dir:
        for index, frame in enumerate(video.frames):
            path = os.path.join(temp_dir, f'video{index:04}.png')
            with open(path, 'wb') as f:
                f.write(frame)

        path_pattern = os.path.join(temp_dir, 'video%04d.png')
        subprocess.check_call(
            [
                'ffmpeg',
                '-r',
                str(frame_rate_hz),
                '-y',
                '-f',
                'image2',
                '-i',
                path_pattern,
                '-vcodec',
                'libx265',
                '-crf',
                '25',
                '-pix_fmt',
                'yuv420p',
                output_path,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        video = IPython.display.Video(filename=output_path)
        IPython.display.display(video)


def _display(fig, dpi, screen_dpi=_SCREEN_DPI):
    with io.BytesIO() as f:
        fig.savefig(f, dpi=dpi, format='png')
        plt.close(fig)

        width, height = fig.get_size_inches()
        image = IPython.display.Image(f.getvalue(),
                                      width=int(screen_dpi * width),
                                      height=int(screen_dpi * height))
        IPython.display.display(image)
