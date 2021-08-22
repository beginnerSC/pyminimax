import numpy as np
from itertools import combinations
from collections import defaultdict
from scipy.cluster.hierarchy import fcluster


# Part of this script is from scipy
# See _hierarchy.pyx and hierarchy.py in https://github.com/scipy/scipy/blob/master/scipy/cluster/
# The key step updating D matrix in the nn chain algorithm is changed to minimax

class LinkageUnionFind:
    """Structure for fast cluster labeling in unsorted dendrogram."""
#     cdef int[:] parent
#     cdef int[:] size
#     cdef int next_label

    def __init__(self, n):
        self.parent = np.arange(2 * n - 1)
        self.next_label = n
        self.size = np.ones(2 * n - 1)

    def merge(self, x, y):
        self.parent[x] = self.next_label
        self.parent[y] = self.next_label
        size = self.size[x] + self.size[y]
        self.size[self.next_label] = size
        self.next_label += 1
        return size

    def find(self, x):
        p = x

        while self.parent[x] != x:
            x = self.parent[x]

        while self.parent[p] != x:
            p, self.parent[p] = self.parent[p], x

        return x


def label(Z, n):
    """Correctly label clusters in unsorted dendrogram."""
    uf = LinkageUnionFind(n)
    for i in range(n - 1):
        x, y = int(Z[i, 0]), int(Z[i, 1])
        x_root, y_root = uf.find(x), uf.find(y)
        if x_root < y_root:
            Z[i, 0], Z[i, 1] = x_root, y_root
        else:
            Z[i, 0], Z[i, 1] = y_root, x_root
        Z[i, 3] = uf.merge(x_root, y_root)


def condensed_index(n, i, j):
    """
    Calculate the condensed index of element (i, j) in an n x n condensed
    matrix.
    """
    if i < j:
        return int(round(n * i - (i * (i + 1) / 2) + (j - i - 1)))
    elif i > j:
        return int(round(n * j - (j * (j + 1) / 2) + (i - j - 1)))


# def nn_chain(dists, n, method):
def minimax(dists, return_prototype=False):
    """Perform minimax-linkage clustering using nearest-neighbor chain algorithm. 
    
    Parameters
    ----------
    dists : ndarray
        The upper triangular of the distance matrix. The result of
        ``scipy.spatial.distance.pdist`` is returned in this form.
    
    return_prototype : bool, default False
        whether to return prototypes. 
        When this is False, the returned linkage matrix Z has 4 columns, structured the same 
        as the return value of the ``scipy.cluster.hierarchy.linkage`` function. 
        When this is True, the returned linkage matrix has a 5th column which contains 
        the indices of the prototypes corresponding to each merge. 
        
    Returns
    -------
    Z : ndarray
        A linkage matrix containing the hierarchical clustering. The first 4 columns has the 
        same structure as the return value of the ``scipy.cluster.hierarchy.linkage`` function. 
        See the documentation for more information on its structure. Depending on the value of 
        ``return_prototype`` there is an optional 5th columns. 
    """
    n = int((np.sqrt(8*len(dists) + 1) + 1)/2)

    Z_arr = np.empty((n - 1, 5))
    Z = Z_arr

    D = dists.copy()  # Distances between clusters.
    size = np.ones(n, dtype=np.intc)  # Sizes of clusters.

    indices = [set([i]) for i in range(n)]

#     new_dist = linkage_methods[method]

    # Variables to store neighbors chain.
    cluster_chain = np.ndarray(n, dtype=np.intc)
    chain_length = 0

