<!--
This file is part of matplotlib-tufte, Tufte-style plots for matplotlib.
https://gitlab.com/lemberger/matplotlib-tufte

SPDX-FileCopyrightText: 2022 Thomas Lemberger <https://thomaslemberger.com>

SPDX-License-Identifier: Apache-2.0
-->
# matplotlib-tufte

matplotlib-tufte is a python module
to create Tufte-like plots with matplotlib.

Inspiration is drawn from [*Edward Tufte: The Visual Display of Quantitative Information*][TufteBook].

[TufteBook]: https://www.edwardtufte.com/tufte/books_vdqi

## Requirements

- python >= 3.7
- matplotlib

## Examples

See [examples/Basic.ipynb](https://gitlab.com/lemberger/matplotlib-tufte/-/blob/main/examples/Basic.ipynb)
for some small examples of tuftelike plots.

## Usage

Create your plots with matplotlib as usual.
Then, run `tuftelike.adjust` with the x- and y-values of your plot to adjust it in-place.

```
import matplotlib.pyplot as plt
import tuftelike

xs, ys = [1, 2, 3, 4], [1, 4, 2, 3]
plt.plot(xs, ys)

tuftelike.adjust(xs, ys)
plt.savefig("example.png")
```

Tuftelike needs the x- and y-values because matplotlib does not store these internally.
The above code produces:

![an example tuftelike plot](https://gitlab.com/lemberger/matplotlib-tufte/-/raw/main/examples/simple.png).
