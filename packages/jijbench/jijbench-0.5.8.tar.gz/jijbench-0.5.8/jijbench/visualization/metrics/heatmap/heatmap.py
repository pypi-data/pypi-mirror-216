from __future__ import annotations

from numbers import Number

import numpy as np
import plotly
import plotly.express as px

import jijbench as jb


class HeatMap:
    """Visualize heatmap by plotly.

    Attributes:
        experiment (jb.Experiment): the experiment to visualize.
        savefig (bool): If True, save the figure.
        savedir (str): the directory to save the figure.
        savescale (int): corresponds to the resolution of the figure.

    Example:
        ```python
        import jijbench as jb
        from jijbench.visualization import HeatMap

        def solve(parameter1, parameter2):
            return parameter1 + parameter2

        bench = jb.Benchmark(
            solver=solve,
            params={
                "parameter1": [2, 1],
                "parameter2": [2, 3, 1,],
            },
        )
        experiment = bench(autosave=True)

        heatmap = HeatMap(experiment=experiment)
        fig = heatmap.create_figure(
            color_column="solver_output[0]",
            x_column="parameter1",
            y_column="parameter2",
        )
        fig.show()
        ```

        You can change the appearance of the figure by `update_layout` method.
        The example below changes the fontsize of the title.
        For other settings, please refer to the plotly reference.

        ```python
        fig.update_layout(title_font={"size": 30})
        fig.show()
        ```
    """

    def __init__(
        self,
        experiment: jb.Experiment,
        savefig: bool = True,
        savedir: str = ".",
        savescale: int = 2,
    ) -> None:
        """Initialize the HeatMap instance with the given parameters.

        Args:
            experiment (jb.Experiment): the experiment to visualize.
            savefig (bool, optional): If True, save the figure. Defaults to True.
            savedir (str, optional): the directory to save the figure. Defaults to `.`.
            savescale (int, optional): corresponds to the resolution of the figure. Defaults to 2.
        """
        self._experiment = experiment
        self._savefig = savefig
        self._savedir = savedir
        self._savescale = savescale

    def create_figure(
        self,
        color_column: str,
        x_column: str,
        y_column: str,
        title_text: str = "Heatmap",
        title_x: float = 0.5,
        title_y: float = 0.95,
        height: int = 600,
        width: int = 600,
        reverse_yaxis_order: bool = False,
        xaxis_title: str | None = None,
        yaxis_title: str | None = None,
        coloraxis_title: str | None = None,
        savefig: bool | None = None,
        savedir: str | None = None,
        savename: str | None = None,
        savescale: int | None = None,
    ) -> plotly.graph_objects.Figure:
        """Create a figure using plotly.

        The x-axis elements are in ascending order from left to right.
        The y-axis elements are in ascending order from bottom to top by default,
        but you can reverse this order by setting `reverse_yaxis_order` to `True`.

        Also note that if the elements in the given column are non-numeric,
        they are converted to strings before sorted.
        That is, non-numeric elements are sorted lexicographically.

        Args:
            color_column (str): the column name used for coloring the heatmap.
            x_column (str): the column name used for x-axis.
            y_column (str): the column name used for y-axis.
            title_text (str, optional): the title of the figure. Defaults to "Heatmap".
            title_x (float, optional): the x position of the title. Defaults to 0.5.
            title_y (float, optional): the y position of the title. Defaults to 0.95.
            height (int, optional): the height of the figure. Defaults to 600.
            width (int, optional): the width of the figure. Defaults to 600.
            reverse_yaxis_order (bool, optional): If True, arrange in ascending order from top to bottom. Defaults to False.
            xaxis_title (str | None, optional): the title of the x-axis. If None is given, `x_column` will be used. Defaults to None.
            yaxis_title (str | None, optional): the title of the y-axis. If None is given, `y_column` will be used. Defaults to None.
            savefig (bool | None, optional): If True, save the figure. If None is given, the value given to the constructor will be used. Defaults to None.
            savedir (str | None, optional): the directory to save the figure. If None is given, the value given to the constructor will be used. Defaults to None.
            savename (str | None, optional): the name of the figure. Since it is automatically saved as png, no extension is required.
                If None is given, it will be same as `title`. Defaults to None.
            savescale (int | None, optional): corresponds to the resolution of the figure. If None is given, the value given to the constructor will be used. Defaults to None.

        """
        if xaxis_title is None:
            xaxis_title = x_column
        if yaxis_title is None:
            yaxis_title = y_column
        if coloraxis_title is None:
            coloraxis_title = color_column
        if savefig is None:
            savefig = self._savefig
        if savedir is None:
            savedir = self._savedir
        if savename is None:
            savename = title_text
        if savescale is None:
            savescale = self._savescale

        experiment_table = self._experiment.table

        if color_column not in experiment_table.columns:
            raise ValueError(f"color_column={color_column} is not in the experiment.")
        if x_column not in experiment_table.columns:
            raise ValueError(f"x_column={x_column} is not in the experiment.")
        if y_column not in experiment_table.columns:
            raise ValueError(f"y_column={y_column} is not in the experiment.")

        def is_numeric(x):
            try:
                float(x)
            except ValueError:
                return False
            else:
                return True

        if not is_numeric(experiment_table[color_column].iloc[0]):
            raise ValueError("color_column must be numeric, but it is not.")

        # Convert non-numeric columns to strings. This ensures that it is Hashable and sorted as a string.
        # If you leave the y_column elements as Unhashable, you will get an error on the following pivot operation.
        if not np.issubdtype(experiment_table[x_column].dtype, np.number):
            experiment_table[x_column] = experiment_table[x_column].astype(str)
        if not np.issubdtype(experiment_table[y_column].dtype, np.number):
            experiment_table[y_column] = experiment_table[y_column].astype(str)

        # reverse_yaxis_order is False (default): Arrange in ascending order from bottom to top. Intended for use with numeric values.
        # reverse_yaxis_order is True: Arrange in ascending order from top to bottom.Intended for use with string.
        heatmap_table = experiment_table.pivot(
            index=y_column, columns=x_column, values=color_column
        ).sort_index(ascending=reverse_yaxis_order)

        fig = px.imshow(
            heatmap_table,
            x=[
                str(i) for i in heatmap_table.columns
            ],  # If the elements of x are numbers, they must be converted to strings.
            y=[
                str(i) for i in heatmap_table.index
            ],  # If the elements of y are numbers, they must be converted to strings.
            color_continuous_scale="deep_r",
            aspect="auto",
        )
        fig.update_layout(
            height=height,
            width=width,
            xaxis=dict(title=xaxis_title),
            yaxis=dict(title=yaxis_title),
            coloraxis_colorbar=dict(
                title=f"{coloraxis_title}<br><span style='color:white;'>_</span>"
            ),  # The elements from <br> is for spacing between the coloraxis_title and the colorbar.
            title=dict(
                text=title_text,
                y=title_y,
                x=title_x,
                xanchor="center",
                yanchor="top",
            ),  # Change the position of the title from the default top left to center top
            font=dict(family="Arial"),  # Change font to Arial
        )
        # change hovertemplate because the color_column name is simply "color" by default.
        # <extra></extra> is required to remove the hoverdata index to enhance the readability of the figure.
        fig.update_traces(
            hovertemplate="<br>".join(
                [
                    f"{x_column}: %{{x}}",
                    f"{y_column}: %{{y}}",
                    f"{color_column}: %{{z}}",
                ]
            )
            + "<extra></extra>"
        )

        if savefig:
            fig.write_image(f"{savedir}/{savename}.png", scale=savescale)
        return fig

    @property
    def experiment(self):
        return self._experiment

    @property
    def savefig(self):
        return self._savefig

    @property
    def savedir(self):
        return self._savedir

    @property
    def savescale(self):
        return self._savescale
