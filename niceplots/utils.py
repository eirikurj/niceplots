from __future__ import division
# Matplotlib modules
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Global modules
import numpy as np
import random

# 3d-party modules
from adjustText import adjust_text


def handle_close(evt):
    """ Handler function that saves the figure as a pdf if the window is closed. """
    plt.tight_layout()
    plt.savefig('figure.pdf')

def adjust_spines(ax = None, spines=['left', 'bottom'], smart_bounds=True, outward=False):
    """ Function to shift the axes/spines so they have that offset
        Doumont look. """
    if ax == None:
        ax = plt.gca()

    # Loop over the spines in the axes and shift them
    for loc, spine in ax.spines.items():
        if loc in spines:
            if outward:
                spine.set_position(('outward', 12))  # outward by 18 points
            spine.set_smart_bounds(smart_bounds)
        else:
            spine.set_color('none')  # don't draw spine

    # turn off ticks where there is no spine
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        # no yaxis ticks
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])


def draggable_legend(axis = None, color_on = True):
    """ Function to create draggable labels on a plot. """
    if axis == None:
        axis = plt.gca()

    # Get the limits and relevant parameters
    xlim = axis.get_xlim()
    ylim = axis.get_ylim()
    xl, yl = xlim[1] - xlim[0], ylim[1] - ylim[0]
    legend = []
    nlines = len(axis.lines)

    # Set the coordinates of the starting location of the draggable labels
    n = np.ceil(np.sqrt(nlines))
    lins = np.linspace(.1, .9, n)
    xs, ys = np.meshgrid(lins, lins)
    xs = xs.reshape(-1)
    ys = ys.reshape(-1)
    coords = np.zeros(2)

    # Loop over each line in the plot and create a label
    for idx, line in enumerate(axis.lines):

        # Set the starting coordinates of the label
        coords[0] = xs[idx]
        coords[1] = ys[idx]
        label = line.get_label()

        # Get the color of each line to set the label color as the same
        if color_on:
            color = line.get_color()
        else:
            color = 'k'

        # Set each annotation and make them draggable
        legend.append(axis.annotate(label, xy=coords,
                   ha="center", va="center", color=color,
                   xycoords='axes fraction'
                   ))
        legend[idx].draggable()

def auto_place_legend(ax, rel_xloc=None, color_on=True, **kwargs):
    """
    This function tries to automatically place legend text
    close to the respective line and tries to minimize the 
    possible overlap with other lines and text. This function uses
    a the adjustText module.

    Inputs:
        ax : matplotlib axes
            Single matplotlib axes
        rel_xloc : list or scalar
            Relative location (between 0 and 1) on the x axis 
            where to *try* to place the legend text. List has to be the 
            same length as the number of lines in plot.
            If not specified random location will be chosen.
        color_on : bool
            Use the color on the line to color the legend text.
        kwargs : optional keyword arguments
            This is intended to tweak the adjustText tool (passed onwards)
    """
    nLines = len(ax.lines)

    # If using a scalar generate a full list needed for placing line label
    if type(rel_xloc) is float:
        rel_xloc = nLines * [rel_xloc]

    # Loop over the lines in the axes to get line label text and color
    texts = []
    for i, line in enumerate(ax.lines):

        # Extract the xy data (numpy Nx2 array) for a given line
        coords = line.get_xydata()
        
        # Set the starting x-coordinates of the label either using the
        # relative locations or randomly
        if rel_xloc is not None:
            idx = int(rel_xloc[i] * coords[:,0].shape[0])
        else:
            # Select randomly one point from the dataset to place the text
            idx = np.random.randint(0, coords.shape[0])
        
        label = line.get_label()
        # Get the color of each line to set the label color as the same
        if color_on:
            color = line.get_color()
        else:
            color = 'k'    

        # Create the text object and place it at this random location on line
        t = ax.text(coords[idx,0], coords[idx,1], label, ha="center", va="center", color=color)
        texts.append(t)

    adjust_text(texts, ax=ax, **kwargs)



