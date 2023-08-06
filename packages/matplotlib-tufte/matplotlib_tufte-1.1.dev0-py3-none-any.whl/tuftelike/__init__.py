# This file is part of matplotlib-tufte, Tufte-style plots for matplotlib.
# https://gitlab.com/lemberger/matplotlib-tufte
#
# SPDX-FileCopyrightText: 2022 Thomas Lemberger <https://thomaslemberger.com>
#
# SPDX-License-Identifier: Apache-2.0

"""
Tufte-style plots for matplotlib.

The workflow with this module is as follows:
First, create your initial plot in matplotlib,
then adjust its style with this module.

Example usage:

    import matplotlib.pyplot as plt
    import tuftelike

    fig = plt.scatter(x, y)
    tuftelike.adjust(fig)
"""

import logging
import math
import matplotlib.pyplot as plt  # type: ignore
from matplotlib.ticker import FixedFormatter, FixedLocator, NullLocator  # type: ignore

__version__ = "1.1.dev0"

logger = logging.getLogger(__name__)


def _pad_xlabel(ax):
    label = ax.get_xlabel()
    if not label:
        return
    ax.set_xlabel(label, labelpad=10)


def _pad_ylabel(ax):
    label = ax.get_ylabel()
    if not label:
        return
    ax.set_ylabel(label, labelpad=10)


def _pad_labels(ax):
    _pad_xlabel(ax)
    _pad_ylabel(ax)


def _remove_chart_junk(xs, ys, ax):
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    _reduce_spine_lengths(xs, ys, ax)


def _set_lims(xs, ys, ax, xpadding, ypadding):
    if isinstance(xs[0], str):
        xs = list(range(len(xs)))
    if isinstance(ys[0], str):
        ys = list(range(len(ys)))

    xlim_low, xlim_high = min(xs), max(xs)
    ylim_low, ylim_high = min(ys), max(ys)

    marginx = (xlim_high - xlim_low) * 0.1
    marginy = (ylim_high - ylim_low) * 0.1
    ax.set_xlim(xlim_low - marginx - xpadding, xlim_high + marginx + xpadding)
    ax.set_ylim(ylim_low - marginy - ypadding, ylim_high + marginy + ypadding)


def _scale_xy_ratio(xs, ys, ax):
    if ax.get_xscale() != ax.get_yscale():
        logger.warning(
            "Different scales for x (%s) and y (%s). Not scaling x/y ratio to 1.",
            ax.get_xscale(),
            ax.get_yscale(),
        )
        return
    xlim_low, xlim_high = min(xs), max(xs)
    ylim_low, ylim_high = min(ys), max(ys)
    lim_low = min(xlim_low, ylim_low)
    lim_high = max(xlim_high, ylim_high)
    ax.set_xlim(lim_low, lim_high)
    ax.set_ylim(lim_low, lim_high)
    ax.set_aspect("equal")


def _reduce_spine_lengths(xs, ys, ax):
    if isinstance(xs[0], str):
        xs = list(range(len(xs)))
    if isinstance(ys[0], str):
        ys = list(range(len(ys)))
    xlim_low, xlim_high = min(xs), max(xs)
    ylim_low, ylim_high = min(ys), max(ys)
    ax.spines["bottom"].set_bounds(low=xlim_low, high=xlim_high)
    ax.spines["left"].set_bounds(low=ylim_low, high=ylim_high)


def _set_new_ticks(xs, ys, ax):
    xaxis_inverted = ax.xaxis_inverted()
    yaxis_inverted = ax.yaxis_inverted()

    def get_lims(vs):
        minv, maxv = min(vs), max(vs)
        distance = maxv - minv
        assert distance >= 0, f"Distance {distance} for max {maxv} and min {minv}"
        return minv, maxv, distance

    def get_ticks(vs):
        lim_low, lim_high, distance = get_lims(vs)

        intermediates = [distance * p for p in (1 / 4, 1 / 2, 3 / 4)]
        # very small and large integer values become imprecise in float representation,
        # for example:
        # >>> int(-917011057314199522+0.0)
        # -917011057314199552
        #
        # So we make sure that we stay in the integer type for these.
        # At the moment, matplotlib does not produce sane plots for such big values either,
        # but we want to be at least hypothetically sound.
        if len(str(abs(lim_low))) > 15 or len(str(abs(lim_high))) > 15:
            intermediates = [int(d) for d in intermediates]
        # take the original lim_low and lim_high as ticks to not lose any precision through computations.
        ticks = [lim_low] + [lim_low + part for part in intermediates] + [lim_high]

        assert all(
            min(vs) <= v <= max(vs) for v in ticks
        ), f"Ticks out of range for min {min(vs)} and max {max(vs)}: To get violating ticks, run [v for v in {ticks} if not ({min(vs)} <= v <= {max(vs)})]"
        assert min(vs) in ticks
        assert max(vs) in ticks
        return ticks

    for axis in [ax.xaxis, ax.yaxis]:
        axis.set_minor_locator(NullLocator())

    def ticks_format(t, amplitude):
        if amplitude is not None:
            # if there is at least two values,
            # we round the values for the ticks, to make the labels well readable.
            # We round to one more decimal digit than the amplitude is (that's the +2).
            rounded = round(float(t), -int(amplitude) + 2)
        else:
            # if there is no amplitude between values, there's only one value.
            # in this case, we use the precise value and do not round.
            rounded = t
        if int(rounded) == rounded:
            # remove trailing '.0'
            return int(rounded)
        return rounded

    def set_ticks_labels(vs, ticks, axis):
        _, _, distance = get_lims(vs)
        if distance == 0:
            amplitude = None
        else:
            amplitude = int(math.log(distance, 10))
        axis.set_major_locator(FixedLocator(ticks))
        axis.set_major_formatter(
            FixedFormatter([ticks_format(t, amplitude) for t in ticks])
        )

    # we keep ticks for categories (string values) as they are, so we only change ticks for x/y if it has numeric values.
    if isinstance(xs[0], str):
        xticks = get_ticks(xs)
        set_ticks_labels(xs, xticks, ax.xaxis)
        ax.set_xticks(xticks)
        if xaxis_inverted:
            ax.invert_xaxis()
    if isinstance(ys[0], str):
        yticks = get_ticks(ys)
        set_ticks_labels(ys, yticks, ax.yaxis)
        ax.set_yticks(yticks)
        if yaxis_inverted:
            ax.invert_yaxis()


# disable too-many-arguments because we may want to have lots of optional arguments in the future
# pylint: disable=too-many-arguments
def adjust(xs, ys, ax=None, same_ratio=False, xpadding=0, ypadding=0, **kwargs):
    """
    Turns the plot into a tufte-like plot.

    Args:
        xs: x values in the plot.
        ys: y values in the plot
        ax: matplotlib axis to adjust. If None, the current axis is used.
        same_ratio: if False, nothing happens. If True, the x/y ratio is set to 1. This requires both axes to use the same scale (linear or logarithmetic).
        xpadding: padding to add in the front of the x axis. This is useful if you want to add some space to the left of the plot, for example to make spar foce wide bar plot bars.
        ypadding: padding to add below the y axis. This is useful if you want to add some space below the plot, for example to make space for wide vertical bar plot bars.
    """
    del kwargs  # we keep kwargs to keep the API backwards compatible in the future
    if ax is None:
        ax = plt.gca()
    _pad_labels(ax)
    if same_ratio:
        _scale_xy_ratio(xs, ys, ax)

    _set_lims(xs, ys, ax, xpadding, ypadding)
    _set_new_ticks(xs, ys, ax)
    _remove_chart_junk(xs, ys, ax)
    return ax
