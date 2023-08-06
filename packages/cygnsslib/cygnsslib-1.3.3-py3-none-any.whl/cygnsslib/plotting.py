import os
from typing import Optional, Union
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

sel_colormap = 'jet'  # matplotlib default is 'viridis'
default_fig_width = 8  # default figure width
plt_font_size = 12  # font size
plt_title = True  # plot figures titles
plot_db_range = 20  # default dynamic range of dB plots
default_save_type = ['png']  # default save image types
ddm_plt_default_delay_axis = 'x'


def pwr2db_threshold(power_linear, dynamic_range_db=None):
    """

    change power from linear two dB with a minimum threshold

    :param power_linear: power in linear scale
    :type power_linear: np.array
    :param dynamic_range_db: dynamic range in dB any value below the maximum by this is set to max - scale
    :type dynamic_range_db: float
    :return: power in dB scale
    :rtype: np.array
    """
    if dynamic_range_db is None:
        dynamic_range_db = plot_db_range

    threshold = np.max(power_linear) * 10 ** (-dynamic_range_db / 10)
    power_db = 10.0 * np.log10(np.where(power_linear < threshold, threshold, power_linear))
    return power_db


def plot_single_ddm(image, title, img_save_name, fig_out_folder, tf_save_fig=True, img_ext=None, fig_width=None, plt_delay_axis=None,
                    fig_save_types=None, cbar_min_max=None):
    """

    plot a single DDM

    :param cbar_min_max:
    :param fig_save_types: type of image? png, eps, pdf, svg ...
    :param image: DDM [dim 0: delay, dim 1: Doppler]
    :type image: np.array
    :param title: plot title
    :type title: str
    :param img_save_name: image save name
    :type img_save_name: str
    :param fig_out_folder: image saving folder
    :type fig_out_folder: str
    :param tf_save_fig: save the figure?
    :type tf_save_fig: bool
    :param img_ext: extend of the image
    :type img_ext: tuple
    :param fig_width: figure width, if None default_fig_width is selected
    :type fig_width: int or float
    :param plt_delay_axis: where the delay axis? select 'x' or 'y'
    :type plt_delay_axis: str or None
    :return: figure handle
    :rtype: plt.figure
    """
    if plt_delay_axis is None:
        plt_delay_axis = ddm_plt_default_delay_axis
    if fig_width is None:
        fig_width = default_fig_width
    if plt_delay_axis.lower() == 'x':
        image = np.transpose(image)
        y_label = 'Doppler bin'
        x_label = 'Delay bin'
        fig_size = (fig_width, np.round(fig_width * image.shape[0]/image.shape[1], decimals=2))
    elif plt_delay_axis.lower() == 'y':
        x_label = 'Doppler bin'
        y_label = 'Delay bin'
        fig_size = (np.round(fig_width * image.shape[1]/image.shape[0], decimals=2), fig_width * 0.9)
    else:
        raise RuntimeError(f'plt_delay_axis has only two options: x and y, you selected {plt_delay_axis}')
    if img_ext is None:
        (dely_len, dopler_len) = np.shape(image)
        img_ext = (-dopler_len / 2, dopler_len / 2, -dely_len / 2, dely_len / 2)

    fig = plt.figure(figsize=fig_size)
    ax = plt.subplot(111)
    im = ax.imshow(image, origin='lower', extent=img_ext, cmap=sel_colormap)
    if title and plt_title:  # this in case we want to remove titles for papers
        plt.title(title, fontsize=plt_font_size)
    plt.xlabel(x_label, fontsize=plt_font_size)
    plt.ylabel(y_label, fontsize=plt_font_size)
    ax.tick_params(axis='both', which='major', labelsize=plt_font_size)
    if cbar_min_max is not None:
        im.set_clim(cbar_min_max[0], cbar_min_max[1])

    # create an axes on the right side of ax. The width of cax will be 5%
    # of ax and the padding between cax and ax will be fixed at 0.05 inch.
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cbar = plt.colorbar(im, cax=cax)
    # cbar = plt.colorbar(fraction=c_fraction, pad=0.02)
    cbar.ax.tick_params(labelsize=plt_font_size)
    plt.tight_layout()
    save_figure(fig, fig_out_folder, img_save_name, tf_save_fig, fig_save_types)
    return fig


def save_figure(fig: plt.Figure, fig_out_folder: str, img_save_name: str, tf_save_fig: bool = True,
                fig_save_types: Optional[Union[list[str], str]] = None) -> bool:
    """
    save figure

    :param fig: figure object
    :param fig_out_folder: image saving folder
    :param img_save_name: image save name
    :param tf_save_fig: save the figure?
    :param fig_save_types: type of image? png, eps, pdf, svg ...
    :return: True if image is saved, else False
    """
    if not tf_save_fig:
        return False
    if fig_save_types is None:
        fig_save_types = default_save_type
    elif type(fig_save_types) is str:
        fig_save_types = [fig_save_types]
    for fig_type in fig_save_types:
        name = f"{img_save_name.split('.')[0]}.{fig_type}"
        fig.savefig(os.path.join(fig_out_folder, name), format=fig_type)
    return True
