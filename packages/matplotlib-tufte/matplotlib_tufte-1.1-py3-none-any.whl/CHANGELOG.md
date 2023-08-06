<!--
This file is part of matplotlib-tufte, Tufte-style plots for matplotlib.
https://gitlab.com/lemberger/matplotlib-tufte

SPDX-FileCopyrightText: 2022 Thomas Lemberger <https://thomaslemberger.com>

SPDX-License-Identifier: Apache-2.0
-->

# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1]

Added:

- Method `tuftelike.adjust` now has parameters `xpadding` and `ypadding`:

      xpadding: padding to add in the front of the x axis.
                This is useful if you want to add some space to the left of the plot,
                for example to make spar foce wide bar plot bars.
      ypadding: padding to add below the y axis.
                This is useful if you want to add some space below the plot,
                for example to make space for wide vertical bar plot bars.
  
  Examples for these parameters are included.

Fixed:

- tuftelike now creates correct ticks for very large value points (coordinates with more than 15 digits).
  At the moment, matplotlib can not produce proper plots for such large values,
  but at least tuftelike does not destroy the ticks labels now.
- tuftelike now supports categories of bar charts on the x- and y-axis.


## [1.0]

Added:

- Method `tuftelike.adjust` allows to turn existing Matplotlib plots into tufte-like plots
  with less chart-junk and more expressive axis boundaries. 



[Unreleased]: https://gitlab.com/lemberger/matplotlib-tufte/-/compare/1.1...main
[1.0]: https://gitlab.com/lemberger/matplotlib-tufte/-/tree/1.0
[1.1]: https://gitlab.com/lemberger/matplotlib-tufte/-/tree/1.1
