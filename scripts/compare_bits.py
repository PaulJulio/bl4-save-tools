import yaml
import sys
from pathlib import Path

sys.path.append('scripts')
from bank_report import bit_pack_decode

def main():
    # Known Heavy Weapons from reference_vex_heavy.yaml
    heavy_serials = ['@Ugr$%Mm/)}}!dP6OK`m-hj~Y5u2LS', '@Ugr$%Mm/)}}!boeNH>gE5DpHdgI#j7obt-)s00', '@Ugr$%Mm/)}}!bsYnH>gEDYEnaoE;R-f29>@A00']
    heavy_bits = [bit_pack_decode(s) for s in heavy_serials]
    
    # Known Grenades from reference_vex_grenades.yaml with same signature
    grenade_serials = ['@Ugr$)Nm/)}}!dTs)M^$Qlc/eU?-%J1', '@Ugr$)Nm/)}}!bk%ps#5Et!680`i(nE5']
    grenade_bits = [bit_pack_decode(s) for s in grenade_serials]
    
    maxlen = max(len(b) for b in heavy_bits + grenade_bits)
    for i in range(maxlen):
        h_vals = set(b[i] for b in heavy_bits if i < len(b))
        g_vals = set(b[i] for b in grenade_bits if i < len(b))
        
        if h_vals and g_vals and h_vals != g_vals:
            if len(h_vals) == 1 and len(g_vals) == 1:
                print(f"Bit {i}: Heavy={list(h_vals)[0]}, Grenade={list(g_vals)[0]}")

if __name__ == "__main__":
    main()
