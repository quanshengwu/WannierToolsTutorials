import re
import numpy as np
import os

def parse_sigma_file(input_filename, mu=0.00):
    # Prepare regex for lists
    selbands_pattern = re.compile(r"^#\s*SELECTEDBANDS\s*=\s*(.*)")
    tlist_pattern = re.compile(r"^#\s*Tlist\s*=\s*(.*)")
    btaulist_pattern = re.compile(r"^#\s*Btaulist\s*=\s*(.*)")
    decimal_pattern = r"([+-]?\d*\.\d+(?:[eE][+-]?\d+)?)"

    # Read all lines
    with open(input_filename, 'r') as f:
        lines = f.readlines()

    # Extract Selected Bands, Tlist, Btaulist
    Nband = NumT = NumBtau = None
    T_array = None
    Btau_array = None
    for line in lines:
        m1 = selbands_pattern.match(line)
        if m1:
            bands = m1.group(1).split()
            Nband = len(bands)
            continue
        m2 = tlist_pattern.match(line)
        if m2:
            T_array = [float(val) for val in re.findall(decimal_pattern, m2.group(1))]
            NumT = len(T_array)
            continue
        m3 = btaulist_pattern.match(line)
        if m3:
            Btau_array = [float(val) for val in re.findall(decimal_pattern, m3.group(1))]
            NumBtau = len(Btau_array)
            continue
        if Nband and NumT and NumBtau:
            break

    # Validate
    if None in (Nband, NumT, NumBtau):
        raise ValueError("Failed to parse SELECTEDBANDS, Tlist, or Btaulist from file.")

    # Prepare output
    out_dir = "./"
    os.makedirs(out_dir, exist_ok=True)

    # Iterate lines for sigma blocks
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('#  iband'):
            rank_match = re.search(r"(\d+)", line)
            if not rank_match:
                i += 1
                continue
            band_rank = int(rank_match.group(1))

            # For each temperature
            for t_idx, T in enumerate(T_array, start=1):
                # seek to '# T' for this block
                while i < len(lines) and not lines[i].startswith('# T'):
                    i += 1
                if i >= len(lines):
                    break
                i += 1  # skip header

                # Read NumBtau rows of 11 columns
                data = []
                count = 0
                while i < len(lines) and count < NumBtau:
                    nums = re.findall(decimal_pattern, lines[i])
                    if len(nums) >= 10:
                        data.append([float(x) for x in nums[:11]])
                        count += 1
                    i += 1

                # Save if complete
                if count == NumBtau:
                    sigma = np.array(data)
                    fname = f"sigma_band_{band_rank}_mu_{mu:.2f}eV_T_{T:.2f}K.dat"
                    path = os.path.join(out_dir, fname)
                    np.savetxt(path, sigma, fmt="%.6e")
                    print(f"Saved: {path}")
                else:
                    print(f"Warning: band {band_rank}, T={T}: expected {NumBtau} rows, got {count}.")
        else:
            i += 1

if __name__ == '__main__':
    parse_sigma_file('sigma_bands_mu_0.0meV.dat', mu=0.00)
