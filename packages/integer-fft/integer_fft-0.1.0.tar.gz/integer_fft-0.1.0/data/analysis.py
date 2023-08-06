#!/usr/bin/env python
# coding: utf-8

# In[9]:


import numpy as np
import os
import matplotlib.pyplot as plt


# In[10]:


def bitswitch(arrin:np.ndarray,n:int):
    assert((1<<n)==len(arrin))
    arrout=np.zeros(len(arrin),dtype="complex")
    for idx,i in enumerate(arrin):
        bfi = int(0)
        for pos in range(n):
            bfi |= ((idx & (1 << pos)) >> pos) << (n - 1 - pos)
        arrout[bfi]=arrin[idx]
    return arrout


# In[30]:


basenames=["grn_"+"{}".format(i).zfill(4) for i in range(1000)]
for name in basenames[:5]:
    gr=np.load(f"{name}.npy") # gaussian random noise input
    gr=np.asarray(gr,dtype=np.float64)
    print(f"gr.std {(gr/35).std()}")
    re=np.load(f"{name}_out_real.npy")
    im=np.load(f"{name}_out_imag.npy")
    data_int=re+1.0j*im # complex out integer fft
    data_tru=np.fft.fft(gr) # complex out 'truth'
    # scale data to make same size as integer fft
    scale = (2**(8-11/2))*2**(1/2) # "true" data is scaled by this much compared to integer fft data
    data_tru/=scale
    # scale both data and integer data so that they have std=1
    scale_grn = 35 # the STD of gaussian random noise (where this come from? - that's just what i used for specific numpy data)
    data_tru/=scale_grn
    data_int/=scale_grn
    # the FFT scales by (log N) /2, so we need to divide by 11/2
    data_tru/= (11/2)
    data_int/= (11/2)
    print(f"data_tru.std {data_tru.std()}")
    print(f"data_tru.std {data_int.std()}\n")
    
#     # some magic
#     data_int=bitswitch(data_int,n=11)
#     data_tru=bitswitch(data_tru,n=11)


# In[38]:


sli=np.arange(0,2048) # slice, for viewing purposes

plt.figure()
# compute residuals
resid = np.real(data_int) - np.real(data_tru) + 1j*(np.imag(data_int) - np.imag(data_tru))

# compute error, deviation of integer FFT from 'truth'
rmse = np.sqrt(np.mean(abs(resid)**2))
std_resid = np.sqrt(np.std(np.real(resid))**2 + np.std(np.imag(resid))**2)

# plt.title("Residuals\nrmse={:.2e}   std={:.2e}".format(rmse,std_resid))
# # plt.plot(abs(resid)[sli],"x",label="abs")
# plt.plot(np.real(resid)[sli],"x",label="real")
# plt.plot(np.imag(resid)[sli],"x",label="imag")
# plt.legend()
# plt.show()

# Plot absolute value comparison
plt.subplots(figsize=(10,8))

plt.subplot(3,1,1)
plt.title("ABS")
plt.plot(np.abs(data_int[sli]),"x",label="integer fft")
plt.plot(np.abs(data_tru[sli]),".",label="truth")
plt.plot(np.abs(data_int[sli])-np.abs(data_tru[sli]),"o",label="abs_integer - abs_truth")
plt.legend()


# Plot real comparison
plt.subplot(3,1,2)
plt.title("REAL")
plt.plot(np.real(data_int[sli]),"x",label="integer fft")
plt.plot(np.real(data_tru[sli]),".",label="truth")
plt.plot(np.real(data_int[sli]) - np.real(data_tru[sli]),"o", label="int_fft - truth")
plt.legend()
plt.grid()


# Plot imaginary comparison
plt.subplot(3,1,3)
plt.title("IMAG")
plt.plot(np.imag(data_int[sli]),"x",label="integer fft")
plt.plot(np.imag(data_tru[sli]),".",label="truth")
plt.plot(np.imag(data_int[sli]) - np.imag(data_tru[sli]),"o", label="int_fft - truth")
plt.legend()
plt.grid()

plt.suptitle(f"Comparison Integer FFT vs Truth\nnbits_sin_coeffs={30}, nbits_data={30}, 2048-point integer FFT")

plt.tight_layout()
plt.show()


# In[40]:



# Plot absolute value comparison
plt.subplots(figsize=(10,8))

plt.subplot(3,1,1)
plt.title("ABS")
plt.plot(np.abs(data_int[sli])-np.abs(data_tru[sli]),"go",label="abs_integer - abs_truth")
plt.legend()


# Plot real comparison
plt.subplot(3,1,2)
plt.title("REAL")
plt.plot(np.real(data_int[sli]) - np.real(data_tru[sli]),"go", label="int_fft - truth")
plt.legend()
plt.grid()


# Plot imaginary comparison
plt.subplot(3,1,3)
plt.title("IMAG")
plt.plot(np.imag(data_int[sli]) - np.imag(data_tru[sli]),"go", label="int_fft - truth")
plt.legend()
plt.grid()

plt.suptitle(f"Comparison Resid Integer FFT vs Truth\nnbits_sin_coeffs={0}, nbits_data={0}, 2048-point integer FFT")

plt.tight_layout()
plt.show()


# In[14]:


# seq_real= # mysterious sequence
seq_real=np.ones(len(data_int))
seq_imag=np.ones(len(data_int))
seq_real[np.where(np.real(data_int)*np.real(data_tru)>0)]=0
seq_imag[np.where(np.imag(data_int)*np.imag(data_tru)>0)]=0
seq_real=np.array(seq_real,dtype=np.int32)
seq_imag=np.array(seq_imag,dtype=np.int32)
print("Imaginary")
for i in seq_imag:
    print(i,end="")
    
print("\n\nReal")
for i in seq_real:
    print(i,end="")
print(seq_real[:100])
seq_real

# autocorrelation
# plt.plot(ndi.convolve(seq_real,seq_real,mode="wrap"))
plt.plot(ndi.correlate(seq_real,seq_real,mode="wrap"),label="autocorr real wrap")
plt.plot(ndi.correlate(seq_imag,seq_imag,mode="wrap"),label="autocorr imag wrap")
# plt.plot(ndi.correlate(seq_imag,seq_real,mode="wrap"),label="corr real imag wrap")
plt.legend()
plt.title("Myster sequences")
plt.show()


# In[135]:


# rmses=[]
# stds=[]
# for i in np.linspace(4,8,50):
#     scale = (2**(i-11/2)) # integer fft scales data by this much
#     resid = np.real(data_int)*scale - np.real(data_tru) + 1j*(np.imag(data_int)*scale + np.imag(data_tru))
#     rmse = np.sqrt(np.mean(abs(resid)**2))
#     std = np.sqrt(np.std(np.real(resid))**2 + np.std(np.imag(resid))**2)
#     rmses.append(rmse)
#     stds.append(std)

# plt.figure()
# plt.plot(rmses)
# plt.plot(stds)
# plt.show()


# In[ ]:





# In[17]:


plt.plot(np.abs(data_int)*(1<<11),"x")
plt.plot(np.abs(data_int),".")


# In[ ]:




