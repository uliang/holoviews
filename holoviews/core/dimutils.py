"""
Advanced utilities for working with Dimensioned objects.
"""

from .dimension import Dimension

def get_by_idxs(idxs):
    return lambda x: tuple(x[idx] for idx in idxs)

def create_ndkey(length, indexes, values):
    key = [None] * length
    for i, v in zip(indexes, values):
        key[i] = v
    return tuple(key)

def uniform(obj):
    """
    Finds all common dimension keys in the object
    including subsets of dimensions. If there are
    is no common subset of dimensions, None is
    returned.
    """
    dim_groups = obj.traverse(lambda x: tuple(x.key_dimensions),
                              ('HoloMap',))
    if dim_groups:
        return all(set(g1) <= set(g2) or set(g1) >= set(g2)
                   for g1 in dim_groups for g2 in dim_groups)
    return True


def unique_dimkeys(obj):
    """
    Finds all common dimension keys in the object
    including subsets of dimensions. If there are
    is no common subset of dimensions, None is
    returned.
    """
    key_dims = obj.traverse(lambda x: (tuple(x.key_dimensions),
                                       (x.data.keys())), ('HoloMap',))
    if not key_dims:
        return [Dimension('Frame')], [(0,)]
    dim_groups, keys = zip(*sorted(key_dims, lambda d, k: len(d)))
    subset = all(set(g1) <= set(g2) or set(g1) >= set(g2)
               for g1 in dim_groups for g2 in dim_groups)
    # Find unique keys
    all_dims = list({dim for dim_group in dim_groups
                     for dim in dim_group})
    ndims = len(all_dims)
    unique_keys = []
    for group, keys in key_dims:
        dim_idxs = [all_dims.index(dim) for dim in group]
        for k in keys:
            matches = [item for item in unique_keys
                       if k == get_by_idxs(dim_idxs)(item)]
            if not matches:
                unique_keys.append(create_ndkey(ndims, dim_idxs, k))
    if subset:
        return all_dims, unique_keys
    else:
        return ['Frames'], [i for i in range(len(unique_keys))]

