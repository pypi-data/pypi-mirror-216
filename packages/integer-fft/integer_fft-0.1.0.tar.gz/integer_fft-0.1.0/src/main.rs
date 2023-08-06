extern crate env_logger;
extern crate npyz;
extern crate integer_fft; // our library

use integer_fft::complex::Complex;
use integer_fft::constants::{QUART_WAV, SINE};
use integer_fft::intfft::{copy_ab, int_fft};
//use integer_fft::iomod::{output_to_npy, read_npyi32};
use log::{debug, info, trace};
use std::env; // retrieve arguments

/// Log a trace of the array
fn trace_array(arr: &[Complex]) {
    for c in arr.iter() {
        trace!("{}, ", c);
    }
}

/// Display a complex array with println!
fn display_array(arr: &[Complex]) {
    for c in arr.iter() {
        println!("({})", c);
    }
}

/// Display just the head of a complex array in debug!
fn display_array_head(arr: &[Complex], n: usize) {
    for i in 0..n {
        debug!("({})", arr[i]);
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    env_logger::init();
    info!("Initiating parameters and arrays");
    let args: Vec<String> = env::args().collect();
    // Begin ------ Change these to fit your needs
    let fname: &String = &args[1]; // Command line argument is the name of file
    //let inbitshift: usize = args[2].parse().unwrap(); // number of bits to shift input (left, see io)
    let ndatabits: usize = args[3].parse().unwrap(); // = 18; // max (64-16-2)/2 = 23 bits
    let nsinebits: usize = args[4].parse().unwrap(); // = 16; // max 16 bits
                                                     // End ------ Change these to fit your needs

    // initiate flip and flop data arrays
    let mut flip: Vec<Complex> = Vec::from([Complex::new(0, 0); 2048]);
    let mut flop: Vec<Complex> = Vec::from([Complex::new(0, 0); 2048]);
    // read file fname into flip array
    //read_npyi32(fname, &mut flip, inbitshift)?;

    // DFT the input
    debug!("Array head of input file");
    display_array_head(&flip, 5);
    info!("Executing FFT logic");
    int_fft(&mut flip, &mut flop, 11u32, nsinebits, ndatabits);
    debug!("Array head of DFT of the input file");
    display_array_head(&flop, 5);

    // Write to .npy file
    let mut fname_real: String = fname.clone();
    let mut fname_imag: String = fname.clone();
    fname_real.truncate(fname_real.len() - 4);
    fname_real.push_str("_out_real.npy");
    fname_imag.truncate(fname_imag.len() - 4);
    fname_imag.push_str("_out_imag.npy");

    //output_to_npy(&fname_real, &fname_imag, &flop)?;
    info!("Done");
    Ok(())
}

// ------------------------------------------------------------------------------
// ------------------------------------------------------------------------------
// EVERYTHING BEYOND THIS POINT IS USED ONLY FOR TESTING OTHER CODE

// Simple three-stage DFT Radix-2 DIT
#[allow(dead_code)]
fn fft8(flip: &mut Vec<Complex>, flop: &mut Vec<Complex>) {
    // Decimation in time re-ordering, flip -> flop
    for idx in 0usize..8 {
        // Bit flipped idx
        let mut bfi: usize = 0;
        for pos in 0u8..=2 {
            bfi |= ((idx & (1 << pos)) >> pos) << (2 - pos);
        }
        trace!("idx={}, bfi={}", idx, bfi);
        // Copy the number at idx into bit-flipped-index
        flop[bfi] = flip[idx];
    }
    trace!("Bit-switch complete, result for flop:");
    trace_array(&*flop);
    trace!("Flip is:");
    trace_array(&*flip);
    // For each stage, compute the twiddle factors
    let mut size: usize; // size of the current butterfly stage
    let mut numb: usize; // number of chunks of size 'size', numb*size=8
    for stage in 1..=3 {
        // Copy flop back into flip
        copy_ab(&*flop, flip);
        trace!("\nButterfly stage {}", stage);
        size = 1 << stage;
        numb = 1 << (3 - stage);
        for chunk in 0..numb {
            for k in 0..(size / 2) {
                let mut d1 = flip[chunk * size + k];
                let twiddle = Complex::new(
                    SINE[QUART_WAV + numb * k * 2048 / 8], // cos
                    -SINE[numb * k * 2048 / 8],            // i*sin
                );
                let mut d2 = flip[chunk * size + size / 2 + k] * twiddle;
                d2.bitshift_right(15); // normalize, twiddle factor too big
                                       // bitshift right by 1 prevent Butterfly overflow
                d1.bitshift_right(1);
                d2.bitshift_right(1);
                flop[chunk * size + k] = d1 + d2;
                flop[chunk * size + k + size / 2] = d1 - d2;
            }
            trace!("\nchunk={}", chunk);
            display_array(&*flop);
        }
    }
}

#[allow(dead_code)]
fn fft2048(flip: &mut Vec<Complex>, flop: &mut Vec<Complex>) {
    // Decimation in time re-ordering, flip -> flop
    for idx in 0usize..2048 {
        // Bit flipped idx
        let mut bfi: usize = 0;
        for pos in 0..=10 {
            bfi |= ((idx & (1 << pos)) >> pos) << (10 - pos);
        }
        trace!("idx={:#b}, bfi={:#b}", idx, bfi);
        // Copy the number at idx into bit-flipped-index
        flop[bfi] = flip[idx];
    }
    // For each stage, compute the twiddle factors
    let mut size: usize; // size of the current butterfly stage
    let mut numb: usize; // number of chunks of size 'size', numb*size=8
    for stage in 1u32..=11 {
        // Copy flop back into flip
        copy_ab(&*flop, flip);
        trace!("\nButterfly stage #{}", stage);
        size = 1 << stage;
        numb = 1 << (11 - stage);
        for chunk in 0usize..numb {
            for k in 0usize..(size / 2) {
                let mut d1 = flip[chunk * size + k];
                let twiddle = Complex::new(SINE[QUART_WAV + numb * k], -SINE[numb * k]);
                let mut d2 = flip[chunk * size + size / 2 + k] * twiddle;
                d2.bitshift_right(15); // normalize, twiddle factor is order 2^15
                                       // bitshift right by 1 prevent Butterfly overflow
                d1.bitshift_right(1);
                d2.bitshift_right(1);
                flop[chunk * size + k] = d1 + d2;
                flop[chunk * size + k + size / 2] = d1 - d2;
            }
        }
    }
}

// FFT for any power of two up to and including 2048
#[allow(dead_code)]
fn fft(flip: &mut Vec::<Complex>, flop: &mut Vec<Complex>) {
    // Make sure length of arrays are a power of two
    let len = flip.len();
    assert!(len == flop.len());
    // init n: the logarithm of len, such that 2^n == len
    let mut n: usize = 0;
    // Loop to figure out what power of 2 len is and to check it is one
    for i in 0..=12 {
        n = i;
        if len == (1 << n) {
            break; // break the loop at the right power of two
        }
    }
    assert!(
        n < 12,
        "The length of our FFT must be a POWER OF TWO STRICTLY LESS than 12"
    );
    trace!("n = {}", n);
    // Decimation in time re-ordering, flip -> flop
    for idx in 0..len {
        // Bit Flipped Index
        let mut bfi: usize = 0;
        for pos in 0..n {
            bfi |= ((idx & (1 << pos)) >> pos) << (n - 1 - pos);
        }
        trace!("idx={}, bfi={}", idx, bfi);
        // Copy the number at index idx into Bit-Flipped-Index (bfi)
        flop[bfi] = flip[idx];
    }
    trace!("Bit-swich complete; result for flop:");
    trace_array(&*flop);
    trace!("Flip is:");
    trace_array(&*flip);
    // For each stage, compute the twiddle factors
    let mut size: usize; // size of the current butterfly stage
    let mut numb: usize; // number of chunks of size 'size', numb*size=len
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
                    SINE[QUART_WAV + numb * k * (2048 >> n)],
                    -SINE[numb * k * (2048 >> n)],
                );
                let mut d2 = flip[chunk * size + size / 2 + k] * twiddle;
                // normalize, twiddle factor is order 2^15
                d2.bitshift_right(15);
                // bitshift right by 1 prevent Butterfly overflow
                d1.bitshift_right(1);
                d2.bitshift_right(1);
                flop[chunk * size + k] = d1 + d2;
                flop[chunk * size + k + size / 2] = d1 - d2;
            }
        }
    }
}

