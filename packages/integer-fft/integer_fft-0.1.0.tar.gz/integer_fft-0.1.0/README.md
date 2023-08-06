# How to use

This program performs a 2048 point integer FFT on 32 bit integer data in numpy serialized arrays, files with the `.npy` extention. If you'd like to add flexibility, feel free to play with the code, I did my best to make it easy to adapt. 

Clone this repository

```
git clone https://github.com/dcxSt/dft_algos.git
```

Change directory 

```
cd dft_algos/fftrs
```

Build the binaries with cargo (install instructions for cargo [here](https://doc.rust-lang.org/cargo/getting-started/installation.html))

```
cargo build --release
```

Copy the binary program that you just compiled into, wherever you want it to be (perhaps the same place as your simulated data)

```
cp target/release/fftrs /any/directory/you/want/
```

Go into the directory you just copied the binary into. Run the program, supplying three arguments

```
./fftrs <name of npy file.npy> <nbitshift> <number of bits for data> <number of sine bits>
```

The number of bits to shift the input (so that the inter-butterfly stage scaling doesn't kill the signal) is the first input `<nbitshift>` after the name of the npy file. The number of sine bits `<number of sine bits>` can be at most 16, and the number of bits used for the real and imaginary parts, each. Since we are doing 64bit integers, this number must be at most 23, because 23 + 23 + 16 + 2 = 64, (the plus two is because we add things together and it's to prevent overflow). 

For instance

```
./fftrs dc100.npy 8 18 16
```

It will output the DFT info files `<input_file_basename>_out_real.npy` and `<output_file_basename>_out_imag.npy`. Have fun. 



## Dev Notes

*Reminder:* The optimal STD to select for the FT of an 8-bit quantized input is 35. I.e. when generating simulated data scale your gaussian noise by 35 before throwing converting to int and throwing it into the integer FFT. 

*Remark:* if you'd like to display trace, debug or info logging statements, run `RUST_LOG=trace cargo run`

`pyo3` breaks if on Apple's ARM machines if you don't have the following in your `~/cargo/config`, [as pointed out by Dennis in StackOverflow](https://stackoverflow.com/questions/28124221/error-linking-with-cc-failed-exit-code-1)

```toml
[target.x86_64-apple-darwin]
rustflags = [
  "-C", "link-arg=-undefined",
  "-C", "link-arg=dynamic_lookup",
]

[target.aarch64-apple-darwin]
rustflags = [
  "-C", "link-arg=-undefined",
  "-C", "link-arg=dynamic_lookup",
]
```

## TODO
- [x] python bindings
- [ ] Refactor naming convention, put thought into this
- [ ] variable sized power-of-two FFTs
    - [ ] Switch to vector instead of static sized array?
- [ ] increase capacity (sine way up to 1<<16 instead of 1<<11)

- [ ] Change twiddle factors to 32i to expand range
- [ ] Change how it's coded so that rounding of twiddle factors is done *well* not just with the bitshift operator >> will induce bias, make sine smaller than it should be
- [ ] Write python script to generate bunch of `.npy` gaussian random noise
- [ ] Write python script to load all input and output data and make some plots comparing integer fft and true ffts
- [ ] extend bash script to generate random noise (by executing python file), execute integer fft with all the knobs and bells, then execute another python file to plot the output and save the plots. 

## Debugging 

(previous) output of `cargo run`

```
before fft8: 0 + i 0
idx=0, bfi=0
idx=1, bfi=4
idx=2, bfi=2
idx=3, bfi=6
idx=4, bfi=1
idx=5, bfi=5
idx=6, bfi=3
idx=7, bfi=7
DEBUG: bit-switch complete, result:
[1000+i0, 1000+i0, 1000+i0, 1000+i0, 1000+i0, 1000+i0, 1000+i0, 1000+i0, ]
----------------------

DEBUG: stage 1

DEBUG: chunk=0
[1999+i0, -1+i0, 1000+i0, 1000+i0, 1000+i0, 1000+i0, 1000+i0, 1000+i0, ]

DEBUG: chunk=1
[1999+i0, -1+i0, 1999+i0, -1+i0, 1000+i0, 1000+i0, 1000+i0, 1000+i0, ]

DEBUG: chunk=2
[1999+i0, -1+i0, 1999+i0, -1+i0, 1999+i0, -1+i0, 1000+i0, 1000+i0, ]

DEBUG: chunk=3
[1999+i0, -1+i0, 1999+i0, -1+i0, 1999+i0, -1+i0, 1999+i0, -1+i0, ]
----------------------

DEBUG: stage 2

DEBUG: chunk=0
[3997+i0, -1+i-1, -1+i0, 1+i-1, 1999+i0, -1+i0, 1999+i0, -1+i0, ]

DEBUG: chunk=1
[3997+i0, -1+i-1, -1+i0, 1+i-1, 3997+i0, -1+i-1, -1+i0, 1+i-1, ]
----------------------

DEBUG: stage 3

DEBUG: chunk=0
[7993+i0, -1+i-3, -1+i-1, 1+i0, -1+i0, 1+i-1, 1+i-1, -1+i2, ]
DEBUG: #2
After fft8: 7993 + i 0
7u16 in bits: 0000000000000111
one 00000001
n_one 11111111

Out:

[7993+i0, -1+i-3, -1+i-1, 1+i0, -1+i0, 1+i-1, 1+i-1, -1+i2, ]
```



