# Calibration transfer based on likelihood maximization 
# Script contains several functions:
# - MLR regression function 
# - coefficient of determination (R2) function
# - PLS function
# - PPLS function
# - LMIR functions: create & exploit
# - function for subervised selection of observations
# - function to build estimation model
# - function to used estimation model 
# - pre-processing functions (autoscale, SNV, EMSC, MSC, detrend, savitzky_golay)
# - loadmat function to load matlab data

import numpy as np
from scipy.spatial import distance
import scipy
import statsmodels.api as sm

#%% MLR regress function 

def regress(y, X):
    model = sm.OLS(y, X).fit()
    b = model.params
    b_int = model.conf_int(0.05)
    b = (b[np.newaxis]).T # Vector format for output
    
    R2 = model.rsquared
    F = model.fvalue
    p = model.f_pvalue
    
    return b, b_int, model, R2, F, p


#%% Coefficient of determination function

def fct_R2(y,yhat):
    # R2 in calibration
    n = y.shape[0]
    ym = np.ones((n,1))*np.mean(y) # Vector form
    SSr = np.sum((yhat-ym)**2)
    SSe = np.sum((y-yhat)**2)
    SSt = sum((y-ym)**2)
    
    R2 = 1 - SSe / SSt
    
    return R2

#%% PLS function

def PLS(X, Y, nbPC):
    ''' 
    
    PLS: partial least squares
    [T, U, P, W, Q, B, Yhat, SSX, SSY] = PLS(X, Y, nbPC)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    Y [n x m] <numpy.ndarray>
        responses
        n samples
        m variables
    npPC [1 x 1] <numpy.ndarray>
        number of components in the PLS decomposition
    
    OUTPUT
    T [n x nbPC] 
        X-block scores
    U [n x nbPC] 
        Y-block scores           
    P [k x nbPC] 
        X-block loadings
    W [k x nbPC] 
        X-block weights        
    Q [m x nbPC] 
        Y-block weights         
    B [nbPC x nbPC]
        Y-block weights 
    Yhat [n x nbPC]
        Y predictions        
    SSX [nbPC x 1] 
        X-block sum of squared variance explained by each component
    SSY [nbPC x 1] 
        Y-block sum of squared variance explained by each component
        
    '''
    

    s0, s1 = X.shape
    s0, s2 = Y.shape
    T = np.zeros(shape=(s0, nbPC))
    U = np.zeros(shape=(s0, nbPC))
    P = np.zeros(shape=(s1, nbPC))
    W = np.zeros(shape=(s1, nbPC))
    Q = np.zeros(shape=(s2, nbPC))
    B = np.zeros(shape=(nbPC, nbPC))
    SSX = np.zeros(shape=(nbPC, 1))
    SSY = np.zeros(shape=(nbPC, 1))
    X0 = X # Save a copy
    Y0 = Y # Save a copy
    
    for i in range(0,nbPC):
        error = 1
        u_temp = np.random.randn(s0, 1)
        u = np.random.randn(s0, 1)
        
        while error > 1E-10:
            w = (X.T @ u) / np.linalg.norm(X.T @ u)
            
            # Fix rotational ambiguity
            onez = np.ones([len(w),1]) # Use as a reference
            if w.T@onez < 0:
                w = -w
                
            t = X @ w    
            q = (Y.T @ t) / np.linalg.norm(Y.T @ t)
            u = Y @ q
            # Check t convergence 
            error = sum(np.power((u-u_temp),2),0) # Squared error
            u_temp = u
        
        # Deflation
        p = (X.T@t)/(t.T@t)
        b = (u.T@t)/(t.T@t) # U = fct(T)
        X = X - t@p.T
        Y = Y - b*t@q.T
               
        # Save        
        W[:,i] = np.squeeze(w)
        P[:,i] = np.squeeze(p)
        T[:,i] = np.squeeze(t)
        U[:,i] = np.squeeze(u)
        Q[:,i] = np.squeeze(q)
        B[i,i] = b

        # Sum of squares X
        Xhat = t@p.T
        ssX0 = np.sum(np.sum(X0 * X0)) # Each element squared
        ssX = np.sum(np.sum(Xhat * Xhat))
        ssX = ssX / ssX0
        SSX[i] = ssX
 
        # Sum of squares Y 
        Yhat = b*t@q.T
        ssY0 = np.sum(np.sum(Y0 * Y0)) # Each element squared
        ssY = np.sum(np.sum(Yhat * Yhat))
        ssY = ssY / ssY0
        SSY[i] = ssY
        
    Yhat = T@B@Q.T # NIPALS
        
    return T, U, P, W, Q, B, Yhat, SSX, SSY



