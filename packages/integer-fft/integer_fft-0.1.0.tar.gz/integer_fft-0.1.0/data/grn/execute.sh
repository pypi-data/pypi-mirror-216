#!/opt/homebrew/bin/zsh
cargo build --release;
rm fftrs;
cp ../../target/release/fftrs ./;
for i in {0..999}
do
  strn=$(printf %04d $i)
  RUST_LOG=info ./fftrs grn_$strn.npy 8 62 16
done
