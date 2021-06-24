import numpy as np
import xarray as xr
import os

def field_150m_mean(da):
    """compute mean over upper 100 m; assume constant dz"""
    depth_slice = slice(0, 150e2)
    with xr.set_options(keep_attrs=True):
        if 'z_t' in da.dims:
            return da.sel(z_t=depth_slice).mean('z_t')
        elif 'z_t_150m' in da.dims:
            return da.mean('z_t_150m')

        
def field_150m_zint(da, dz):
    """compute integral over upper 100 m; assume constant dz"""
    depth_slice = slice(0, 150e2)
    with xr.set_options(keep_attrs=True):
        if 'z_t' in da.dims:            
            dao = (dz * da).sel(z_t=depth_slice).sum('z_t')
        elif 'z_t_150m' in da.dims:
            dao = (dz.isel(z_t=slice(0, 15)).rename({'z_t': 'z_t_150m'}) * da).sum('z_t_150m')
    dao.attrs['units'] = da.attrs['units'] + ' cm'        
    return dao

def field_at_bottom(da, KMT):
    """return a field indexed at the model's bottom layer"""

    tmp_bot = xr.DataArray(np.ones(da[:, 0, :, :].shape) * np.nan, 
                           dims=tuple(da.dims[i] for i in [0, 2, 3]),
                           coords={c: da.coords[c] for c in ['time']},
                          )

    assert KMT.shape == da.shape[-2:]
    
    for j in range(len(da.nlat)):
        for i in range(len(da.nlon)):
            if KMT[j, i] > 0:
                k = int(KMT[j, i] - 1)
                tmp_bot.values[:, j, i] = da[:, k, j, i]
    return tmp_bot


def file_in(var,styear,member):
    
    case = 'g.e11_LENS.GECOIAF.T62_g16.009'
    m03 = "{:03d}".format(member)
    endyear = styear + 10
    droot = '/glade/campaign/cesm/collections/CESM1-DPLE/ocn/proc/tseries/monthly/' + var + '/'
    filename = 'b.e11.BDP.f09_g16.' + str(styear) + '-11.' + m03 + '.pop.h.' +  var + '.' + str(styear) + '11-' + str(endyear) + '12.nc'

    file = droot + filename
    
    
    assert os.path.exists(file), f'missing {file}'
    return file


def file_out(dout,var,styear,member):
    
    case = 'g.e11_LENS.GECOIAF.T62_g16.009'
    m03 = "{:03d}".format(member)
    endyear = styear + 10
    filename = 'b.e11.BDP.f09_g16.' + str(styear) + '-11.' + m03 + '.pop.h.' +  var + '.' + str(styear) + '11-' + str(endyear) + '12.nc'

    file = dout + filename
    
    return file
