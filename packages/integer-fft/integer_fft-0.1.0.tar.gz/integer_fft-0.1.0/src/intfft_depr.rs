extern crate npyz;

use crate::constants::{QUART_WAV, SINE};
use crate::complex::Complex;
use log::{debug, trace};

/// Copy complex array from a into b (utility function)
pub fn copy_ab(a: &[Complex], b: &mut [Complex]) {
    let len = a.len();
    assert!(len == b.len()); // check they are same size
    for idx in 0..len {
        b[idx] = a[idx];
    }
}

/// Takes a 2^n sized complex array, reverses binary index 01101 -> 10110
/// Puts values of flip into flop
fn bitswitch(flip: &[Complex], flop: &mut [Complex], n: usize) {
    for idx in 0..(1 << n) {
        // Bit Flipped Index
        let mut bfi: usize = 0;
        for pos in 0..n {
            bfi |= ((idx & (1 << pos)) >> pos) << (n - 1 - pos);
        }
        trace!("idx={:#b}, bfi={:#b}", idx, bfi);
        // copy the number at index idx into Bit-Flipped-Index (bfi)
        flop[bfi] = flip[idx];
    }
}

/// The core componant of FFTs, the butterfly stage.
/// Computes all twiddle factors and multiplies them appropriately.
fn butterfly(flip: &mut [Complex], flop: &mut [Complex], nsinebits: usize, n: usize) {
    //// For each stage of FFT, compute the twiddle factors and multiply
    let mut size: usize; // size of the current butterfly stage
    let mut numb: usize; // number of chunks of size 'size', numb*size=2^n
    for stage in 1..=n {
        // Copy flop back into flip
        copy_ab(&*flop, flip);
        trace!("\nButterfly stage #{}", stage);
        size = 1 << stage;
        numb = 1 << (n - stage);
        for chunk in 0..numb {
            for k in 0..(size / 2) {
                let mut d1 = flip[chunk * size + k];
                let twiddle = Complex::new(
                    SINE[QUART_WAV + numb * k * (2048 >> n)] >> (16 - nsinebits),
                    (-SINE[numb * k * (2048 >> n)]) >> (16 - nsinebits),
                );
                let mut d2 = flip[chunk * size + size / 2 + k] * twiddle;
                // normalize, twiddle factor is order 2^(nsinebits - 1)
                d2.bitshift_right(nsinebits - 1);
                // bitshift right by 1 prevent Butterfly overflow
                d1.bitshift_right(1);
                d2.bitshift_right(1);
                // Set next stage butterfly values
                flop[chunk * size + k] = d1 + d2;
                flop[chunk * size + k + size / 2] = d1 - d2;
            }
        }
    }
}

// Note on design choice: we always MANIPULATE data going from flip to
// flop, and then COPY data back from flop into flip. This is not the
// fastest way to do an FFT, but it makes for readable code.
pub fn int_fft(
    flip: &mut [Complex], // input (also gets modified)
    flop: &mut [Complex], // output
    nsinebits: usize,     // number of bits used to store sine coeffs
    ndatabits: usize,     // number of bits used to store our data
                          // ndatabits for each real and im componants
) {
    trace!("Starting basic tests and checks");
    // Our SINE lookup table is in i16, values in -2^15 to 2^15
    assert!(nsinebits <= 16);
    // Make sure length of arrays are a power of two
    let len = flip.len();
    assert!(len == flop.len());
    // initiate n: the log2 of len
    let mut n: usize = 0;
    // Loop to find what power of 2 len is, and check it really is one
    for i in 0..=12 {
        n = i;
        if len == (1 << n) {
            break; // break the loop at the correct power of two
        }
    }
    assert!(
        n < 12,
        "The length of our FFT must be a POWER OF TWO STRICTLY LESS than 12"
    );
    trace!("n = {}", n);
    trace!(
        "Clipping input data (flip) to {} bits to avoid overflow",
        ndatabits
    );
    for i in 0..len {
        flop[i] = flip[i].get_clipped_msb(ndatabits);
        if flop[i] != flip[i] {
            trace!("{} got clipped to {}", flip[i], flop[i]);
        }
    }
    // copy flop back into flip
    copy_ab(&*flop, flip);
    // TODO: refactor this for loop into a function used by all fft methods
    debug!("Starting Decimation In Time re-ordering");
    // data will be in flop after bitswitch
    bitswitch(flip, flop, n);
    trace!("Bit swich complete");
    // NB: flop is copied back into flip at every stage of the
    // butterfly so there is no need to copy it right now
    butterfly(flip, flop, nsinebits, n);
    // now data is in flop
}
