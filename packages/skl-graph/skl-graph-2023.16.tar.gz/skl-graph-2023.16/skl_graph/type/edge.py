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

from __future__ import annotations

import dataclasses as dtcl
from types import MethodType
from typing import Any
from typing import NamedTuple as named_tuple_t
from typing import Sequence

import numpy as nmpy
import scipy.interpolate as spnt
import skimage.measure as sims

import skl_graph.type.topology_map as tgmp
from skl_graph.standard.identifier import COORDINATE_SEPARATOR, EncodedNumber
from skl_graph.type.node import branch_node_t, end_node_t, node_t

array_t = nmpy.ndarray


_MAX_SQ_INTERPOLATION_ERROR = 0.8**2


class measures_t(named_tuple_t):
    """
    segment_: prefix for pixel-to-pixel segments
    segment_sq_lengths: squared segment lengths; Interest: all integers
    segment_based_area: width-weighted length
    """

    length: float
    segment_lengths: array_t
    segment_sq_lengths: array_t
    mean_width: float
    mean_based_area: float | None
    segment_based_area: float | None


@dtcl.dataclass(slots=True, repr=False, eq=False)
class raw_edge_t:
    sites: tuple[array_t, ...]

    @classmethod
    def NewWithSites(cls, sites: tuple[array_t, ...], /) -> raw_edge_t:
        """"""
        return cls(sites=_ReOrderedSites(sites))

    @property
    def dim(self) -> int:
        """"""
        return self.sites.__len__()

    @property
    def n_sites(self) -> int:
        """
        Cannot be less than 2 since even an edge between an end node and a touching branch node will contain the end
        node pixel and one branch node pixel.
        """
        return self.sites[0].size

    def __str__(self) -> str:
        """"""
        return (
            f"{self.__class__.__name__}:\n" f"    Sites[{self.dim}-D]: {self.n_sites}"
        )


