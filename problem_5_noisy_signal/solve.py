import numpy as np

def gaussian_filter(sigma=1, size=5):
    k = size // 2
    xs = [np.exp(-(z*z)/2*sigma**2) for z in range(-k, k+1)]
    xs = xs / np.sum(xs)
    return xs

def flat_filter(size=5):
    return np.ones((size, )) / size

def smooth(x,window_len=11,window='hanning'):

    assert x.ndim == 1,"smooth only accepts 1 dimension arrays."
    assert x.size >= window_len, "Input vector needs to be bigger than window size."

    if window_len<3:
        return x

    assert window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman'], "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s = np.r_[x[window_len-1:0:-1], x, x[-2:-window_len-1:-1]]

    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    return np.convolve(w / w.sum(), s, mode='valid')
