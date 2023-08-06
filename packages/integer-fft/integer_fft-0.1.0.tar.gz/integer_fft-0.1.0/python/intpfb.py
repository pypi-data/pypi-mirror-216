from integer_fft import integer_fft_2048 as intfft
import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt

NCHAN=1025
LFRAME=2*(NCHAN - 1)
NTAP=4


def int_pfb(ts):
    nblock = ts.size // LFRAME - (NTAP - 1)
    spec_re = np.zeros((nblock, LFRAME), dtype="int")
    spec_im = np.zeros((nblock, LFRAME), dtype="int")
    w=np.hanning(NTAP*LFRAME) * np.sinc(np.linspace(-NTAP/2, NTAP/2, LFRAME*NTAP+1))[:-1]
    # S matrix
    def s(ts_sec):
        return np.sum(ts_sec.reshape(NTAP,LFRAME),axis=0)
    # Iterate over blocks to perform PFB
    for bi in range(nblock):
        # cut out the correct timestream section
        ts_sec = ts[bi*LFRAME:(bi+NTAP)*LFRAME].copy()
        ts_sec_win = np.asarray(ts_sec * w + 0.4999999, dtype="int") 
        # perform a real DFT (with applied, chunked window)
        spec_re[bi], spec_im[bi] = intfft(
                s(ts_sec_win), 
                np.zeros(LFRAME,dtype="int")
                )

    return spec_re, spec_im

# floating point PFB, represents the truth
def true_pfb(ts):
    nblock = ts.size // LFRAME - (NTAP - 1)
    spec_re = np.zeros((nblock, LFRAME), dtype="int")
    spec_im = np.zeros((nblock, LFRAME), dtype="int")
    w=np.hanning(NTAP*LFRAME) * np.sinc(np.linspace(-NTAP/2, NTAP/2, LFRAME*NTAP+1))[:-1]
    # S matrix
    def s(ts_sec):
        return np.sum(ts_sec.reshape(NTAP,LFRAME),axis=0)
    # Iterate over blocks to perform PFB
    for bi in range(nblock):
        # cut out the correct timestream section
        ts_sec = ts[bi*LFRAME:(bi+NTAP)*LFRAME].copy()
        ts_sec_win = np.asarray(ts_sec * w + 0.4999999, dtype="int") 
        # perform a real DFT (with applied, chunked window)
        spec_bi = fft.fft(
                s(ts_sec_win)
                )
        spec_re[bi], spec_im[bi] = spec_bi.real, spec_bi.imag

    return spec_re, spec_im




if __name__=="__main__":
    ts = np.random.randn(LFRAME * 10000) * (1<<12)
    ts = np.asarray(ts, dtype="int")
    # saturate for 14 bit adcs
    saturate_up_idxs = np.where(ts > (1<<13))
    saturate_down_idxs = np.where(ts < -(1<<13))
    ts[saturate_up_idxs] = (1<<13)
    ts[saturate_down_idxs] = -(1<<13)

    # Compute integer pfb spectrum, write to disk
    int_spec_re, int_spec_im = int_pfb(ts)
    np.save("int_spec_re.npy", int_spec_re)
    np.save("int_spec_im.npy", int_spec_im)

    # Compute floating point pfb spectrum, write to disk
    fp_spec_re, fp_spec_im = true_pfb(ts)
    np.save("fp_spec_re.npy", fp_spec_re)
    np.save("fp_spec_im.npy", fp_spec_im)


    print(f"DEBUG: spec_re type {int_spec_re.dtype}, shape {int_spec_re.shape}, spec_im type {int_spec_im.dtype}, shape {int_spec_im.shape}")

    int_spec_abs = np.sqrt(int_spec_re**2 + int_spec_im**2)

    plt.figure()
    plt.imshow(int_spec_abs)
    plt.show()