#%% P-PLS function

def PPLS(X,y, nbPC):

    gamma = np.arange(0,1,.01)
    gamma = np.append(gamma,np.array([.999,.9999,.99999,.999999]))
    gamma = np.array([gamma]).T
    
    all_weights = []
    all_scores = []
    
    for A in range(nbPC):
        
        w = np.array([np.corrcoef(X.T,y.T)[-1,:-1]])
        s = w/np.abs(w)
        w = np.abs(w)
        w = w/np.max(w)
        allW = w**( gamma/(1-gamma) )
        allW = s*allW
        
        T = X@allW.T
        all_correlations = np.corrcoef(T.T,y.T)[-1,:-1]
        pos_max_corr = np.argmax(all_correlations)
        
        best_w = allW[pos_max_corr:pos_max_corr+1,:]
        best_t = T[:,pos_max_corr:pos_max_corr+1]
        
        scaling = np.linalg.pinv(best_t.T@best_t)@best_t.T@y
        scaling = scaling[0,0]
        y_pred = best_t*scaling
        
        all_weights.append( (best_w*scaling)[0] )
        
        # y Deflation
        y = y-y_pred
    
    
    all_weights = np.array(all_weights)
    # filter_w = abs(all_weights) < 10**-4
    # all_weights[filter_w] = 0
    
    y_pred_final = np.sum(X@all_weights.T,axis=1)
    y_pred_final = y_pred_final[np.newaxis].T
    
    return all_weights, all_scores, y_pred_final

#%% LMIR functions

def LMIR_create(X,y):

    n,k = X.shape
    
    X0 = X.copy()
    y0 = y.copy()
    
    
    #----- Initialization------
    model = {'y_exp_vector':[],'covE':[],'covE_inv':[], 'Xpred_NL_LMIR':[]}
    ypred = np.zeros([n,1])
    
    
    # Create y expectation vector
    # y_exp_vector = np.linspace(min(y), max(y),1000)
    y_exp_vector = np.linspace(-3, 3,1000)[np.newaxis].T
    model['y_exp_vector']= y_exp_vector
    
    # Linear model calculation
    models_l = []
    # Error matrix
    x_pred = np.zeros([n,k])
    # Register model for each variable in X
    y = np.concatenate((np.ones((n,1)),y),axis=1)
    for j in range(k):
        xj = X[:,j][np.newaxis].T
        b, _, _, _, _, _  = regress(xj,y)
        x_pred[:,j] = np.squeeze(y@b)
        models_l.append(b)
    
    # For each calibration observation
    for j in range(k):    
        # For each variable
        x_pred[:,j] = np.squeeze(y@models_l[j])
    
    # Error matrix
    E = X - x_pred
    
    # From all errors, calculate the variance-covariance matrix
    covE = np.cov(E.T) 
    model['covE']= covE 
    
    covE_inv = np.linalg.pinv(covE)
    model['covE_inv'] = covE_inv
    
    # Estimate X matrix for a lot of different values of y with
    Xpred_NL_LMIR = np.zeros([1000, k])
    
    y_exp_vector1 = np.concatenate((np.ones((1000,1)),y_exp_vector),axis=1)
    for j in range(k):    
        # For each variable
        Xpred_NL_LMIR[:,j] = np.squeeze(y_exp_vector1@models_l[j])
    
    model['Xpred_NL_LMIR'] = Xpred_NL_LMIR
    
    # Make predictions
    for i in range(n):
        # Non-linear LMIR
        # Expected errors
        Errs = Xpred_NL_LMIR - np.matlib.repmat(X[i,:],1000,1)
        # Without considering the additional noise
        LL_NL =  Errs@covE_inv@Errs.T
        LL_NL = np.diag(LL_NL)
        IND = np.argmin(LL_NL)
        ypred[i] = (y_exp_vector[IND])
        
        
    return model, ypred

