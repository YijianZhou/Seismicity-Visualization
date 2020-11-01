import matplotlib.pyplot as plt
import numpy as np

# 1. fit G-R law: Mc, b-value & a-value
def gr_fit(mag, min_num=100, method='MAXC'):
    if len(mag) < min_num: return np.nan, [np.nan, np.nan], np.nan
    mag = np.array(mag)
    if method=='MAXC': mc = calc_mc_maxc(mag)
    mag = mag[mag>=mc]
    b_val, b_dev = calc_b(mag)
    return mc, [b_val, b_dev], np.log10(len(mag))


# calc b value
def calc_b(mag, min_num=None):
    num_events = len(mag)
    if min_num: 
        if num_events < min_num: return -1, -1
    b_val = np.log10(np.exp(1)) / (np.mean(mag) - np.min(mag) + 0.05)
    b_dev = 2.3 * b_val**2 * (np.var(mag) / num_events)**0.5
    return round(b_val,2), round(b_dev,2)


# calc fmd
def calc_fmd(mag):
    mag = mag[mag!=-np.inf]
    mag_max = np.ceil(10 * max(mag)) / 10
    mag_min = np.floor(10 * min(mag)) / 10
    mag_bin = np.around(np.arange(mag_min-0.1, mag_max+0.2, 0.1),1)
    num = np.histogram(mag, mag_bin)[0]
    cum_num = np.cumsum(num[::-1])[::-1]
    return mag_bin[1:], num, cum_num


# calc Mc by MAXC method
def calc_mc_maxc(mag):
    mag_bin, num, _ = calc_fmd(mag)
    return mag_bin[np.argmax(num)]


# calc b_val to Mc relation
def calc_b2mc(mag):
    mag_min = np.floor(10 * min(mag)) / 10
    mag_max = np.ceil(10 * max(mag)) / 10
    mc_min = calc_mc_maxc(mag)
    mag_rng = np.arange(mc_min-1., mc_min+1.5, 0.1)
    b_val_dev = np.array([calc_b(mag[mag>mi]) for mi in mag_rng])
    return b_val_dev, mag_rng