@dtcl.dataclass(slots=True, repr=False, eq=False)
class edge_t(raw_edge_t):
    uid: str = None
    widths: array_t = None
    measures: measures_t = None
    properties: dict[Any, Any] = dtcl.field(init=False, default_factory=dict)
    _cache: dict[str, Any] = dtcl.field(default_factory=dict)

    @classmethod
    def NewWithDetails(
        cls,
        sites: tuple[array_t, ...],
        adjacent_node_uids: Sequence[str],
        /,
        *,
        width_map: array_t = None,
    ) -> edge_t:
        """"""
        raw_edge = raw_edge_t.NewWithSites(sites)
        transient = _transient_t.NewFromRaw(raw_edge)

        transient.SetUID(adjacent_node_uids)
        transient.SetWidths(width_map)
        transient.ComputeMeasures()

        return transient.AsEdge()

    def SetProperty(self, name: str, /, *, value: Any = None):
        """"""
        self.properties[name] = value

    @property
    def arc_lengths(self) -> array_t:
        """"""
        output = nmpy.cumsum([0.0] + list(self.measures.segment_lengths))
        output[-1] = self.measures.length  # To correct round-off errors
        assert output[-1] > output[-2]  # To check above correction was not invalid

        return output

    def AsCurve(self) -> spnt.PchipInterpolator | None:
        """"""
        cache_entry = self.AsCurve.__name__

        if cache_entry not in self._cache:
            if self.n_sites > 3:
                self._cache[cache_entry] = _PchipInterpolator(
                    self.arc_lengths, nmpy.array(self.sites)
                )
            else:
                self._cache[cache_entry] = None

        return self._cache[cache_entry]

    def InitialDirection(self) -> array_t:
        """"""
        return self._Direction(self.InitialDirection)

    def FinalDirection(self) -> array_t:
        """"""
        return self._Direction(self.FinalDirection)

    def Directions(self) -> tuple[array_t, array_t, array_t]:
        """"""
        cache_entry = self.Directions.__name__

        if cache_entry not in self._cache:
            as_curve = self.AsCurve()
            if as_curve is None:
                if self.n_sites > 1:
                    sites_as_array = nmpy.array(self.sites)
                    derivatives = nmpy.diff(sites_as_array, axis=1).astype(nmpy.float64)
                    norms = nmpy.linalg.norm(derivatives, axis=0, keepdims=True)
                    derivatives /= norms
                    last = derivatives[:, -1][:, None]
                    self._cache[cache_entry] = (
                        sites_as_array,
                        self.arc_lengths,
                        nmpy.hstack((derivatives, last)),
                    )
                else:
                    raise RuntimeError("Should never happen. Please contact developer.")
            else:
                arc_lengths = as_curve.x
                sites, derivatives = (as_curve(arc_lengths, _rdr) for _rdr in (0, 1))
                norms = nmpy.linalg.norm(derivatives, axis=0, keepdims=True)
                self._cache[cache_entry] = (sites, arc_lengths, derivatives / norms)

        return self._cache[cache_entry]

    def DirectionChanges(self) -> array_t:
        """
        2-D: determinant of consecutive directions, normalized by arc length differences.
        3-D: "signed" norm of the cross product of consecutive directions, normalized by arc length differences.
        """
        cache_entry = self.DirectionChanges.__name__

        if cache_entry not in self._cache:
            if self.dim == 2:
                Determinant = lambda _vct, _ref: (nmpy.linalg.det(_vct), _ref)
            else:
                Determinant = _SignedCrossProductNorm

            _, arc_lengths, directions = self.Directions()
            determinants = nmpy.empty((directions.shape[1] - 1), dtype=nmpy.float64)
            reference = None
            for c_idx in range(directions.shape[1] - 1):
                determinants[c_idx], reference = Determinant(
                    directions[:, c_idx : (c_idx + 2)], reference
                )
            determinants /= arc_lengths[1:]

            self._cache[cache_entry] = determinants

        return self._cache[cache_entry]

    def Tortuosity(self) -> float:
        """
        https://en.wikipedia.org/wiki/Tortuosity
        """
        chord_length = nmpy.linalg.norm(self.sites[0] - self.sites[-1])
        return self.measures.length / chord_length

    def _InnerSegments(self) -> tuple[tuple[int, ...], tuple[int, ...]]:
        """"""
        dim_range = tuple(range(self.dim))
        first_inner = tuple(
            self.sites[_idx][1] - self.sites[_idx][0] for _idx in dim_range
        )
        last_inner = tuple(
            self.sites[_idx][-2] - self.sites[_idx][-1] for _idx in dim_range
        )

        return first_inner, last_inner

    def _Direction(self, caller: MethodType, /) -> array_t:
        """"""
        cache_entry = caller.__name__
        if cache_entry not in self._cache:
            cache_entry_i = self.InitialDirection.__name__
            cache_entry_f = self.FinalDirection.__name__

            as_curve = self.AsCurve()
            if as_curve is None:
                if self.n_sites > 1:
                    first_inner, last_inner = self._InnerSegments()
                    self._cache[cache_entry_i] = nmpy.array(
                        first_inner
                    ) / nmpy.linalg.norm(first_inner)
                    self._cache[cache_entry_f] = nmpy.array(
                        last_inner
                    ) / nmpy.linalg.norm(last_inner)
                else:
                    raise RuntimeError("Should never happen. Please contact developer.")
            else:
                first_inner, last_inner = self._InnerSegments()
                max_arc_length = as_curve.x.item(-1)
                derivatives = as_curve((0, max_arc_length), 1)
                initial = derivatives[:, 0]
                final = derivatives[:, 1]
                flips = [1.0, 1.0]
                for p_idx, product in enumerate(
                    (nmpy.dot(initial, first_inner), nmpy.dot(final, last_inner))
                ):
                    if product < 0.0:
                        flips[p_idx] = -1.0
                self._cache[cache_entry_i] = initial / (
                    flips[0] * nmpy.linalg.norm(initial)
                )
                self._cache[cache_entry_f] = final / (
                    flips[1] * nmpy.linalg.norm(final)
                )

        return self._cache[cache_entry]

    def __str__(self) -> str:
        """
        Does not call raw_edge_t.__str__ since raw edges do not have UID
        """
        origin = tuple(self.sites[_idx][0] for _idx in range(self.dim))
        if self.measures is None:
            raw_length = "Not computed yet"
            segment_based_area = raw_length
        else:
            raw_length = round(self.measures.length, 2)
            segment_based_area = round(self.measures.segment_based_area, 2)

        main = (
            f"{self.__class__.__name__}.{self.uid}:\n"
            f"    Sites[{self.dim}-D]: {self.n_sites}\n"
            f"    Origin:              {origin}\n"
            f"    Lengths:             Raw={raw_length}, SB-Area={segment_based_area}"
        )

        if (self._cache is None) or (self._cache.__len__() == 0):
            cached_values = "None yet"
        else:
            cached_values = ", ".join(self._cache.keys())

        return main + f"\n    Cached values: {cached_values}"


