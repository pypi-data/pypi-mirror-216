// Simple complex data type, (simpler than num::complex::Complex)
#[derive(Copy, Clone)]
pub struct Complex {
    pub re: i64,
    pub im: i64,
}

/// Complex datatype
impl Complex {
    /// Create a new complex number
    pub fn new(re: i64, im: i64) -> Complex {
        // Initiate and return complex number
        Complex { re: re, im: im }
    }
    /// Bitshift both real and imaginary components right by `n` bits
    pub fn bitshift_right(&mut self, n: usize) {
        self.re >>= n;
        self.im >>= n;
    }
    /// Clip to select the `nbits_keep` least significant bits
    pub fn get_clipped_msb(self, nbits_keep: usize) -> Complex {
        let mut re: i64 = self.re;
        let mut im: i64 = self.im;
        // saturate
        if self.re >= 1 << (nbits_keep - 1) {
            re = (1 << (nbits_keep - 1)) - 1;
        } else if self.re <= -1 << (nbits_keep - 1) {
            re = -1 << (nbits_keep - 1);
        }
        if self.im >= 1 << (nbits_keep - 1) {
            im = (1 << (nbits_keep - 1)) - 1
        } else if self.im <= -1 << (nbits_keep - 1) {
            im = -1 << (nbits_keep - 1);
        }
        Self::new(re, im)
    }
}

impl std::fmt::Display for Complex {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if self.im >= 0 {
            write!(f, "{}+{}j", self.re, self.im)
        } else {
            write!(f, "{}{}j", self.re, self.im)
        }
    }
}

impl std::ops::Add for Complex {
    type Output = Complex;
    fn add(self, rhs: Complex) -> Complex {
        Complex::new(rhs.re + self.re, rhs.im + self.im)
    }
}

impl std::ops::Sub for Complex {
    type Output = Complex;
    fn sub(self, rhs: Complex) -> Complex {
        Complex::new(self.re - rhs.re, self.im - rhs.im)
    }
}

impl std::ops::Mul for Complex {
    type Output = Complex;
    fn mul(self, rhs: Complex) -> Complex {
        Complex::new(
            rhs.re * self.re - rhs.im * self.im,
            rhs.re * self.im + rhs.im * self.re,
        )
    }
}

impl PartialEq for Complex {
    fn eq(&self, rhs: &Self) -> bool {
        self.re == rhs.re && self.im == rhs.im
    }
}
