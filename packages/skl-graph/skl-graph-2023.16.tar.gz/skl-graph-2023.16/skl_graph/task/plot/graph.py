# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2018)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from typing import Callable

import networkx as ntkx
import numpy as nmpy

from skl_graph.graph import skl_graph_t
from skl_graph.task.plot.base import (
    FigureAndAxesFromBoth,
    ManagePlotOptions,
    YTransformations,
    YTransformationsFromAxes,
    axes_3d_t,
    axes_any_h,
    axes_t,
    figure_t,
    y_transform_h,
)
from skl_graph.task.plot.edge import Plot as PlotEdges
from skl_graph.task.plot.node import (
    Plot2DBranchNodes,
    Plot2DEndNodes,
    Plot2DNodeLabels,
    Plot3DBranchNodes,
    Plot3DEndNodes,
    Plot3DNodeLabels,
    PositionsForPlotFromDetails,
    positions_as_dict_h,
)
from skl_graph.type.plot import plot_mode_e

array_t = nmpy.ndarray


def Plot(
    skl_graph: skl_graph_t,
    /,
    *,
    figure: figure_t = None,
    axes: axes_any_h = None,
    mode: plot_mode_e = plot_mode_e.SKL_Pixel,
    should_block: bool = True,
    should_return_figure: bool = False,
    should_return_axes: bool = False,
) -> figure_t | axes_t | axes_3d_t | tuple[figure_t, axes_any_h] | None:
    """"""
    if skl_graph.n_nodes < 1:
        return None

    figure, axes = FigureAndAxesFromBoth(figure, axes, skl_graph.dim)
    TransformedY, TransformedYForVector = YTransformationsFromAxes(
        axes, skl_graph.domain_shape[0]
    )
    positions_as_dict = PositionsForPlotFromDetails(
        skl_graph.nodes.data("details"), TransformedY
    )

    if mode is plot_mode_e.Networkx:
        if skl_graph.dim != 2:
            raise ValueError(
                f'{skl_graph.dim}: Invalid dimension for plot mode "plot_mode_e.Networkx". Expected=2.'
            )

        if skl_graph.label_styles[1].show:
            edge_labels = EdgeLabelsForPlot(skl_graph)
        else:
            edge_labels = None
        _PlotWithNetworkX(
            skl_graph,
            axes,
            node_positions=positions_as_dict,
            node_colors=NodeColors(skl_graph),
            with_node_labels=skl_graph.label_styles[0].show,
            node_font_size=int(round(skl_graph.label_styles[0].size)),
            edge_width=skl_graph.edge_styles[0].size,
            edge_labels=edge_labels,
            edge_font_size=int(round(skl_graph.label_styles[1].size)),
        )
    else:
        _PlotExplicitly(
            skl_graph,
            positions_as_dict,
            TransformedY,
            TransformedYForVector,
            axes,
            mode,
        )

    return ManagePlotOptions(
        figure,
        axes,
        should_block,
        should_return_figure,
        should_return_axes,
    )


def PlotNetworkXGraph(
    graph: ntkx.MultiGraph,
    /,
    *,
    NodePositions: Callable[[axes_t], positions_as_dict_h] = None,
    node_colors: tuple[str, ...] = None,
    with_node_labels: bool = False,
    node_font_size: int = None,
    edge_width: int = None,
    edge_labels: dict[str, str] = None,
    edge_font_size: int = None,
    figure: figure_t = None,
    axes: axes_t = None,
    should_block: bool = True,
    should_return_figure: bool = False,
    should_return_axes: bool = False,
) -> figure_t | axes_t | axes_3d_t | tuple[figure_t, axes_t] | None:
    """
    Only 2-D graphs
    """
    if graph.number_of_nodes() < 1:
        return None

    figure, axes = FigureAndAxesFromBoth(figure, axes, 2)

    if NodePositions is None:
        node_positions = None
    else:
        node_positions = NodePositions(axes)
    _PlotWithNetworkX(
        graph,
        axes,
        node_positions=node_positions,
        node_colors=node_colors,
        with_node_labels=with_node_labels,
        node_font_size=node_font_size,
        edge_width=edge_width,
        edge_labels=edge_labels,
        edge_font_size=edge_font_size,
    )

    return ManagePlotOptions(
        figure,
        axes,
        should_block,
        should_return_figure,
        should_return_axes,
    )