@dtcl.dataclass(slots=True, repr=False, eq=False)
class _transient_t(raw_edge_t):
    uid: str = None
    widths: array_t = None
    measures: measures_t = None

    @classmethod
    def NewFromRaw(cls, raw_edge: raw_edge_t, /) -> _transient_t:
        """"""
        return cls(**dtcl.asdict(raw_edge))

    def AsEdge(self) -> edge_t:
        """"""
        return edge_t(**dtcl.asdict(self))

    def SetUID(self, adjacent_node_uids: Sequence[str], /) -> None:
        """"""
        if adjacent_node_uids.__len__() != 2:
            raise RuntimeError(
                f"{adjacent_node_uids.__len__()}: Incorrect number of adjacent node uids"
            )

        node_uid_0, node_uid_1 = adjacent_node_uids
        if node_uid_0 > node_uid_1:
            node_uid_0, node_uid_1 = node_uid_1, node_uid_0

        uid_components = [
            EncodedNumber(coord) for coord in node_uid_0.split(COORDINATE_SEPARATOR)
        ]
        uid_components.append(COORDINATE_SEPARATOR)
        uid_components.extend(
            EncodedNumber(coord) for coord in node_uid_1.split(COORDINATE_SEPARATOR)
        )

        self.uid = "".join(uid_components)

    def SetWidths(self, width_map: array_t, /) -> None:
        """"""
        if width_map is not None:
            self.widths = width_map[self.sites]

    def ComputeMeasures(self) -> None:
        """
        Must not be called before SetWidths
        """
        sites_as_array = nmpy.array(self.sites)
        segments = nmpy.diff(sites_as_array, axis=1)
        segment_sq_lengths = nmpy.sum(segments**2, axis=0)
        segment_lengths = nmpy.sqrt(segment_sq_lengths)
        length = segment_lengths.sum().item()

        if self.widths is None:
            mean_width = mean_based_area = segment_based_area = 0.0
        else:
            mean_width = nmpy.mean(self.widths).item()
            mean_based_area = length * mean_width
            segment_based_area = (
                (0.5 * (self.widths[1:] + self.widths[:-1]) * segment_lengths)
                .sum()
                .item()
            )

        self.measures = measures_t(
            length=length,
            segment_lengths=segment_lengths,
            segment_sq_lengths=segment_sq_lengths,
            mean_width=mean_width,
            mean_based_area=mean_based_area,
            segment_based_area=segment_based_area,
        )

    def AppendBranchNode(
        self,
        b_coords: array_t,
        node: node_t,
        adjacent_node_uids: list[str],
        /,
        *,
        force_after: bool = False,
    ) -> None:
        """"""
        adjacent_node_uids.append(node.uid)

        space_dim = self.dim
        first_site = tuple(self.sites[idx_][0] for idx_ in range(space_dim))
        sq_distance = (nmpy.subtract(first_site, b_coords) ** 2).sum()

        if self.n_sites > 1:
            # 0 <: so that if the edge is a self-loop ending at the same site, it does not put twice the site in a row
            if 0 < sq_distance <= space_dim:
                self.sites = tuple(
                    nmpy.hstack((b_coords[idx_], self.sites[idx_]))
                    for idx_ in range(space_dim)
                )
            else:
                self.sites = tuple(
                    nmpy.hstack((self.sites[idx_], b_coords[idx_]))
                    for idx_ in range(space_dim)
                )
        elif force_after:
            self.sites = tuple(
                nmpy.hstack((self.sites[idx_], b_coords[idx_]))
                for idx_ in range(space_dim)
            )
        else:
            self.sites = tuple(
                nmpy.hstack((b_coords[idx_], self.sites[idx_]))
                for idx_ in range(space_dim)
            )


