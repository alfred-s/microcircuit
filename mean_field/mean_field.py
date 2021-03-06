"""mean_field.py

Imports mf_class as model and mf_plot.

Numerical analysis of the equations corresponding to the 
stationary solutions of the mean field approximation of the 
cortical microcircuit model. 

8 coupled integral equations are solved numerically. 
"""
from __future__ import print_function
from imp import reload
import numpy as np
from scipy.optimize import root
import time
import mf_class as model; reload(model)
import mf_plot; reload(mf_plot)
plotting = True
iterate_g = True                # iterate g for fixed v_ext
iterate_v_ext = False           # iterate v_ext for fixed g

# Global parameters
choose_model = "micro"  # brunelA, brunelB for corresponding models!
n_layer = 4
n_types = 2
n_pop = n_layer * n_types
print("Model: ", choose_model)
print("n layers: ", n_layer)
# Create reference instance containing parameters and functions:
# (used mostly for plotting)
mf_net0  = model.mf_net(choose_model=choose_model, n_layer=n_layer)
plot_pops= mf_net0.populations[:2]    # These populations are plotted
if not type(plot_pops) == np.ndarray:
    plot_pops = np.array([plot_pops])

raise Exception
######################################################
# Functions
######################################################

def v0_g(v_exts, gs, jacobian=False, root_method=None, options=None):
    """Iterate over g for fixed v_ext (fig. 1 B.1)
    Returns v0s[v_ext, g, population]
    """
    print("Iterate over g")
    v0s = np.zeros([len(v_exts), len(gs), n_pop])
    #print("g\tv_ext\tv0\t\td(v0)")
    for i, v_ext_factor in enumerate(v_exts):
        v_guess = np.array([2.]*n_pop)  # initial guess
        for j, g in enumerate(gs):
            # create instance of class:
            mf_net = model.mf_net(choose_model=choose_model, n_layer=n_layer, 
                g=g, v_ext_factor=v_ext_factor)
            if jacobian:
                jac = mf_net.jacobian
            else:
                jac = False
            try:
                sol = root(mf_net.root_v0, v_guess, jac=jac, method=root_method, options=options)
                if sol["success"]:
                    v0  = sol["x"]
                    d   = np.linalg.norm(mf_net.root_v0(v0))
                    v0s[i, j] = v0
                    v_guess = v0
                else:
                    v0s[i, j] = -1
            except:
                v0s[i, j] = -2
    return v0s

def v0_v_ext(v_exts, gs, jacobian=False, root_method=None, options=None):
    """Iterate over v_ext for fixed g (fig. 1 B.2)
    Returns v0s[g, v_ext, population]
    """
    print("Iterate over v_ext")
    v0s = np.zeros([len(gs), len(v_exts), n_pop])
    #print("g\tv_ext\tv0\t\td(v0)")
    for i, g in enumerate(gs):
        v_guess = np.array([2.]*n_pop)  # initial guess
        for j, v_ext_factor in enumerate(v_exts):
            # create instance of class:
            mf_net = model.mf_net(choose_model=choose_model, n_layer=n_layer, 
                g=g, v_ext_factor=v_ext_factor)
            if jacobian:
                jac = mf_net.jacobian
            else:
                jac = False
            try:
                sol = root(mf_net.root_v0, v_guess, jac=jac, method=root_method, options=options)
                if sol["success"]:
                    v0  = sol["x"]
                    d   = np.linalg.norm(mf_net.root_v0(v0))
                    v0s[i, j] = v0
                    v_guess = v0
                else:
                    v0s[i, j] = -1
            except:
                v0s[i, j] = -2
    return v0s
    
######################################################
# Solving
######################################################

# v_0 over g (fig. 1 B.1)
jacobian        = False     # whether to use calculated jacobian
root_method     = ['hybr', 'lm', 'broyden1', 'anderson', 'krylov'][0]
print("Method: ", root_method)
options         = None

def diagnostics(constants, v0s):
    failures        = np.sum(v0s[:, :, 0] == -1, axis=1)    # algorithm stopped unsuccessfull
    bad_failures    = np.sum(v0s[:, :, 0] == -2, axis=1)    # algorithm yielded NaN/overflow
    total_failures  = np.sum(v0s[:, :, 0] > 1. / mf_net0.t_ref, axis=1)    
        # converged unphysically (v0 > 1/t_ref)
    successes       = np.sum(v0s[:, :, 0] >=  0, axis=1) - total_failures
    for const, succ, fail, bad_fail, total_fail in zip(\
        constants, successes, failures, bad_failures, total_failures):
        print("%.1f\t%i\t%i\t%i"%(const, succ, fail, bad_fail))

if iterate_g:
    v_exts_g    = np.array([1.1, 2., 4.])
    gs_g        = np.arange(8., 3.7, -0.1)
    #v_exts_g    = np.array([2.])
    #gs_g        = np.array([6.])

    t_int0      = time.time()
    v0s_g       = v0_g(v_exts_g, gs_g, jacobian, root_method, options)
    t_int1      = time.time() - t_int0
    print("Integration time: %.2f"%(t_int1))
    print("v_ext\t#succ.\t#fail\t#bad fail")
    diagnostics(v_exts_g, v0s_g)
    
if iterate_v_ext:
    gs_v        = np.array([4.5, 5, 6, 8])
    v_exts_v    = np.arange(4.0, 0.7, -0.1)

    t_int0      = time.time()
    v0s_v       = v0_v_ext(v_exts_v, gs_v, jacobian, root_method, options)
    t_int2      = time.time() - t_int0
    print("Integration time: %.2f"%(t_int2))
    print("g\t#succ.\t#fail\t#bad fail")
    diagnostics(v_exts_g, v0s_g)


######################################################
# Plotting
######################################################
if plotting:
    suptitle = "Mean field approach: model: " + choose_model + "; method: " + root_method
    plot = mf_plot.mf_plot(mf_net0, suptitle, plot_pops) 

    if iterate_g:
        plot.plot_v0_g_full(gs_g, v_exts_g, v0s_g)
    if iterate_v_ext:
        plot.plot_v0_v_ext(gs_v, v_exts_v, v0s_v)
    
    #vs0, lows0, ups0 = plot.plot_bounds()

    fig_name = 'mean_field_v0'
    #plot.fig.savefig(figure_path + fig_name + picture_format)
    plot.fig.show()