#[cfg(test)]
mod test {
    use super::*;

    #[test]
    fn test_complex() {
        let _c = Complex::new(3, 1);
    }

    #[test]
    fn test_fft() {
        // Perform an fft, see if it breaks
        let mut flip: Vec<Complex> = Vec::from([Complex::new(1000, 0); 8]);
        let mut flop: Vec<Complex> = Vec::from([Complex::new(1000, 0); 8]);
        fft(&mut flip, &mut flop);

        // Compare output with output of fft8, should be exact same
        let mut flip8: Vec<Complex> = Vec::from([Complex::new(1000, 0); 8]);
        let mut flop8: Vec<Complex> = Vec::from([Complex::new(1000, 0); 8]);
        fft8(&mut flip8, &mut flop8);
        for i in 0..8 {
            assert!(flip[i] == flip8[i]);
            assert!(flop[i] == flop8[i]);
        }

        //// Compare output with fft2048, should be exact same
        // Perform 2048 point FFT with fft2048()
        let mut flip2048: Vec<Complex> = Vec::from([Complex::new(100, 0); 2048]);
        let mut flop2048: Vec<Complex> = Vec::from([Complex::new(0, 0); 2048]);
        fft2048(&mut flip2048, &mut flop2048);
        // Perform 2048 point FFT with fft()
        let mut flip: Vec<Complex> = Vec::from([Complex::new(100, 0); 2048]);
        let mut flop: Vec<Complex> = Vec::from([Complex::new(0, 0); 2048]);
        fft(&mut flip, &mut flop);
        for i in 0..2048 {
            assert!(flip[i] == flip2048[i]);
            assert!(flop[i] == flop2048[i]);
        }
    }

