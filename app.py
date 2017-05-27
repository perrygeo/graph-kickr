#!/usr/bin/env python
import os

from fitparse import FitFile
from matplotlib.ticker import MaxNLocator
import click
import matplotlib.pyplot as plt
import pandas as pd


def get_records(fitfile, fields=None):
    if fields is None:
        fields = ['power', 'heart_rate', 'speed']

    for record in fitfile.get_messages('record'):
        # first pass, grab timestamp
        timestamp = None
        for entry in record:
            if entry.name == 'timestamp':
                timestamp = entry.value
        if timestamp is None:
            continue

        result = {'timestamp': timestamp}

        # second pass
        for entry in record:
            if entry.name in fields:
                # assume units, todo assert
                result[entry.name] = entry.value
        yield result


@click.command()
@click.argument("path")
@click.argument("outpng")
def main(path, outpng):
    """Analyze records from a Garmin .fit file
    """
    fitfile = FitFile(path)
    df = pd.DataFrame(get_records(fitfile)).set_index('timestamp', drop=False)

    # Make index an elapsed time
    df['minutes'] = df.index - df.index[0]
    df.index = df['minutes'].apply(lambda x: float(x.total_seconds()) / 60)  # minutes

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    for ax in axes:
        ax.spines["top"].set_visible(False)
        for spine in ax.spines.values():
            # spine.set_alpha(0.2)
            spine.set_color('LightGrey')
        ax.tick_params(color='LightGrey')
        ax.xaxis.tick_bottom()
        ax.yaxis.tick_left()

    axes[0].spines["right"].set_visible(False)
    df.plot(y='power', color="DarkBlue", label="Power (watts)", ax=axes[0], alpha=0.6)
    df.plot(y='heart_rate', color="Orange", label="Heart Rate (bpm)", alpha=0.6, ax=axes[0])
    axes[0].xaxis.set_major_locator(MaxNLocator(prune='lower'))
    axes[0].legend().get_frame().set_alpha(0)

    axes[1].spines["left"].set_visible(False)
    axes[1].yaxis.set_label_position("right")
    axes[1].yaxis.tick_right()
    df.plot.scatter(y='power', x='heart_rate', alpha=0.3, ax=axes[1])
    # df.plot.hexbin(y='power', x='heart_rate', legend=False, gridsize=24, ax=axes[1])

    plt.subplots_adjust(wspace=0.045, hspace=0)
    fig.suptitle(os.path.basename(path), fontsize=14)
    plt.savefig(outpng, bbox_inches="tight")
    print(outpng)


if __name__ == "__main__":
    main()
