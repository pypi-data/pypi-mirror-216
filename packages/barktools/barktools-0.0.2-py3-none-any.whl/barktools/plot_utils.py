# Functions here may depend on the matplotlib package
import random
import itertools
import math

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors



# Variables 
##########################################
plt_colors_base = list(dict(mcolors.BASE_COLORS).keys())
plt_colors_css4 = list(dict(mcolors.CSS4_COLORS).keys())




# Functions
##########################################

# TODO: Better solution for seeding. Currently, seeding would affect all randomizations for the rest of the functions in this module, right?
def color_cycler_plt(colormap='base', order=None, n_colors=None, seed=None): 
    ''' Returns an iterator for matplotlib colors

        Parameters
        --------------
        colormap : str, ['base' (default), 'css4']
            Name of colormap to use
        order : (OPTIONAL) list of int OR str=='random'
            I have no clue what I was smoking here, just leave it at None.
            If order is a string ('random'), the number of colors can be specified with n_colors.
            If order is a list, the number of colors is taken to be the length of the list.
        n_colors : int
            Same as above, just leave it at None
        seed : int
            I guess?

        Returns
        ------------
        plt_color_cycler : iterator
            Iterator for matplotlib colors

    '''

    if colormap == 'base':
        plt_colors = plt_colors_base
    elif colormap == 'css4':
        plt_colors = plt_colors_css4
    else:
        print('plt_color_cycler: Please specify a valid colormap. Using base for now.')
        plt_colors = plt_colors_base

    if seed is not None:
        random.seed(seed)

    if order is not None:
        if order == 'random':
            order = list(range(len(plt_colors)))
            random.shuffle(order)
            if n_colors is not None:
                order = [order[i] for i in range(n_colors)] # Shrink the list

        assert(isinstance(order, list))
        plt_colors = [plt_colors[i] for i in order]

    plt_color_cycler = itertools.cycle(plt_colors)

    return plt_color_cycler

# NOTE: scikit-learn recommends using PCA to reduce the number of dimensions to less than 50 if it is higher than that before transforming with TSNE
# TODO: Implement downsampling
# TODO: Refactor function to return an axis object
def scatter_tsne_2d(data, downsampling_ratio=0):
    ''' Scatter the 2D TSNE decomoposition of a dataset

        Parameters
        -----------------
        data : list of ndarrays, 
            Each ndarray represents the features of samples of one category and has shape shape=[n_samples, n_features].
            n_samples may vary between categories.
        downsampling_ratio : float, between 0 and 1
            Discard a proportion downsampling_ratio of the data for plotting
            NOTE: Not yet implemented

        Notes
        ------------------
        - (DEPENDS) barktools.plot_utils.color_cycler_plt

    '''
    tsne = TSNE(n_components=2)
    color_cycler = color_cycler_plt()

    x_all = np.concatenate(tuple(data), axis=0)
    x_transformed = tsne.fit_transform(x_all)

    n_labels = len(data)
    prev_idx = 0
    for i in range(n_labels):
        this_n_samples = data[i].shape[0]
        x = x_transformed[prev_idx:prev_idx+this_n_samples,:]
        prev_idx += this_n_samples
        color = next(color_cycler)
        plt.scatter(x[:,0], x[:,1], c=color)

    plt.show()

def get_bins(data, bin_width):
    ''' Generate bin edges for a histogram with specified width for target data

        Parameters
        -----------------
        data : array_like
            Data to be plotted in a histogram
        bin_width : float
            Target bin width of histogram bins

        Returns
        -------------------
        bins : list
            List of bin edges, including right edge of rightmost bin
    '''
    lower = min(data)
    upper = max(data)
    n_bins = math.ceil((upper-lower) / bin_width)
    eps = (n_bins*bin_width - (upper-lower)) / 2
    bins = [lower-eps+i*bin_width for i in range(n_bins+1)]
    return bins



# Classes
#####################################

# Abstract class
# Updates content of axis according to index
# Usage: 
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax_gen.__update_ax__(ax, index)
class AxesGenerator:
    ''' Abstract base class which maps an index to axis content, and updates an axis with that content.

        Examples
        -----------------
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax_gen = AxesGeneratorExample()
        ax_gen.update_ax(ax, 3)

    '''
    def update_ax(self, ax, index):
        ''' Update the contents of 'ax' according 'index'

            Parameters 
            ----------------
            ax : matplotlib.axes.Axes
                Axes whose contents is to be updated
            index : int
                Content index
        '''
        raise NotImplementedError
    def __len__(self):
        raise NotImplementedError

class PlotScroller:
    ''' Updates the axes object of a figure when you scroll according to an Axes-generator which outputs an axes according to an index 

        Parameters
        ----------------
        ax : matplotlib.axes.Axes
            Axes whose content is to be updated on scroll
        ax_gen : AxesGenerator
            AxesGenerator to determine how the contents is updated when scrolling up/down

        Examples
        ----------------------
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax_gen = AxesGeneratorExample()
        plot_scroller = PlotScroller(ax, ax_gen)

        Notes
        -------------------
        - (DEPENDS) barktool.plot_utils.AxesGenerator

    '''
    def __init__(self, ax, ax_gen):

        self.ax_gen = ax_gen # Instance of AxesGenerator
        self.ax = ax

        self.__index = 0
        self.__len = len(self.ax_gen)

        self.__draw()
        self.ax.get_figure().canvas.mpl_connect('scroll_event', self.__onscroll)

    def __onscroll(self, event): 
        if event.button == 'up':
            self.__index = (self.__index + 1) % self.__len
        else:
            self.__index = (self.__index - 1) % self.__len
        self.__draw()

    def __draw(self):
        self.ax_gen.__update_ax__(self.ax, self.__index)
        plt.draw()

    def __len__(self):
        return self.__len


# Plotting functions (Create specific plots)
def plot_timelines(ax, event_times, unit="h"):
    """Plots timelines for each of n_trials process realizations next to each other
    
    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Matplotlib axes object to plot into
    event_times : list of np.ndarray, len=n_trials
        event_times[i] contains an ndarray of event times for the i:th trial
    unit : str
    """
    n_timelines = len(event_times)
    timeline_heights = np.linspace(0, 1, num=n_timelines+2)[1:-1]
    for i in range(n_timelines):
        ax.scatter(event_times[i], timeline_heights[i]*np.ones(len(event_times[i])), marker='|')
    ax.set_ylim(0,1)
    ax.set_yticks(timeline_heights, minor=False)
    ax.set_yticklabels(np.arange(n_timelines)+1)
    ax.yaxis.grid(True, which='major')
    ax.set_ylabel('Timeline #')
    ax.set_xlabel(f"Time ({unit})")

