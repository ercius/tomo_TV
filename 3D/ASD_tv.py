# General 3D - ASD/TV Reconstruction with Positivity Constraint. 

import sys
sys.path.append('./Utils')
from pytvlib import parallelRay, timer, load_data
import plot_results as pr
import numpy as np
import ctvlib 
import time
########################################

file_name = '256_Co2P_tiltser.tif'

# Number of Iterations (Main Loop)
Niter = 15

# Number of Iterations (TV Loop)
ng = 10

# Parameter in ART Reconstruction.
beta = 1.0

# ART Reduction.
beta_red = 0.975

# Data Tolerance Parameter
eps = 0.5

# Reduction Criteria
r_max = 0.95
alpha_red = 0.95
alpha = 0.5

#Outcomes:
save = True                 # Save final Reconstruction. 
show_live_plot = False      # Show intermediate results.
show_final_plot = False     # Show final results (i.e. tv and dd) 
##########################################

# #Read Image. 
(file_name, tiltSeries) = load_data(file_name)
(Nslice, Nray, Nproj) = tiltSeries.shape
b = np.zeros([Nslice, Nray*Nproj])

# Initialize C++ Object.. 
tomo_obj = ctvlib.ctvlib(Nslice, Nray, Nproj)

for s in range(Nslice):
    b[s,:] = tiltSeries[s,:,:].transpose().ravel()
tomo_obj.setTiltSeries(b)
tiltSeries = None

# Generate Tilt Angles.
tiltAngles = np.load('Tilt_Series/'+ file_name +'_tiltAngles.npy')

# Generate measurement matrix
A = parallelRay(Nray, tiltAngles)
tomo_obj.load_A(A)
A = None
tomo_obj.rowInnerProduct()

dd_vec = np.zeros(Niter)
tv_vec = np.zeros(Niter)

counter = 1 

t0 = time.time()

#Main Loop
for i in range(Niter): 

    if ( i % 25 ==0):
        print('Iteration No.: ' + str(i+1) +'/'+str(Niter))

    tomo_obj.copy_recon()

    #ART Reconstruction. 
    tomo_obj.ART(beta, -1)

    #Positivity constraint 
    tomo_obj.positivity()

    #ART-Beta Reduction
    beta *= beta_red 

    #Forward Projection.
    tomo_obj.forwardProjection(-1)

    #Measure Magnitude for TV - GD.
    if (i == 0):
        dPOCS = tomo_obj.matrix_2norm() * alpha
        dp = dPOCS / alpha
    else: # Measure change from ART.
        dp = tomo_obj.matrix_2norm() 

    # Measure difference between exp/sim projections.
    dd_vec[i] = tomo_obj.vector_2norm()

    #Measure TV. 
    tv_vec[i] = tomo_obj.tv()

    tomo_obj.copy_recon() 

    #TV Minimization. 
    tomo_obj.tv_gd(ng, dPOCS)
    dg = tomo_obj.matrix_2norm()

    if(dg > dp * r_max and dd_vec[i] > eps):
        dPOCS *= alpha_red

    if ((i+1) % 15 ==0):
        timer(t0, counter, Niter)
        if show_live_plot:
            pr.ASD_live_plot(dd_vec, eps, tv_vec, i)

    counter += 1

#Get the final reconstruction. 
recon = np.zeros([Nslice, Nray, Nray], dtype=np.float32, order='F') 
for s in range(Nslice):
    recon[s,:,:] = tomo_obj.getRecon(s)

if show_final_plot:
    pr.ASD_results(dd_vec, eps, tv_vec) 

if save:
    np.save('Results/TV_'+ file_name + '_recon.npy', recon)