def LMIR_exploit(X, model, cov_noise=0, return_LL_NL=False):
    # Initalize variables
    ypred = np.zeros([len(X),1])
    
    # # Make predictions
    for i in range(len(X)):
        # NON-LINEAR LMIR
        # Expected errors
        Errs = model['Xpred_NL_LMIR'] - np.matlib.repmat(X[i,:],1000,1)
        
        # Autoscaled performed in main code at the moment
        # Errs = model['Xpred_NL_LMIR'] - np.matlib.repmat((X[i,:] - model['Xm'])/model['Xs'],1000,1)
        
        # Without considering the additional noise
        covE = model['covE'] + cov_noise
        covE_inv = np.linalg.pinv(covE)
        LL_NL =  Errs@covE_inv@Errs.T
        LL_NL = np.diag(LL_NL)
        IND = np.argmin(LL_NL)
        ypred[i] = model['y_exp_vector'][IND]
    
    if return_LL_NL:
        return ypred, np.min(LL_NL)
    else:
        return ypred
    







#%% Supervised selection of observations

def fct_selobs(X, Nout,factor_k, distance_measure = "mahalanobis", dim_reduction = True):

    # ---------- Effective rank -----------------
    A = X.T@X
    [P,D,PT] = np.linalg.svd(A)  
    D = np.diag(D)
    # Lambda : eigenvalues 
    lada = np.diag(D) / np.sum(np.diag(D))
    # Shannon entropy
    Shannon = -np.sum(lada*np.log(lada)) # natural logarithm (log base e) 
    Effective_rank = np.exp(Shannon)
    
    
    xx_c = X.copy()
    Nin = len(xx_c)
    ncp = int(np.ceil(Effective_rank))
    first_ncp = 0
    U,sval,Vt = np.linalg.svd(xx_c, full_matrices = False, compute_uv=True)
    Sval = np.zeros((U.shape[0], Vt.shape[0]))
    Sval[0:sval.shape[0], 0:sval.shape[0]] = np.diag(sval)
    xx_u = U[:,first_ncp:ncp]
    xx_t = U[:,first_ncp:ncp].dot(Sval[first_ncp:ncp, first_ncp:ncp])

    
    if distance_measure == "mahalanobis":
        xx = xx_u
    elif dim_reduction:
        # print('yes')
        xx = xx_t
    else:
        xx = xx_c
        
    Nin = xx.shape[0]
    current_ncp = xx.shape[1]
    
    xx_mean = xx.mean(axis=0)
    xx_mean.shape = (1,xx_mean.shape[0])
    
    d = distance.cdist(xx, xx, metric = "euclidean")
    d_ini = factor_k * np.amax([current_ncp-2,1])
      


    sel = []
    obs = np.zeros((Nin), dtype=bool)
    m = 1
    dm = m * d_ini
    n_sel = 0
   
        
    count = 0
    
    while n_sel < Nout:
        idr = np.random.choice(np.arange(Nin)[np.invert(obs)], replace=False)
        sel.append(idr)
        
        min_d =  d[idr,:] <= dm
        obs = np.logical_or(obs, (min_d))
        n_sel = len(sel)
        
        count +=1
        
        if (sum(obs)==100):
            obs =  np.zeros((Nin), dtype=bool)
            obs[sel]=True
    
    
    sel = np.array(sel)
   
    return sel


#%% Create estimation model

