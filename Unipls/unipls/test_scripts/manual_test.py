#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 14:31:48 2018

data from University of Copenhagen, Frans van den Berg
http://www.models.life.ku.dk/~courses/MBtoolbox/mbtmain.htm

info from data origin:
X (objects x all X-block variables) one, augmented data matrix with all the X-blocks
Xin (number of X-blocks x 2 = first and last variable per block) index for X-blocks
(optional:)
Xpp (number of X-blocks x 3) processing per X-block
 - first entry scaling: 0=do not scale to sum-of-squares, number=scale to sum-of-squares
 - second entry preprocessing: 0=none, 1=mean centering, 2=auto scaling
 - third entry = number of factors to compute for this X-block
Y (objects x all Y-block variables) one, augmented data matrix with all the Y-blocks
Yin (number of Y-blocks x 2 = first and last variable per block) index for Y-blocks
 - if omitted, one Y-block is assumed
Ypp (number of Y-blocks x 1) preprocessing per Y-block: 0=none, 1=mean centering, 2=auto scaling
Model (1 x 2) first entry : 0 = no cross validation (default), 1 = cross validation;
  second entry overrides default modeling methods (MBCPCA for X, MBSPLS for X and Y)
- 0=MBCPCA, 1=MBPCA, 2=MBHPCA
- 10=MBSPLS, 11=MBBPLS, 12=MBHPLS

@author: Andreas Baum, andba@dtu.dk
@edited: Laurent Vermue, lauve@dtu.dk
"""
#%%
from matplotlib import pyplot as plt
from unipls.data.get_data import data_path
from unipls.mbpls import MBPLS
import numpy as np
import os

plt.ioff()


def loaddata():
    from scipy.io import loadmat
    data = loadmat(os.path.join(data_path(), 'MBdata.mat'))
    y = data['Y']
    x1 = data['X'][:, :50]
    x2 = data['X'][:, 50:]
    return x1, x2, y


def plotdata(spectra, yields):
    yields = yields + abs(yields.min())
    for spectrum, yield1 in zip(spectra, yields / yields.max()):
        plt.plot(spectrum.T, color=[0, 0, yield1], linewidth=6)


def preprocess(spectra, yields):
    from sklearn.preprocessing import StandardScaler
    Scaler1 = StandardScaler(with_mean=True, with_std=False)
    Scaler2 = StandardScaler(with_mean=True, with_std=True)
    return Scaler1.fit_transform(spectra), Scaler2.fit_transform(yields)


plt.close('all')
x1, x2, y = loaddata()
x1_process, y_process = preprocess(x1, y)
x2_process, y_process = preprocess(x2, y)

## Plot preprocessed datablocks X1 and X2 colored according to y1, y2, y3
#plt.subplot(231)
#plotdata(x1, y[:, 0:1])
#plt.title('Block x1 colored by y[:,0]')
#plt.subplot(232)
#plotdata(x1, y[:, 1:2])
#plt.title('Block x1 colored by y[:,1]')
#plt.subplot(233)
#plotdata(x1, y[:, 2:3])
#plt.title('Block x1 colored by y[:,2]')
#
#plt.subplot(234)
#plotdata(x2, y[:, 0:1])
#plt.title('Block x2 colored by y[:,0]')
#plt.subplot(235)
#plotdata(x2, y[:, 1:2])
#plt.title('Block x2 colored by y[:,1]')
#plt.subplot(236)
#plotdata(x2, y[:, 2:3])
#plt.title('Block x2 colored by y[:, 2]')
#plt.show()

# Here follows the calculation

pls_own_SVD = MBPLS(n_components = 1, method='SVD', standardize=True)
pls_own_NIPALS = MBPLS(n_components = 1, method='NIPALS', standardize=True)
pls_own_SIMPLS = MBPLS(n_components = 1, method='SIMPLS', standardize=True)

pls_own_SVD.fit([x1, x2], y[:, 0:1])
pls_own_NIPALS.fit([x1, x2], y[:,0:1])
pls_own_SIMPLS.fit([x1, x2], y[:,0:1])

#%%
print(np.sum(np.abs(pls_own_SIMPLS.Ts)-np.abs(pls_own_SVD.Ts)))
X=np.hstack((x1, x2))
X.dot(pls_own_SVD.beta)



#%% Testing on data from above

pls_own_NIPALS = MBPLS(n_components = 2, method='NIPALS', standardize=True)
pls_own_NIPALS.fit([x1, x2], y[:,0:2])
print(pls_own_NIPALS.A)
pls_own_NIPALS = MBPLS(n_components = 2, method='NIPALS', standardize=False)
pls_own_NIPALS.fit([x1, x2], y[:,0:2])
print(pls_own_NIPALS.A)

#%% Testing vectors that are not completely othogonal
a=np.random.randint(1,20,size=(20,500))
y_a=a[:,0:1] * 100
y_a = y_a.T + np.random.rand(a[:,0:1].shape[0])
y_a = y_a.T
a1=a[:,0:2]
a2=a[:,2:]


# Not standardizing the blocks renders the blockimportance useless

pls_own_NIPALS = MBPLS(n_components = 2, method='NIPALS', standardize=True)
pls_own_NIPALS.fit([a1, a2], y_a)
print(pls_own_NIPALS.A)
pls_own_NIPALS = MBPLS(n_components = 2, method='NIPALS', standardize=False)
pls_own_NIPALS.fit([a1, a2], y_a)
print(pls_own_NIPALS.A)

#%% Testing completely orthogonal vectors
from scipy.stats import ortho_group
A = ortho_group.rvs(100)
y_a=A[:,0:1] * 10
y_a = y_a.T + np.random.rand(A[:,0:1].shape[0])
y_a = y_a.T
a1=A[:,0:2]
a2=A[:,2:]

# Not standardizing the blocks renders the blockimportance useless

pls_own_NIPALS = MBPLS(n_components = 2, method='NIPALS', standardize=True)
pls_own_NIPALS.fit([a1, a2], y_a)
print(pls_own_NIPALS.A)
pls_own_NIPALS = MBPLS(n_components = 2, method='NIPALS', standardize=False)
pls_own_NIPALS.fit([a1, a2], y_a)
print(pls_own_NIPALS.A)



#%%

# Specify here which Component loadings and scores to plot below
pls_own_SVD.plot(4)
# pls_own_SVD.plot([1,3,5])
pls_own_NIPALS.plot(4)

# Scikit Learn PLS
from sklearn.cross_decomposition import PLSRegression

pls = PLSRegression(n_components=2, scale=False)
scikitpls = pls.fit(X=np.hstack((x1_process, x2_process)), Y=y_process[:, 0:1])
#scikitscores = scikitpls.x_scores_
#scikitloadings = scikitpls.x_loadings_

#pls = PLSSVD(n_components=1, scale=False)
#scikitpls = pls.fit(X=np.hstack((x1_process, x2_process)), Y=y_process[:,0:1])
#scikitscores = scikitpls.x_scores_

#print(pls_own_NIPALS.W[1][10,1])
#print(pls_own_SVD.W[1][10,1])