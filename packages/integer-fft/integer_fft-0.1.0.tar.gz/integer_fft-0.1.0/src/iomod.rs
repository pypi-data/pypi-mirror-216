extern crate npyz;

use crate::complex::Complex;
use npyz::WriterBuilder;
use std::fs::File;
use std::io;

// Loads numpy 2048-szed array of 32 bit integers from .npy file into
// a Complex array arr
pub fn read_npyi32(
    fname: &String,
    arr: &mut [Complex; 2048],
    inbitshift: usize,
) -> Result<(), Box<dyn std::error::Error>> {
    let bytes = std::fs::read(fname)?;
    let npy = npyz::NpyFile::new(&bytes[..])?;
    let mut count = 0;
    for number in npy.data::<i32>()? {
        let mut n64: i64 = number?.into();
        n64 = n64 << inbitshift;
        if n64 > std::i32::MAX as i64 {
            n64 = std::i32::MAX as i64;
        } else if n64 < std::i32::MIN as i64 {
            n64 = std::i32::MIN as i64;
        }
        arr[count] = Complex::new(n64, 0);
        count += 1;
    }
    Ok(())
}

// writerimag: impl io::Write,
// Serializes output in the .npy format
pub fn output_to_npy(
    fname_real: &String,
    fname_imag: &String,
    arr: &[Complex; 2048],
) -> io::Result<()> {
    let writerreal = File::create(fname_real)?;
    let writerimag = File::create(fname_imag)?;
    let mut writerreal = {
        npyz::WriteOptions::new()
            .default_dtype()
            .shape(&[2048])
            .writer(writerreal)
            .begin_nd()?
    };
    let mut writerimag = {
        npyz::WriteOptions::new()
            .default_dtype()
            .shape(&[2048])
            .writer(writerimag)
            .begin_nd()?
    };
    for c in arr.iter() {
        writerreal.push(&c.re)?;
        writerimag.push(&c.im)?;
    }
    Ok(())
}
