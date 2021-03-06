import argparse
import os
import numpy as np
from scipy import io, sparse
from scipy.sparse import linalg
import main

def matrix_power(mtx, exp):
    """ Return the exp power of (mtx + I) """
    I = sparse.identity(mtx.shape[1], dtype=float, format='csr')
    A = mtx + I
    for i in xrange(int(exp)-1):
        A = A.dot(mtx + I)

    return A

def walk_generator(A):
    """ Return the walk-generating function of A. """
    I = sparse.identity(A.shape[1], dtype=float)
    inv_mat = linalg.inv((I-A).tocsc()).tocsr()
    return inv_mat

def exponentiate(mat):
    """ Return the matrix exponential of A, exp(A). """
    exp_mat = linalg.expm(mat.tocsc()).tocsr()
    return exp_mat

def reciprocal_ties(mat):
    """ Symmetrize A considering reciprocal ties. """
    A = mat.todok()
    B = sparse.dok_matrix(A.shape)
    for (i, j), aij in A.iteritems():
        if (j,i) in A:
            val = aij + A[j, i]
            B[i, j] = val
            B[j, i] = val
    
    return B.tocsr()

def symmetrize(mat):
    """ Symmetrize by taking the mean of the aij and aji entries """
    return (mat + mat.T)/2

def extract_largest_component(mat):
    """ Extract the largest component using scipy's method """
    num_comp, affiliation = sparse.csgraph.connected_components(mat)
    if num_comp == 1:
        return mat
    max_comp = np.argmax(np.bincount(affiliation))
    indices = np.arange(mat.shape[0])
    indices = indices[affiliation == max_comp]

    return mat[indices, :][:, indices]

def edge_restriction(restrictee, restrictor):
    indptr = restrictor.indptr
    indices = restrictor.indices
    nz = restrictor.nonzero()
    data = np.array(restrictee[nz[0], nz[1]], dtype=float)[0]
    return sparse.csr_matrix((data, indices, indptr), dtype=float)


def power_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_input",
                        help="Specify the path of the input data set")
    parser.add_argument("-p", "--power", type=int,
                        help="Specify to which power to raise the matrix to")
    parser.add_argument("-w", "--walk", help="Calculate (I-A)^-1",
                        action="store_true")
    parser.add_argument("-e", "--exp", help="Calculate exp(A)",
                        action="store_true")
    parser.add_argument("-r", "--restrict", 
                        help="Restrict the elements of the "
                        "transformed matrix to the coordinates of the nonzero "
                        "elements of the original matrix.",
                        action="store_true")
    parser.add_argument("--recip", action="store_true", 
                        help="Symmetrize by reciprocal ties")
    parser.add_argument("--symmetrize", action="store_true", 
                        help="Symmetrize by the mean of entry ij and ji")
    parser.add_argument("-lcc", "--components", action="store_true", 
                        help="Extract the largest connected component")
    parser.add_argument("path_to_output", \
        help="Specify where to save output")

    args = parser.parse_args()
    in_path = args.path_to_input
    out_path = args.path_to_output
    if os.path.isfile(in_path):
        filename, ending = os.path.splitext(in_path)
        out_path, out_ending = os.path.splitext(out_path)
        try:
            A = main.get_graph(in_path)
        except IOError:
            print("File format not recognized")
        else:
            if args.power:
                mat = matrix_power(A, args.power)
            elif args.walk:
                mat = walk_generator(A)
            elif args.exp:
                mat = exponentiate(A)
            else:
                mat = A

            if args.recip:
                mat = reciprocal_ties(mat)
            elif args.symmetrize:
                mat = symmetrize(mat)
            
            if args.components:
                mat = extract_largest_component(mat)

            if args.restrict:
                mat = edge_restriction(mat, A)

            if out_path:
                io.savemat(out_path, {'mat': mat}, do_compression=True,
                           oned_as='row')
    else:
        print("Specify a valid input-file")

if __name__ ==  '__main__':
    power_main()