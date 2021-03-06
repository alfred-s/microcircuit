"""network_params.py

    Network parameters. 
    Based on network_params.sli (Potjans 2014)

    Contains:
    - network parameters
    - single-neuron parameters
    - stimulus parameters

Connection probabilities as well as mean values of synaptic weights and 
delays are implemented as numpy arrays with shape (n_pop, n_pop), where
n_pop = number of populations. Each layer contains neurons of all types. 

In order to introduce further types, all arrays have to be carefully adapted. 
However, the script running the simulation should not depend on these adaptations 
but work without further configuration (not yet tested).
"""
import numpy as np

###################################################
###     	Network parameters		###        
###################################################

# area of network in mm^2; scales numbers of neurons
# use 1 for the full-size network (77,169 neurons)
area    = 1.0

# Whether to scale number of synapses C linearly: C = C_full_scale * area.
# When scale_C_linearly is false, C is derived from the connection probabilities and
# scaled neuron numbers according to eq. (1) of the paper. In first order 
# approximation, this corresponds to C = C_full_scale * area**2.
# Note that this produces different dynamics compared to the original model.
scale_C_linearly  = True

layers  = np.array(["L23", "L4", "L5", "L6"])
types = np.array(["e", "i"]) 

full_scale_n_neurons = np.array( \
  [20683,   # layer 2/3 e
   5834,    # layer 2/3 i
   21915,   # layer 4 e
   5479,    # layer 4 i
   4850,    # layer 5 e
   1065,    # layer 5 i
   14395,   # layer 6 e
   2948])   # layer 6 i


# Synaptic weights
# Synaptic weight in the model are PSCs, which are derived in "model_class.py".
g     = 4.           # weight for inhibitory synapses
# Factor for mean EPSP amplitude for L4e->L2/3e connections.
# See p. 801 of the paper, second paragraph under "Model Parameterization",
# and the caption to Supplementary Fig. 7
j02 = 2.
# Mean reference PSP (EPSP amplitude except for L4e->L2/3e)
PSP_e   = .15           # mv
# Standard deviation of weight  relative to mean weight
weight_rel_sd = 0.1 


# Connection probabilities
# Probabilities for >=1 connection between neurons in the given populations
# columns correspond to source populations; rows to target populations
# i. e. conn_probs[post, pre] = conn_prob[target, source]
# source      L2/3e   L2/3i   L4e     L4i     L5e     L5i     L6e     L6i       
conn_probs = np.array(
            [[0.1009, 0.1689, 0.0437, 0.0818, 0.0323, 0.    , 0.0076, 0.    ],
             [0.1346, 0.1371, 0.0316, 0.0515, 0.0755, 0.    , 0.0042, 0.    ],
             [0.0077, 0.0059, 0.0497, 0.135 , 0.0067, 0.0003, 0.0453, 0.    ],
             [0.0691, 0.0029, 0.0794, 0.1597, 0.0033, 0.    , 0.1057, 0.    ],
             [0.1004, 0.0622, 0.0505, 0.0057, 0.0831, 0.3726, 0.0204, 0.    ],
             [0.0548, 0.0269, 0.0257, 0.0022, 0.06  , 0.3158, 0.0086, 0.    ],
             [0.0156, 0.0066, 0.0211, 0.0166, 0.0572, 0.0197, 0.0396, 0.2252],
             [0.0364, 0.001 , 0.0034, 0.0005, 0.0277, 0.008 , 0.0658, 0.1443]])
	     
# mean dendritic delays for excitatory and inhibitory transmission (ms)
delay_e = 1.5   # ms, excitatory synapses
delay_i = 0.75  # ms, inhibitory synapses
# standard deviation relative to mean delays
delay_rel_sd = 0.5 

# Synapse dictionaries
# default connection dictionary
connection_rule   = "fixed_total_number"
# weight distribution of connections between populations
weight_dict_exc = {"distribution": "normal_clipped", "low": 0.0} 
weight_dict_inh = {"distribution": "normal_clipped", "high": 0.0} 
# delay distribution of connections between populations
delay_dict  = {"distribution": "normal_clipped", "low": 0.1} 
# default synapse dictionary
syn_dict = {"model": "static_synapse"}


###################################################
###          Single-neuron parameters		###        
###################################################

neuron_model = "iaf_psc_exp"    # "iaf_psc_delta" or "iaf_psc_exp"
Vm0_mean    = -58.0             # mean of initial membrane potential (mV)
Vm0_std     = 10.0              # std of initial membrane potential (mV)

# neuron model parameters
model_params = {"tau_m": 10.,       # membrane time constant (ms)
                "t_ref": 2.,        # absolute refractory period (ms)
                "C_m": 250.,        # membrane capacitance (pF)
                "E_L": -65.,        # resting membrane potential (mV)
                "V_th": -50.,       # spike threshold (mV)
                "V_reset": -65.     # reset potential (mV)
               } 

# Synaptic time constants are only applied if the neuron model is not iaf_psc_delta
tau_syn_ex = 0.5 # excitatory synaptic time constant (ms)
tau_syn_in = 0.5 # inhibitory synaptic time constant (ms)

###################################################
###           Stimulus parameters		###        
###################################################
 
# rate of background Poisson input at each external input synapse (spikes/s) 
rate_ext    = 8.        # Hz 
PSP_ext     = 0.15      # mean EPSP amplitude (mV) for external input
# DC amplitude at each external input synapse (pA)
# This is relevant for reproducing Potjans & Diesmann (2012) Fig. 7.
dc_amplitude = 0. 
# in-degrees for background input
C_aext = np.array([
        1600,   # 2/3e
        1500,   # 2/3i
        2100,   # 4e
        1900,   # 4i
        2000,   # 5e
        1900,   # 5i
        2900,   # 6e
        2100])   # 6i
        

# optional additional thalamic input (Poisson)
# Set n_th to 0 to avoid this input.
# For producing Potjans & Diesmann (2012) Fig. 10, n_th = 902 was used.
# Note that the thalamic rate here reproduces the simulation results
# shown in the paper, and differs from the rate given in the text. 
n_th    = 0       # size of thalamic population
th_start    = 700.  # onset of thalamic input (ms)
th_duration = 10.   # duration of thalamic input (ms)
th_rate = 120.      # rate of thalamic neurons (spikes/s)
PSP_th  = 0.15      # mean EPSP amplitude (mV) for thalamic input

# connection probabilities for thalamic input
conn_probs_th = np.array(
        [0.0,       # 2/3e
         0.0,       # 2/3i    
         0.0983,    # 4e
         0.0619,    # 4i
         0.0,       # 5e
         0.0,       # 5i
         0.0512,    # 6e
         0.0196])   # 6i
      

# mean delay of thalamic input (ms)
delay_th    = 1.5  
# standard deviation relative to mean delay of thalamic input
delay_th_rel_sd = 0.5  