def RawEdges(
    skl_map: array_t, b_node_lmap: array_t, /
) -> tuple[Sequence[raw_edge_t], array_t]:
    """"""
    edge_map = skl_map.astype(nmpy.int8)
    edge_map[b_node_lmap > 0] = 0
    edge_lmap, n_edges = tgmp.LABELING_FCT_FOR_DIM[skl_map.ndim](edge_map)

    edge_props = sims.regionprops(edge_lmap)

    edges: list[raw_edge_t] = n_edges * [None]
    for props in edge_props:
        sites = props.image.nonzero()
        for d_idx in range(skl_map.ndim):
            sites[d_idx].__iadd__(props.bbox[d_idx])
        edges[props.label - 1] = raw_edge_t.NewWithSites(sites)

    return edges, edge_lmap


def EdgesFromRawEdges(
    raw_edges: Sequence[raw_edge_t],
    e_nodes: Sequence[end_node_t],
    b_nodes: Sequence[branch_node_t],
    edge_lmap: array_t,
    e_node_lmap: array_t,
    b_node_lmap: array_t,
    /,
    *,
    width_map: array_t = None,
) -> tuple[tuple[edge_t], list[list[str]]]:
    """"""
    edge_tmap = tgmp.TopologyMapOfMap(edge_lmap > 0)
    transient_edges = [_transient_t.NewFromRaw(_raw) for _raw in raw_edges]

    # ep=edge end point; Keep < 2 since ==0 (length-1 edges) and ==1 (other edges) are needed
    # Do not use list multiplication since the same list then used for all the elements
    node_uids_per_edge: list[list[str]] = [[] for _ in transient_edges]
    for ep_coords in zip(*(edge_tmap < 2).nonzero()):
        edge_idx = edge_lmap[ep_coords] - 1
        transient = transient_edges[edge_idx]
        e_node_label = e_node_lmap[ep_coords]

        if e_node_label > 0:
            # End node-to-X edge (i.e., edge end point is also an end node)
            node_uids_per_edge[edge_idx].append(e_nodes[e_node_label - 1].uid)
            if transient.n_sites == 1:
                # End node-to-branch node edge (and there is a unique non-zero value in b_neighborhood)
                nh_slices_starts, b_neighborhood = _LMapNeighborhood(
                    b_node_lmap, ep_coords
                )
                b_node_label = nmpy.amax(b_neighborhood)
                b_coords = nmpy.transpose((b_neighborhood == b_node_label).nonzero())[0]
                transient.AppendBranchNode(
                    nmpy.add(nh_slices_starts, b_coords),
                    b_nodes[b_node_label - 1],
                    node_uids_per_edge[edge_idx],
                )
        else:
            nh_slices_starts, b_neighborhood = _LMapNeighborhood(b_node_lmap, ep_coords)
            force_after = False
            # Looping only for length-1, b-to-b edges
            for b_coords in zip(*b_neighborhood.nonzero()):
                b_node_label = b_neighborhood[b_coords]
                transient.AppendBranchNode(
                    nmpy.add(nh_slices_starts, b_coords),
                    b_nodes[b_node_label - 1],
                    node_uids_per_edge[edge_idx],
                    force_after=force_after,
                )
                force_after = not force_after

    for transient, adjacent_node_uids in zip(transient_edges, node_uids_per_edge):
        # Fix sites order for self-loops connected to branch nodes
        if adjacent_node_uids[0] == adjacent_node_uids[1]:
            node = None
            for current in b_nodes:
                if current.uid == adjacent_node_uids[0]:
                    node = current
                    break
            if node is not None:
                node_sites = nmpy.array(node.sites)
                edge_sites = nmpy.array(transient.sites)
                while not all(
                    any(
                        nmpy.all(
                            (node_sites - edge_sites[:, _sdx][:, None]) == 0, axis=0
                        )
                    )
                    for _sdx in (0, -1)
                ):
                    edge_sites = nmpy.roll(edge_sites, -1, axis=1)

                transient.sites = tuple(
                    edge_sites[_cdx, :] for _cdx in range(transient.dim)
                )

        transient.SetUID(adjacent_node_uids)
        transient.SetWidths(width_map)
        transient.ComputeMeasures()

    edges = tuple(_tst.AsEdge() for _tst in transient_edges)

    return edges, node_uids_per_edge