def estimation_model(X1, Y1, X2c, Y2c,factor_k,nb_pairs=30,B=0):

    n1, k1  = X1.shape
    n2, k2 = X2c.shape
    
    if B==0:
        B = 3*max(k1,k2)

    R1_all = []
    R2_all = []
    g1_all = []
    g2_all = []
    
    y1_all = []
    y2_all = []
    
    save_p1 = []
    save_p2 = []
    
    pair = 0
    
    while pair < nb_pairs:    
        # On one block pair
        R1 = np.zeros((B,k1))
        R2 = np.zeros((B,k2))
        g1 = np.zeros((B,1))
        g2 = np.zeros((B,1))   
        
        # Bootstrap observation                   
        Y1r = []
        while len(np.unique(Y1r))<2:
    
            Nout = np.random.choice([int(0.3*n1),int(0.4*n1),int(0.5*n1)])
            rand_obs1 = fct_selobs(X1, Nout,factor_k, distance_measure = "mahalanobis", dim_reduction = True)
            
            save_p1.append(rand_obs1)
            
            
            X1_or = X1[rand_obs1,:]
            Y1r = Y1[rand_obs1]
              
        Y2r = []
        while len(np.unique(Y2r))<3:
            rand_obs2 =  np.random.choice(n2, int(0.5*n2), replace=False)
            save_p2.append(rand_obs2)
            
            X2_or = X2c[rand_obs2,:]
            Y2r = Y2c[rand_obs2] 
            
        # P-PLS models  
        for bi in range(B):
            rand_v1 = np.random.choice(k1, int(0.2*k1), replace=False)
            rand_v2 = np.random.choice(k2, int(0.2*k2), replace=False)
            
    
            X1r = X1_or[:,rand_v1]
            X2r = X2_or[:,rand_v2]
            
            # PPLS    
            beta1, all_scores, y_pred_final = PPLS(X1r, Y1r, 1)  
            # Validation on all obs available for X1
            Y1r_hat = (X1[:,rand_v1]@beta1.T)
            g1[bi] = fct_R2(Y1, Y1r_hat)
            R1[bi,rand_v1] = np.squeeze(beta1)
            y1_all.append(Y1r_hat)
            
            # PPLS    
            beta2, all_scores, y_pred_final = PPLS(X2r, Y2r, 1)
            # Validation on all obs available for X2c
            Y2r_hat = (X2c[:,rand_v2]@beta2.T)
            g2[bi] = fct_R2(Y2c, Y2r_hat)
            R2[bi,rand_v2] = np.squeeze(beta2)
            y2_all.append(Y2r_hat)
          
        # Replace negative values in g1 or g2
        g1[g1<0.0]=0
        g2[g2<0.0]=0
        
        if sum(g2==0) < int(B*2/3): 
            # Save
            R1_all.append(R1)
            R2_all.append(R2)
            g1_all.append(g1)
            g2_all.append(g2)
        
        
        pair = len(R1_all)
    return R1_all, g1_all, R2_all, g2_all

#%% Use estimation model

