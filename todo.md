Improvements:
- [x] implement louvain.make_C_matrix with a COO to make it much faster
- [x] store np.sum(k[c]) for all communities c.
- [ ] parallelize some calculation
- [x] initialize C with generator
- [ ] make new A directly?
- [x] Consider rewriting movein, moveout and get_max_gain to same f.
- [ ] Use numexpr instead of regular numpy
- [ ] Try with PYPU

Issues:
- [x] Absolute gain in modularity in louvain.py
- [x] map with lambda apparantly slower than list comprehension
- [x] gains are too high // modularity is not calculated right
- [x] should moveinmodularity include aii? NO