def _ReOrderedSites(sites: tuple[array_t, ...], /) -> tuple[array_t, ...]:
    """
    If the number of sites is 1 or 2, the input argument is returned (i.e., no copy is made).
    """
    n_sites = sites[0].size
    if n_sites < 3:
        return sites

    dim = sites.__len__()

    self_loop = all(sites[idx][0] == sites[idx][-1] for idx in range(dim))
    if self_loop:
        sites = tuple(sites[idx][:-1] for idx in range(dim))
        n_sites -= 1
        self_origin = nmpy.fromiter(
            (sites[idx][0] for idx in range(dim)), dtype=sites[0].dtype
        )
        self_origin = nmpy.reshape(self_origin, (1, dim))
    else:
        self_origin = None

    sites_as_array = nmpy.transpose(nmpy.array(sites))
    reordered_coords = [nmpy.array([sites[idx][0] for idx in range(sites.__len__())])]
    unvisited_slc = nmpy.ones(n_sites, dtype=nmpy.bool_)
    unvisited_slc[0] = False
    unvisited_sites = None
    end_point = None
    pre_done = False
    post_done = False

    while unvisited_slc.any():
        if post_done:
            neighbor_idc = ()
        else:
            end_point = reordered_coords[-1]
            neighbor_idc, unvisited_sites = _NeighborIndices(
                dim, sites_as_array, unvisited_slc, end_point
            )

        if (neighbor_idc.__len__() == 1) or post_done:
            also_grow_first = (reordered_coords.__len__() > 1) and not pre_done
            if not post_done:
                c_idx = neighbor_idc[0]
                reordered_coords.append(unvisited_sites[c_idx, :])
                unvisited_slc[nmpy.where(unvisited_slc)[0][c_idx]] = False
            if also_grow_first:
                end_point = reordered_coords[0]
                neighbor_idc, unvisited_sites = _NeighborIndices(
                    dim, sites_as_array, unvisited_slc, end_point
                )
                if neighbor_idc.__len__() == 1:
                    c_idx = neighbor_idc[0]
                    reordered_coords = [unvisited_sites[c_idx, :]] + reordered_coords
                    unvisited_slc[nmpy.where(unvisited_slc)[0][c_idx]] = False
                elif neighbor_idc.__len__() == 0:
                    pre_done = True  # End point has been reached
                else:
                    raise RuntimeError(
                        f"{neighbor_idc.__len__()} neighbors when only 1 is expected\n"
                        f"{sites}\n{reordered_coords}\n{unvisited_slc}\n{end_point}"
                    )
        elif neighbor_idc.__len__() == 2:
            if reordered_coords.__len__() == 1:
                idx1, idx2 = neighbor_idc
                reordered_coords = [unvisited_sites[idx1, :]] + reordered_coords
                reordered_coords.append(unvisited_sites[idx2, :])
                true_map = nmpy.where(unvisited_slc)[0]
                unvisited_slc[true_map[idx1]] = False
                unvisited_slc[true_map[idx2]] = False
            else:
                raise RuntimeError(
                    f"2 neighbors when only 1 is expected\n"
                    f"{sites}\n{reordered_coords}\n{unvisited_slc}\n{end_point}"
                )
        elif neighbor_idc.__len__() == 0:
            post_done = True  # End point has been reached
        else:
            raise RuntimeError(
                f"{neighbor_idc.__len__()} neighbors when only 1 or 2 are expected\n"
                f"{sites}\n{reordered_coords}\n{unvisited_slc}\n{end_point}"
            )

    reordered_coords = nmpy.array(reordered_coords)
    if self_loop:
        reordered_coords = _RolledSitesWithFixedOrigin(reordered_coords, self_origin)
    reordered_coords = tuple(reordered_coords[:, _idx] for _idx in range(dim))

    return reordered_coords