def estimation_exploit(R1_all,g1_all,R2_all,g2_all,X2c,X1,model):
    
    nb_pairs = len(g1_all)
    n1, k1  = X1.shape
    n2, k2 = X2c.shape

    #%% Estimation & prediction for calibration samples test set
    ypred_ct = []   
    x1hat_ct = []
    covx1_ct = []
        
    for i in range(len(X2c)):
             
        x1hat_p = []
        covx1_p = []
        Kp = np.zeros((nb_pairs,k1,k1))
        covx1_pinv = np.zeros((nb_pairs,k1,k1))
        for pair in range(nb_pairs):  
            # print('pair: '+str(pair))
            # Estimate x1hat from new spectra acquired on probe 2
            x2_new =  X2c[i,:][np.newaxis]
            y_new =  (R2_all[pair]@x2_new.T)
            h = np.diagflat(g1_all[pair]*g2_all[pair])
            x1_hat = scipy.linalg.inv(R1_all[pair].T@h@R1_all[pair])@(R1_all[pair].T@h@y_new)
            x1_hat = x1_hat.T
       
            MSE = R1_all[pair]@x1_hat.T
            MSE = np.sum((MSE - y_new)**2)/np.sum(h)
    
            cov_x1 = scipy.linalg.inv(R1_all[pair].T@h@R1_all[pair])*MSE
            
            # Save
            x1hat_p.append(x1_hat)
            covx1_p.append(cov_x1)
    
        # Global estimation   
        x1hat_p = np.reshape(x1hat_p, [nb_pairs,1,k1])   
        covx1_p = np.squeeze(covx1_p)
        
        for pair in range(nb_pairs):
            covx1_pinv[pair,:,:] = scipy.linalg.inv(covx1_p[pair,:,:])
        Kp = scipy.linalg.inv(np.sum(covx1_pinv, axis=0))@covx1_pinv
        
        x1hat_bar = np.sum(x1hat_p@Kp, axis=0)
        
        covx1_bar = np.sum(scipy.linalg.inv(np.sum(covx1_pinv, axis=0))@ \
                            scipy.linalg.inv(np.sum(covx1_pinv, axis=0))@\
                            covx1_pinv, axis=0)                   
                            
        covx1_bar = nb_pairs*covx1_bar
    
        x1hat_ct.append(x1hat_bar)
        covx1_ct.append(covx1_bar)
    
        # Prediction    
        ypred_x1hat = LMIR_exploit(x1hat_bar, model, covx1_bar)
        ypred_ct.append(ypred_x1hat)
        
        Kp_all = np.sum(Kp, axis=0)
        
    ypred_ct = np.array(ypred_ct)
    ypred_ct = np.squeeze(ypred_ct)
    ypred_ct = ypred_ct[np.newaxis].T

    return ypred_ct, x1hat_ct, covx1_ct 

#%% Pre-processing functions
from numpy import matlib as mb

def autoscale(X, *args):
    '''
    
    Autoscale: center and scale to unit variance
    [X_auto, mX, sX] = autoscale(X)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    *args
        optional inputs
        mX [1 x k] 
            mean of all variables - computed beforehand
        sX [1 x k] 
            standard deviation of all variables - computed beforehand       
    
    OUTPUT
    X_auto [n x k] 
        preprocessed spectra
    mX [1 x k] 
        mean of all variables
    sX [1 x k] 
        standard deviation of all variables        
    
    '''
    
    varargin = args
    n_params = len(varargin)

    if n_params == 2:
        mx = varargin[0]
        stdx = varargin[1]
        mx = np.squeeze(mx)
        stdx = np.squeeze(stdx)
        
    else:
        mx = np.nanmean(X, axis=0)
        stdx = np.nanstd(X, axis=0)     
    
    
    m,n = X.shape
    
    # Deal with NaN values occuring when std = 0
    for i in range(X.shape[1]):
        if stdx[i] == 0:
            X[:,i] = np.zeros((X.shape[0]))
            
        else:
            X[:,i] = (X[:,i] - mx[i])/stdx[i]
    
    mx = mx[np.newaxis]
    stdx = stdx[np.newaxis]
    
    return X, mx, stdx

def SNV(x):
    ''' 
    
    SNV: standard normal variate
    [X_snv] = snv(X)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    
    OUTPUT
    X_snv [n x k] 
        preprocessed spectra
    
    '''

    [m,n]=x.shape
    rmean=np.mean(x,1)
    rmean = (rmean[np.newaxis]).T
    dr=x-mb.repmat(rmean,1,n)
    drsum = np.sqrt(np.sum(dr**2,1)/(n-1))
    drsum = (drsum[np.newaxis]).T
    x_snv=dr/np.matlib.repmat(drsum,1,n)
    
    return x_snv

def EMSC(spectra):
    '''
    
    EMSC: extended multiplicative scatter correction to the mean
    [X_emsc] = EMSC(X)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    
    OUTPUT
    X_emsc [n x k] 
        preprocessed spectra
       
    '''
    
    spectra = spectra.T
        
    wave = np.arange(0,spectra.shape[0],1)    
    p1 = .5 * (wave[0] + wave[-1])
    p2 = 2 / (wave[0] - wave[-1])

    # Compute model terms
    model = np.ones((wave.size, 4))
    model[:, 1] = p2 * (wave[0] - wave) - 1
    model[:, 2] = (p2 ** 2) * ((wave - p1) ** 2)
    model[:, 3] = np.mean(spectra, axis=1)

    # Solve correction parameters
    params = np.linalg.lstsq(model, spectra,rcond=None)[0].T

    # Apply correction
    spectra = spectra - np.dot(params[:, :-1], model[:, :-1].T).T
    spectra = np.multiply(spectra, 1 / np.repeat(params[:, -1].reshape(1, -1), spectra.shape[0], axis=0))

    spectra = spectra.T
    return spectra