def NodePositionsForPlot(
    skl_graph: skl_graph_t, /
) -> Callable[[axes_any_h], positions_as_dict_h]:
    """"""
    YTransformationsForAxes = YTransformations(skl_graph.domain_shape[0])

    return lambda _axs: PositionsForPlotFromDetails(
        skl_graph.nodes.data("details"), YTransformationsForAxes(_axs)[0]
    )


def NodeColors(skl_graph: skl_graph_t, /) -> tuple[str, ...]:
    """"""
    degrees = skl_graph.degree
    node_styles = skl_graph.node_styles
    default_style = node_styles[None]

    return tuple(
        node_styles.get(degrees[_nde], default_style).color for _nde in skl_graph.nodes
    )


def EdgeLabelsForPlot(skl_graph: skl_graph_t, /) -> dict[str, str]:
    """"""
    output = {}

    details_as_dict = ntkx.get_edge_attributes(skl_graph, "details")
    for key, value in details_as_dict.items():
        output[key[0:2]] = f"{key[2]}\n{round(value.measures.length)}"

    return output


def _PlotExplicitly(
    skl_graph: skl_graph_t,
    node_label_positions: positions_as_dict_h,
    TransformedY: y_transform_h,
    TransformedYForVector: y_transform_h,
    axes: axes_any_h,
    mode: plot_mode_e,
    /,
) -> None:
    """"""
    PlotEdges(
        skl_graph.edges.data("details"),
        TransformedY,
        TransformedYForVector,
        axes,
        skl_graph.edge_styles,
        skl_graph.direction_style,
        skl_graph.label_styles[1],
        mode,
    )

    if skl_graph.dim == 2:
        PlotEndNodes = Plot2DEndNodes
        PlotBranchNodes = Plot2DBranchNodes
    else:
        PlotEndNodes = Plot3DEndNodes
        PlotBranchNodes = Plot3DBranchNodes
    # Note: there is no distinction between end nodes and isolated nodes
    PlotEndNodes(
        skl_graph.nodes.data("details"),
        TransformedY,
        axes,
        skl_graph.node_styles,
    )
    PlotBranchNodes(
        skl_graph.nodes.data("details"),
        skl_graph.degree,
        TransformedY,
        axes,
        skl_graph.node_styles,
    )

    if skl_graph.label_styles[0].show:
        if skl_graph.dim == 2:
            Plot2DNodeLabels(skl_graph, node_label_positions, axes)
        else:
            Plot3DNodeLabels(
                skl_graph, node_label_positions, axes, skl_graph.label_styles[0]
            )


def _PlotWithNetworkX(
    graph: ntkx.MultiGraph | skl_graph_t,
    axes: axes_t,
    /,
    *,
    node_positions: positions_as_dict_h = None,
    node_colors: tuple[str, ...] = None,
    with_node_labels: bool = False,
    node_font_size: int = None,
    edge_width: int = None,
    edge_labels: dict[str, str] = None,
    edge_font_size: int = None,
) -> None:
    """"""
    options = {}
    if node_positions is not None:
        options["pos"] = node_positions
    if node_colors is not None:
        options["node_color"] = node_colors
    if node_font_size is not None:
        options["font_size"] = node_font_size
    if edge_width is not None:
        options["width"] = edge_width
    ntkx.draw_networkx(
        graph,
        ax=axes,
        with_labels=with_node_labels,
        **options,
    )

    if (edge_labels is not None) and (node_positions is not None):
        options = {"edge_labels": edge_labels}
        if edge_font_size is not None:
            options["font_size"] = edge_font_size
        ntkx.draw_networkx_edge_labels(
            graph,
            node_positions,
            ax=axes,
            **options,
        )
