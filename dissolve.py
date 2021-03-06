import modularity as mod
import functions as fns
# from louvain import louvain

def community_dissolve(G, C, init_q, tsh):
    """
    Run first the first phase of Louvain(with a bit modified notation),
    then run dissolve once. 

    """
    luv_q = luvxdiss(G, C, init_q, tsh)
    dis_q = dissolve(G, C, luv_q)
    return dis_q

def luvxdiss(G, C, init_q, tsh):
    """
    Find the communities of the graph represented by A using the Louvain
    method.

    Args:
    A: Adjacency matrix in CSR format
    m: 0.5 * A.sum()
    n: A.shape[1] the number of vertices in the graph
    k: degree sequence
    args: flags and objects for data export etc.

    """
    n = G.n
    k = G.k
    mod_gain = mod.modularity_gain_new_notation
    move = C.move
    new_q = init_q 
    
    while True:
        old_q = new_q
        no_moves = set(C.communities.keys())
        for i in fns.yield_random_modulo(n):
            (c, movein, moveout) = mod_gain(G, C, i)
            gain = movein - moveout + 2*C.node_mods[i]
            if gain > 0:
                no_moves.discard(c)
                move(i, c, k[i], movein, moveout, C.node_mods[i])
                new_q += gain
 
        if new_q - old_q < tsh:
            break
    return new_q

def dissolve(G, C, init_q):
    """
    Extracts the community with the lowest modularity and tries to
    'dissolve' it (move all vertices) repeatedly. When all communities
    have been considered it is finished.

    Args:
    G: Graph named tuple
    C: Community structure
    init_q: the initial modularity

    Returns:
    q: the modularity of the network after a round of dissolve

    """
    def move(i, dest):
        """ Move vertex i to dest in our community object """
        if dest != -1:
            C.move(i, dest, k[i], movein[i],
                   moveout[i], quv[dest])
        else:
            C.move(i, dest, k[i], movein[i],
                   moveout[i], C.node_mods[i])
        quv[dest] = 0.00 # Only add this the first time.

    k = G.k
    q = init_q

    while True:
        c, (seen, q_c) = C.pop()

        if seen:
            return C.network_modularity

        (node2c, c2node, movein,
         moveout, quv, best) = mod.mass_modularity(G, C, C[c], c)

        if sum(movein.values()) + sum(quv.values()) > q_c:
            for dest, nodes in c2node.iteritems():
                for i in nodes:
                    move(i, dest)

    return q