def MSC(input_data):
    ''' 
    MSC: Multiplicative scatter correction
    [X_msc,reference] = msc(X,reference)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    
    OUTPUT
    X_msc [n x k] 
        preprocessed spectra
    reference [1 x k] 
        reference spectra
    '''
    
    
    
    # mean centre correction
    for i in range(input_data.shape[0]):
        input_data[i,:] -= input_data[i,:].mean()
    
    # Get the reference spectrum : calculate mean
    ref = np.mean(input_data, axis=0)    
        
    # Define a new array and populate it with the corrected data    
    data_msc = np.zeros_like(input_data)
    for i in range(input_data.shape[0]):
        # Run regression
        fit = np.polyfit(ref, input_data[i,:], 1, full=True)
        # Apply correction
        data_msc[i,:] = (input_data[i,:] - fit[0][1]) / fit[0][0] 
    
    ref = ref[np.newaxis]
    return (data_msc,ref) 



def detrend(spectra):
    '''
    
    Detrend: Perform spectral detrending to remove linear trend from data
    [X_detrend] = detrend(X)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    
    OUTPUT
    X_detrend [n x k] 
        preprocessed spectra      
    
    '''
    
    return scipy.signal.detrend(spectra, bp=0)


def savitzky_golay(Y, window_size, order, deriv, rate=1):
    ''' 
    
    Savitzky Golay smoothing and derivative of spectral data
    [X_sg] = savitzky_golay(X,window_size, order, deriv)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    window_size [1 x 1] <numpy.ndarray>
        width of the smoothing window
    order [1 x 1] <numpy.ndarray>
        order of the polynomial function used for the smoothing
    deriv [1 x 1] <numpy.ndarray>
        degree of the derivative
  
    OUTPUT
    X_sg [n x k] 
        preprocessed spectra
    
    '''
    for i in range(Y.shape[0]):
        Y[i,:] = sav_gol(Y[i,:], window_size, order, deriv)
        
    return Y

#%% Function to load matlab data

import scipy.io as spio

def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    def _check_keys(d):
        '''
        checks if entries in dictionary are mat-objects. If yes
        todict is called to change them to nested dictionaries
        '''
        for key in d:
            if isinstance(d[key], spio.matlab.mio5_params.mat_struct):
                d[key] = _todict(d[key])
        return d

    def _has_struct(elem):
        """Determine if elem is an array and if any array item is a struct"""
        return isinstance(elem, np.ndarray) and any(isinstance(e, spio.matlab.mio5_params.mat_struct) for e in elem)

    def _todict(matobj):
        '''
        A recursive function which constructs from matobjects nested dictionaries
        '''
        d = {}
        for strg in matobj._fieldnames:
            elem = matobj.__dict__[strg]
            if isinstance(elem, spio.matlab.mio5_params.mat_struct):
                d[strg] = _todict(elem)
            elif _has_struct(elem):
                d[strg] = _tolist(elem)
            else:
                d[strg] = elem
        return d

    def _tolist(ndarray):
        '''
        A recursive function which constructs lists from cellarrays
        (which are loaded as numpy ndarrays), recursing into the elements
        if they contain matobjects.
        '''
        elem_list = []
        for sub_elem in ndarray:
            if isinstance(sub_elem, spio.matlab.mio5_params.mat_struct):
                elem_list.append(_todict(sub_elem))
            elif _has_struct(sub_elem):
                elem_list.append(_tolist(sub_elem))
            else:
                elem_list.append(sub_elem)
        return elem_list
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)