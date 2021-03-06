"""mean_field.py

Numerical analysis of the equations corresponding to the 
stationary solutions of the mean field approximation of the 
cortical microcircuit model. 

8 coupled integral equations are solved numerically. 
"""
from __future__ import print_function
import numpy as np
from scipy.optimize import fsolve, root
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import cm
import time
import sys, os
sys.path.append(os.path.abspath("../")) # include path with style
import style
# Close other plots by adding "c" after "run <script>" 
if 'c' in sys.argv:
    plt.close('all')
picture_format = '.pdf'
figure_path = './'
plotting = True
# Import specific moduls
from mean_field_params import *
from mean_field_functions import *

######################################################
# Plotting
######################################################
colors = style.colors[:n_pop]
def mu2D(X,Y): 
    mu2D = np.tensordot(mat1[:,0], X, axes=0) + \
        np.tensordot(mat1[:,1], Y, axes=0) + \
        mu_ext.reshape(2, 1, 1)    
    return mu2D
def sd2D(X,Y): 
    sd2D = np.sqrt(np.tensordot(mat2[:,0], X, axes=0) +
        np.tensordot(mat2[:,1], Y, axes=0) + 
        var_ext.reshape(2, 1, 1))
    return sd2D

# Function to be solved
def integral(X, Y):
    n_x     = X.shape[0] * X.shape[1]
    mu_v    = mu2D(X, Y)
    sd_v    = sd2D(X, Y)
    low = (V_r - mu_v) / sd_v
    up  = (theta - mu_v) / sd_v
    integral = np.zeros([2, n_x])
    for i in range(2):
        lows_rs = low[i].reshape(n_x)
        ups_rs  = up[i].reshape(n_x)
        for j in range(n_x):
            integral[i, j] = quad(integrand, lows_rs[j], ups_rs[j])[0]
    return integral.reshape(2, *X.shape)

def func_2D(X, Y):
    s1  = -1./X + t_ref
    s2  = -1./Y + t_ref
    summand = np.array([s1, s2])
    return summand + tau_m * np.sqrt(np.pi) * integral(X, Y)

if plotting:
    fig = plt.figure()
    suptitle = "Mean field approach: model: " + choose_params 
    fig.suptitle(suptitle, y=0.98)
    # Mean
    ax0 = plt.subplot2grid((2, 2), (0, 0), colspan=1, rowspan=1, projection='3d')
    # SD
    ax1 = plt.subplot2grid((2, 2), (0, 1), colspan=1, rowspan=1) #projection='3d')
    # Lower and upper boundary
    ax2 = plt.subplot2grid((2, 2), (1, 0), colspan=1, rowspan=1) # , projection='3d')
    # Distance between lower and upper boundary
    ax3 = plt.subplot2grid((2, 2), (1, 1), colspan=1, rowspan=1, projection='3d')
    
    # Set up grids, variables, etc.
    v_min   = 2.0
    v_max   = 7.0
    v_min_y   = 2.0
    v_max_y   = 7.0
    v_plotx  = np.array([np.linspace(v_min, v_max, 20)])
    v_ploty  = np.array([np.linspace(v_min_y, v_max_y, 20)])
    X, Y    = np.meshgrid(v_plotx, v_ploty)
    mus = mu2D(X, Y)
    sds = sd2D(X, Y)
    lows= (V_r - mus) / sds
    ups = (theta - mus) / sds
    u_min   = np.min((V_r - mus) / sds)
    u_max   = np.max((theta - mus) / sds)
    u_min, u_max = (-2, 5)
    us  = np.linspace(u_min, u_max, 100) 
    
    t_int0 = time.time()
    func_0 = func_2D(X, Y)
    t_int = time.time() - t_int0
    print("Integration time: ", t_int)
    
    # Plotting everything
    cms = [cm.YlGnBu, cm.Reds]
    n_l = 2
    levels = np.linspace(-1, 1, n_l * 2 + 1)
    linestyles = ['solid'] * n_l + ['dashed'] + ['solid']*n_l 
    for i, population in enumerate(populations):
        '''ax0.plot_surface(X, Y, mus[i], color=colors[i], alpha=0.6, label=population, 
            rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax1.plot_surface(X, Y, sds[i], color=colors[i], alpha=0.6, label=population, 
            rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax0.plot_surface(X, Y, lows[i], color=colors[i], alpha=0.6, label=population, 
            rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax1.plot_surface(X, Y, ups[i] - lows[i], color=colors[i], alpha=0.6, label=population, 
            rstride=1, cstride=1, linewidth=0, antialiased=False)
        '''
        ax.plot_surface(X, Y, func_0[i], color=colors[i], alpha=0.6, label=population, 
            rstride=1, cstride=1, linewidth=0, antialiased=False)
        ax1.contour(X, Y, func_0[i], levels=levels, cmap=cms[i], linestyles=linestyles)
        cont = ax1.contour(X, Y, func_0[i], levels=levels, cmap=cms[i], linestyles=linestyles)
        #        , color=colors[i], alpha=0.6, label=population, 
        #    rstride=1, cstride=1, linewidth=0, antialiased=False)

    ax2.contour(X, Y, 0.1* func_0[0], levels=levels, cmap=cms[0], linestyles=linestyles)
    ax2.contour(X, Y, 1.*(func_0[0] - func_0[1]), levels=levels, cmap=cm.binary, linestyles=linestyles)
    # Set axes labels, etc.   
    for ax in fig.axes[:5]:
        ax.set_xlabel("$\\nu_E$ / Hz")
        ax.set_ylabel("$\\nu_I$ / Hz")
        ax.grid(False)
        ax.legend()
    '''ax0.set_zlabel("$\mu$")
    ax1.set_zlabel("$\sigma$")
    ax0.set_zlabel("Bounds: $\\frac{V_r - \mu(\\nu)}{\sigma(\\nu)}$;" +\
        "$\, \\frac{\\theta - \mu(\\nu)}{\sigma(\\nu)}$")
    ax1.set_zlabel("up($\\nu$) - low($\\nu$)")
    '''
    ax0.set_zlabel("Integral")
    ax0.set_zlim(-1, 1)
    for ax in fig.axes:
        style.fixticks(ax)

    fig_name = 'mean_field'
    #fig.savefig(figure_path + fig_name + picture_format)
    fig.show()

cv= get_contour_verts(cont)
cv0 = cv[2][0]
xs = cv0.T[0]
ys = cv0.T[1]
mu0 = mu2D(xs, ys)[0,0]
sd0 = sd2D(xs, ys)[0,0]

lower = lambda mu, sd: (V_r - mu) / sd
upper = lambda mu, sd: (theta - mu) / sd
