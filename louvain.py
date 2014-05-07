import modularity as mod
import functions as fns

def louvain(A, m, n, k, C, init_q, tsh):
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

    calc_modularity = mod.calc_modularity
    move = C.move
    new_q = init_q 
    
    while True:
        old_q = new_q
        
        for i in fns.yield_random_modulo(n):
            indices = A.indices[A.indptr[i]:A.indptr[i+1]]
            data = A.data[A.indptr[i]:A.indptr[i+1]]
            (c, gain) = calc_modularity(data, indices, m, k, C, i)
            if gain > 0:
                move(i, c, k[i])
                new_q += gain

        if new_q - old_q < tsh:
            break

    return new_q