def horiz_bar(labels, times, header, ts=1, nd=1, size=[5, .5], color='#FFCC00'):
    """ Creates a horizontal bar chart to compare positive numbers.

    'labels' contains the ordered labels for each data set
    'times' contains the numerical data for each entry
    'header' contains the left and right header for the labels and
    numeric data, respectively
    'ts' is a scaling parameter that's useful when the labels
    have many skinny or wide characters
    'nd' is the number of digits to show after the decimal point for the data
    'size' is the size of the final figure (iffy results)
    'color' is a hexcode for the color of the scatter points used

    """

    # Obtain parameters to size the chart correctly
    num = len(times)
    width = size[0]
    height = size[1] * num
    t_max = max(times)
    l_max = len(max(labels, key=len))

    # Create the corresponding number of subplots for each individual timing
    fig, axarr = plt.subplots(num, 1)

    # Playing with these values here can help with label alignment
    left_lim = -ts*l_max*.038*t_max
    right_lim = t_max*1.11

    # These values tweak the header label placement
    left_header_pos = -len(header[0])*.018*t_max + left_lim/2
    right_header_pos = -len(header[1])*.018*t_max + right_lim + t_max*(.09+nd*.02)

    # Loop over each time and get the max number of digits
    t_max_digits = 0
    for t in times:
        tm = len(str(int(t)))
        if tm > t_max_digits:
            t_max_digits = tm

    # Actual loop that draws each bar
    for j,(l,t,ax) in enumerate(zip(labels, times, axarr)):

        # Draw the gray line and singular yellow dot
        ax.axhline(y=1, c='#C0C0C0', lw=3, zorder=0)
        ax.scatter([t],[1], c=color, lw=0, s=100, zorder=1, clip_on=False)

        # Set chart properties
        ax.set_ylim(.99, 1.01)
        ax.set_xlim(0, t_max*1.05)
        ax.tick_params(
            axis='both',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            left=False,      # ticks along the bottom edge are off
            labelleft=False,
            labelright=False,
            labelbottom=False,
            right=False,         # ticks along the top edge are off
            bottom=j==num,
            top=False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.text(left_lim, 1, l, va='center')
        d = t_max_digits - len(str(int(t)))
        string = '{number:.{digits}f}'.format(number=t, digits=nd)
        ax.text(right_lim*1.15, 1, string, va='center', ha='right')

        # Create border graphics if this is the top bar line
        if j == 0:
            ax.text(left_header_pos,1.02, header[0], fontsize=13)
            ax.text(right_header_pos,1.02, header[1], fontsize=13)

            line = Line2D([left_lim, right_lim+t_max*(.15+nd*.03)], [1.014, 1.014], lw=1.2, color='k')
            line.set_clip_on(False)
            ax.add_line(line)

            # line = Line2D([left_lim, right_lim+t_max*(.15+nd*.03)], [1.012, 1.012], lw=1.2, color='k')
            # line.set_clip_on(False)
            # ax.add_line(line)

    # Save the figure and export as pdf
    fig.set_size_inches(width, height)
    fig.savefig('bar_chart.pdf', bbox_inches="tight")

def stacked_plots(xlabel, xdata, data_dict_list, figsize=(12, 10), pad=200, filename='stacks.png', xticks=None, cushion=0.1):

    # If it's a dictionary, make it into a list so we can generically loop over it
    if type(data_dict_list) == type({}):
        data_dict_list = [data_dict_list]

    data_dict = data_dict_list[0]
    n = len(data_dict)

    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    f, axarr = plt.subplots(n, figsize=figsize)

    for i, (ylabel, ydata) in enumerate(data_dict.items()):
        if type(ydata) == dict:
            if 'limits' in ydata.keys():
                axarr[i].set_ylim(ydata['limits'])
            elif 'ticks' in ydata.keys():
                axarr[i].set_yticks(ydata['ticks'])
                low_tick = ydata['ticks'][0]
                high_tick = ydata['ticks'][-1]
                height = high_tick - low_tick
                limits = [low_tick - cushion * height, high_tick + cushion * height]
                axarr[i].set_ylim(limits)

        axarr[i].set_ylabel(ylabel, rotation='horizontal', horizontalalignment='left', labelpad=pad)

    for data_dict in data_dict_list:
        for i, (ylabel, ydata) in enumerate(data_dict.items()):
            if type(ydata) == dict:
                ydata = ydata['data']
            axarr[i].plot(xdata, ydata, clip_on=False, lw=6)
            axarr[i].scatter(xdata, ydata, clip_on=False, edgecolors='white', s=100, lw=1.5, zorder=100)

    for i,ax in enumerate(axarr):
        adjust_spines(ax)
        if i < len(axarr)-1:
            ax.xaxis.set_ticks([])
        else:
            ax.xaxis.set_ticks_position('bottom')
            if xticks is not None:
                ax.xaxis.set_ticks(xticks)

    f.align_labels()

    axarr[-1].set_xlabel(xlabel)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    # plt.show()

    return f, axarr



def all():
    """ Runs all of the functions provided in this module. """
    adjust_spines()
    draggable_legend()
    plt.gcf().canvas.mpl_connect('close_event', handle_close)