#     cdef int i, j, k, x, y, nx, ny, ni
#     cdef double dist, current_min

    for k in range(n - 1):
        if chain_length == 0:
            chain_length = 1
            for i in range(n):
                if size[i] > 0:
                    cluster_chain[0] = i
                    break

        # Go through chain of neighbors until two mutual neighbors are found.
        while True:
            x = cluster_chain[chain_length - 1]

            # We want to prefer the previous element in the chain as the
            # minimum, to avoid potentially going in cycles.
            if chain_length > 1:
                y = cluster_chain[chain_length - 2]
                current_min = D[condensed_index(n, x, y)]
            else:
                current_min = np.inf   # NPY_INFINITYF

            for i in range(n):
                if size[i] == 0 or x == i:
                    continue

                dist = D[condensed_index(n, x, i)]
                if dist < current_min:
                    current_min = dist
                    y = i

            if chain_length > 1 and y == cluster_chain[chain_length - 2]:
                break

            cluster_chain[chain_length] = y
            chain_length += 1

        # Merge clusters x and y and pop them from stack.
        chain_length -= 2

        # This is a convention used in fastcluster.
        if x > y:
            x, y = y, x

        # get the original numbers of points in clusters x and y
        nx = size[x]
        ny = size[y]

        # merge x and y. Cluster x will be dropped, and y will be replaced with the new cluster
        indices[y] |= indices[x]
        indices[x] = set()

        prototype, minmax = min(((j, max(dists[condensed_index(n, j, k)] if j!=k else 0 for k in indices[y])) for j in indices[y]), key=lambda pt_max: pt_max[1])        
        
        # Record the new node.
        Z[k, 0] = x
        Z[k, 1] = y
        Z[k, 2] = current_min
        Z[k, 3] = nx + ny
        Z[k, 4] = prototype
        size[x] = 0  # Cluster x will be dropped.
        size[y] = nx + ny  # Cluster y will be replaced with the new cluster

        # Update the distance matrix.
        for i in range(n):
            ni = size[i]
            if ni == 0 or i == y:
                continue
                
            # D[condensed_index(n, i, y)] = max(D[condensed_index(n, i, x)], D[condensed_index(n, i, y)])  # complete linkage
            
            all_indices = indices[y] | indices[i]
            D[condensed_index(n, i, y)] = min(max(dists[condensed_index(n, j, k)] if j!=k else 0 for k in all_indices) for j in all_indices)

    # Sort Z by cluster distances.
    order = np.argsort(Z_arr[:, 2], kind='mergesort')
    Z_arr = Z_arr[order]

    # Find correct cluster labels inplace.
    label(Z_arr, n)
    
    if return_prototype:
        return Z_arr
    else: 
        return Z_arr[:, :4]
    