def _NeighborIndices(
    dim: int, sites: array_t, unvisited_slc: array_t, end_point: array_t
) -> tuple[array_t, array_t]:
    """"""
    unvisited_sites = sites[unvisited_slc, :]

    distances = nmpy.fabs(unvisited_sites - nmpy.reshape(end_point, (1, dim)))
    neighbor_idc = nmpy.nonzero(nmpy.all(distances <= 1, axis=1))[0]

    return neighbor_idc, unvisited_sites


def _RolledSitesWithFixedOrigin(sites: array_t, origin: array_t, /) -> array_t:
    """"""
    self_origin_idx = nmpy.argwhere(nmpy.all(sites == origin, axis=1)).item()
    if self_origin_idx > 0:
        sites = nmpy.roll(sites, -self_origin_idx, axis=0)

    return nmpy.vstack((sites, origin))


def _LMapNeighborhood(lmap: array_t, site: tuple[int, ...]) -> tuple[array_t, array_t]:
    """"""
    slices_starts = tuple(max(site[idx_] - 1, 0) for idx_ in range(site.__len__()))
    slices = tuple(
        slice(slices_starts[idx_], min(site[idx_] + 2, lmap.shape[idx_]))
        for idx_ in range(site.__len__())
    )
    neighborhood = lmap[slices]

    return nmpy.array(slices_starts, dtype=nmpy.int64), neighborhood


def _PchipInterpolator(
    arc_lengths: array_t, sites: array_t, /
) -> spnt.PchipInterpolator:
    """"""
    for n_samples in range(2, arc_lengths.size + 1):
        arc_length_samples = nmpy.linspace(0, arc_lengths.size - 1, num=n_samples)
        indices = nmpy.unique(nmpy.around(arc_length_samples)).astype(nmpy.uint64)
        output = spnt.PchipInterpolator(
            arc_lengths[indices], sites[:, indices], axis=1, extrapolate=False
        )

        error = max(nmpy.sum((output(arc_lengths) - sites) ** 2, axis=0))
        if error <= _MAX_SQ_INTERPOLATION_ERROR:
            return output

    raise RuntimeError("Should never happen. Please contact developer.")


def _SignedCrossProductNorm(
    vectors: array_t, reference: array_t | None, /
) -> tuple[float, array_t]:
    """"""
    product = nmpy.cross(vectors[:, 0], vectors[:, 1])
    if reference is None:
        reference = product
        sign = 1.0
    else:
        sign = nmpy.dot(product, reference)

    return (sign * nmpy.linalg.norm(product)).item(), reference
