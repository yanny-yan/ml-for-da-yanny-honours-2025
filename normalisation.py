import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
ds = nc.Dataset("F:/speedy_datasets_james/(Copy) run_3k_tsteps/run_3k_tsteps/output.nc", mode='r')

def std_a_temporal_diff(a):
    
    T = a.shape[0]; Y = a.shape[1]; X = a.shape[2]
    inv_TYX = 1/(T*X*Y)
    
    mu_a = np.mean(a)
    std_a = np.std(a)
    
    # standard normalisation
    a_ff = (a - mu_a)/std_a
    
    # temporal difference
    a_ff_dash = a_ff[1:T-1] - a_ff[0:T-2]
    
    # std of temoporal difference
    std_a_ff = inv_TYX*( (a_ff_dash ** 2).sum() ) # 1/TXY(sum_txy( temporal difference squared ) )
    return (np.sqrt(std_a_ff), a_ff)


if __name__ == "__main__":

    # just looking at surface level for now
    std_all = np.empty([4])
    
    # meridonal wind, v
    v_std_ff = std_a_temporal_diff(ds['v'][:,0,:,:])
    std_all[0] = v_std_ff[0]  #first index is std, second is full field
    
    # zonal wind, u
    u_std_ff = std_a_temporal_diff(ds['u'][:,0,:,:])
    std_all[1] = u_std_ff[0]
    
    # humid
    humid_std_ff = std_a_temporal_diff(ds['humid'][:,0,:,:])
    std_all[2] = humid_std_ff[0]
    
    # temp
    temp_std_ff = std_a_temporal_diff(ds['temp'][:,0,:,:])
    std_all[3] = temp_std_ff[0]
    
    #spres
    spres_std_ff = std_a_temporal_diff(ds['spres'][:,:,:])
    std_all[1] = spres_std_ff[0]
    
    std_geo_mean = std_all.mean()
    
    # all 5 residuals
    v_res = v_std_ff[1]/std_geo_mean
    u_res = u_std_ff[1]/std_geo_mean
    humid_res = humid_std_ff[1]/std_geo_mean
    temp_res = temp_std_ff[1]/std_geo_mean
    spres_res = spres_std_ff[1]/std_geo_mean

    f, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5,1, figsize=(5, 15))

    t=100
    
    pos1 = ax1.imshow(v_res[t])
    pos2 = ax2.imshow(u_res[t])
    pos3 = ax3.imshow(humid_res[t])
    pos4 = ax4.imshow(temp_res[t])
    pos5 = ax5.imshow(spres_res[t])
    
    f.colorbar(pos1)
    f.colorbar(pos2)
    f.colorbar(pos3)
    f.colorbar(pos4)
    f.colorbar(pos5)
    
    plt.show()