def _minimax_brute_force(dists, return_prototype=False):
    n = int((np.sqrt(8*len(dists) + 1) + 1)/2)

    def d(i, j): return dists[n*i+j-((i+2)*(i+1))//2] if i<j else (0 if i==j else d(j, i))
    def r(i, G): return max(d(i, j) for j in G)

    Z = np.empty((n-1, 5))
    clusters = {i: set([i]) for i in range(n)}
    for i in range(n-1):
        min_d = np.inf
        for (idxG, G), (idxH, H) in combinations(clusters.items(), 2):
            x, dminimax = min(((x, r(x, G|H)) for x in G|H), key=lambda pt_max_d: pt_max_d[1])
            if dminimax < min_d:
                min_d = dminimax
                to_merge = [idxG, idxH, dminimax, len(G|H), x]
        Z[i] = to_merge
        idxG, idxH, _, _, _ = to_merge
        clusters[n+i] = clusters.pop(idxG) | clusters.pop(idxH)
    
    if return_prototype:
        return Z
    else: 
        return Z[:, :4]
    
    
def fcluster_prototype(Z, t, criterion='inconsistent', depth=2, R=None, monocrit=None):
    """
    Form flat clusters from the hierarchical clustering defined by
    the given linkage matrix, and the 
    
    Parameters
    ----------
    Z : ndarray
        The hierarchical clustering encoded with the matrix returned
        by the `minimax` function.
    t : scalar
        For criteria 'inconsistent', 'distance' or 'monocrit',
         this is the threshold to apply when forming flat clusters.
        For 'maxclust' or 'maxclust_monocrit' criteria,
         this would be max number of clusters requested.
    criterion : str, optional
        The criterion to use in forming flat clusters. This can
        be any of the following values:
        
          ``inconsistent`` :
              If a cluster node and all its
              descendants have an inconsistent value less than or equal
              to `t`, then all its leaf descendants belong to the
              same flat cluster. When no non-singleton cluster meets
              this criterion, every node is assigned to its own
              cluster. (Default)
              
          ``distance`` :
              Forms flat clusters so that the original
              observations in each flat cluster have no greater a
              cophenetic distance than `t`.
              
          ``maxclust`` :
              Finds a minimum threshold ``r`` so that
              the cophenetic distance between any two original
              observations in the same flat cluster is no more than
              ``r`` and no more than `t` flat clusters are formed.
              
          ``monocrit`` :
              Forms a flat cluster from a cluster node c
              with index i when ``monocrit[j] <= t``.
              For example, to threshold on the maximum mean distance
              as computed in the inconsistency matrix R with a
              threshold of 0.8 do::
                  MR = maxRstat(Z, R, 3)
                  fcluster_prototype(Z, t=0.8, criterion='monocrit', monocrit=MR)
                  
          ``maxclust_monocrit`` :
              Forms a flat cluster from a
              non-singleton cluster node ``c`` when ``monocrit[i] <=
              r`` for all cluster indices ``i`` below and including
              ``c``. ``r`` is minimized such that no more than ``t``
              flat clusters are formed. monocrit must be
              monotonic. For example, to minimize the threshold t on
              maximum inconsistency values so that no more than 3 flat
              clusters are formed, do::
              
                  MI = maxinconsts(Z, R)
                  fcluster_prototype(Z, t=3, criterion='maxclust_monocrit', monocrit=MI)
    depth : int, optional
        The maximum depth to perform the inconsistency calculation.
        It has no meaning for the other criteria. Default is 2.
    R : ndarray, optional
        The inconsistency matrix to use for the 'inconsistent'
        criterion. This matrix is computed if not provided.
    monocrit : ndarray, optional
        An array of length n-1. `monocrit[i]` is the
        statistics upon which non-singleton i is thresholded. The
        monocrit vector must be monotonic, i.e., given a node c with
        index i, for all node indices j corresponding to nodes
        below c, ``monocrit[i] >= monocrit[j]``.
        
    Returns
    -------
    fcluster_prototype : ndarray
        An array of shape ``(n, 2)``. ``T[i]`` is the flat cluster number to
        which original observation ``i`` belongs, and the index of the prototype of this cluster.
    """
    fclust = fcluster(Z[:, :4], t=t, criterion=criterion, depth=depth, R=R, monocrit=monocrit)
    idx2clust = dict(enumerate(fclust))     # map from data point index to cluster
    n = len(fclust)

    clust_dict = defaultdict(set)           # map from cluster to set of indices
    for idx, clust in enumerate(fclust):
        clust_dict[clust].add(idx)

    protos = {}

    # if a cluster only contains one point, prototype must be that point, 
    # in which case update protos and remove all relevant data from idx2clust

    for cidx, cset in clust_dict.copy().items():
        if len(cset)==1:
            idx = cset.pop()
            protos[cidx] = idx
            idx2clust.pop(idx)
            clust_dict.pop(cidx)

    # if a cluster has multiple points, the prototype is in the coresponding 5th columns of Z of the lastly merged data point
    for x, y, _, _, proto in Z:
        if x < n and x in idx2clust:
            clust = idx2clust[x]
            clust_dict[clust].remove(x)
            if clust_dict[clust] == set([]):
                protos[clust] = proto
        if y < n and y in idx2clust:
            clust = idx2clust[y]
            clust_dict[clust].remove(y)
            if clust_dict[clust] == set([]):
                protos[clust] = proto
                
    return np.array([(clust, protos[clust]) for clust in fclust])