    #[test]
    fn test_int_fft() {
        // Perform an int_fft, see if it breaks
        let mut flip: Vec<Complex> = Vec::from([Complex::new(100, 0); 8]);
        let mut flop: Vec<Complex> = Vec::from([Complex::new(100, 0); 8]);
        int_fft(&mut flip, &mut flop, 3, 16, 16);
        // Compare output with other integer FFT
        let mut flip2: Vec<Complex> = Vec::from([Complex::new(100, 0); 8]);
        let mut flop2: Vec<Complex> = Vec::from([Complex::new(100, 0); 8]);
        fft(&mut flip2, &mut flop2);
        for i in 0..8 {
            assert!(flip[i] == flip2[i]);
            assert!(flop[i] == flop2[i]);
        }
    }

    #[test]
    fn test_int_fft2() {
        // Perform an int_fft, see if it breaks
        let mut flip: Vec<Complex> = Vec::from([Complex::new(100, 0); 2048]);
        let mut flop: Vec<Complex> = Vec::from([Complex::new(100, 0); 2048]);
        int_fft(&mut flip, &mut flop, 11, 16, 16);
        // Compare output with other integer FFT
        let mut flip2: Vec<Complex> = Vec::from([Complex::new(100, 0); 2048]);
        let mut flop2: Vec<Complex> = Vec::from([Complex::new(100, 0); 2048]);
        fft(&mut flip2, &mut flop2);
        for i in 0..2048 {
            assert!(flip[i] == flip2[i]);
            assert!(flop[i] == flop2[i]);
        }
    }

    // To see clip output run: RUST_LOG=trace cargo test -- --nocapture
    #[test]
    fn test_fft_clipped() {
        // Perform an int_fft with larger values than it can take
        let mut flip: Vec<Complex> = Vec::from([Complex::new(100, 0); 8]);
        let mut flop: Vec<Complex> = Vec::from([Complex::new(100, 0); 8]);
        int_fft(&mut flip, &mut flop, 3, 8, 8);
    }

    #[test]
    fn test_copy_ab() {
        // copy a into b
        let a: Vec<Complex> = Vec::from([Complex::new(1, 1); 8]);
        let mut b: Vec<Complex> = Vec::from([Complex::new(0, 0); 8]);
        copy_ab(&a, &mut b);
        for (ai, bi) in a.iter().zip(b.iter()) {
            assert!(ai == bi);
        }
    }

    #[test]
    fn test_copy_ab_vec() {
        // copy a into b
        let a: Vec<Complex> = Vec::from([Complex::new(1, 1); 8]);
        let mut b: Vec<Complex> = Vec::from([Complex::new(0, 0); 8]);
        copy_ab(&a, &mut b);
        for (ai, bi) in a.iter().zip(b.iter()) {
            assert!(ai == bi);
        }
    }

    #[test]
    fn test_get_clipped_msb() {
        let mut c0 = Complex::new(1, -5);
        c0 = c0.get_clipped_msb(5);
        assert!(c0 == Complex::new(1, -5));
        let mut c1 = Complex::new(1, -5);
        c1 = c1.get_clipped_msb(3);
        println!("c1={}", c1);
        assert!(c1 == Complex::new(1, -4));
        let mut c2 = Complex::new(-4, 4);
        c2 = c2.get_clipped_msb(2);
        assert!(c2 == Complex::new(-2, 1));
        let mut c3 = Complex::new(8, 5);
        c3 = c3.get_clipped_msb(4);
        assert!(c3 == Complex::new(7, 5));
    }
}
