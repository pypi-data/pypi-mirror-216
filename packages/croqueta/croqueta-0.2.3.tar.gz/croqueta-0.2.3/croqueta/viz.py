
from matplotlib.axes import Axes
from pathlib import Path

def savefig(fig, filename : str, path = None, size = None, dpi: int = 300):
    """
    Save a figure to a file.

    Parameters:
        - fig: The figure or axes object to save.
        - filename: The filename to save the figure as.
        - path: Optional. The directory path to save the figure in.
        - size: Optional. The size of the figure in inches (width, height).

    Note:
        - If `fig` is an `Axes` object, it will be converted to a `Figure` object.
        - If `path` is not provided, the figure will be saved in the current working directory.
        - If `size` is provided as a tuple, it will be used to set the figure size.

    Example usage:
        savefig(fig, 'myplot.png', path='output/', size=(10, 8))
    """
    if isinstance(fig, Axes):
        fig = fig.get_figure()
    if path is None:
        path = Path()
    elif isinstance(path,str):
        path = Path(path)
    if not filename.endswith('.png'):
        filename = filename + '.png'
    if isinstance(size, tuple):
        fig.set_size_inches(size)
    fig.savefig(path / filename, dpi = dpi) 