import argparse
import os
from asltk.asldata import ASLData
from asltk.registration.asl_normalization import head_movement_correction
from asltk.utils.io import save_image, load_image
from asltk.reconstruction.multi_te_mapping import MultiTE_ASLMapping
from rich import print
import numpy as np

def main():
    parser = argparse.ArgumentParser(
        description="Run ASL mapping experiment with PCASL and M0 images."
    )
    parser.add_argument(
        "--pcasl", required=True, type=str, help="Full path to the ASL PCASL image"
    )
    parser.add_argument(
        "--m0", required=True, type=str, help="Full path to the ASL M0 image"
    )
    args = parser.parse_args()


    pcasl_path = args.pcasl
    m0_path = args.m0

    basepath = os.path.dirname(os.path.abspath(pcasl_path))

    # Adopting default values for the parameters (LOAMRI pattern)
    ld_values=[100.0, 100.0, 150.0, 150.0, 400.0, 800.0, 1800.0],
    pld_values=[170.0, 270.0, 370.0, 520.0, 670.0, 1070.0, 1870.0],
    te_values=[13.56, 67.82, 122.08, 176.33, 230.59, 284.84, 339.100, 393.36],

    # Load images
    pcasl_img = load_image(pcasl_path)
    m0_img = load_image(m0_path)

    # Check if m0 image is 4D
    m0_is_4D = False
    if m0_img.ndim > 3:
        print(f"M0 image is expected to be 4D, got {m0_img.ndim}D instead. Adopting average across time dimension.")
        m0_is_4D = True

    # Load ASL data
    print(f"[bold green]Loading ASLData from:[/bold green] {pcasl_path} and {m0_path}")
    average_m0 = False
    if m0_is_4D:
        average_m0 = True
    asl_data = ASLData(
        pcasl=pcasl_img,
        m0=m0_img,
        ld_values=[100.0, 100.0, 150.0, 150.0, 400.0, 800.0, 1800.0],
        pld_values=[170.0, 270.0, 370.0, 520.0, 670.0, 1070.0, 1870.0],
        te_values=[13.56, 67.82, 122.08, 176.33, 230.59, 284.84, 339.100, 393.36],
        average_m0=average_m0
    )

    # Perform head movement correction
    print("[bold green]Performing head movement correction...[/bold green]")
    asl_data_corr, _ = head_movement_correction(asl_data)

    # Run mapping - Original data
    print("[bold green]Running create_map()[/bold green]")
    mte = MultiTE_ASLMapping(asl_data)
    mte.set_brain_mask(load_image(os.path.join(basepath, "m0_brain_mask.nii.gz")))
    results_orig = mte.create_map()

    # Run mapping - Corrected data
    print("[bold green]Running create_map() on corrected data[/bold green]")
    mte_corr = MultiTE_ASLMapping(asl_data_corr)
    mte_corr.set_brain_mask(load_image(os.path.join(basepath, "m0_brain_mask.nii.gz")))
    results_corr = mte_corr.create_map()

    # Save outputs
    output_dir = basepath
    for key in ['cbf_norm', 'att', 't1blgm']:
        if key in results_orig:
            out_path = os.path.join(output_dir, f"{key}_orig.nii.gz")
            print(f"[bold blue]Saving {key} to {out_path}[/bold blue]")
            save_image(results_orig[key], out_path)
        else:
            print(f"[yellow]Warning: {key} not found in results.[/yellow]")

    for key in ['cbf_norm', 'att', 't1blgm']:
        if key in results_corr:
            out_path = os.path.join(output_dir, f"{key}_corr.nii.gz")
            print(f"[bold blue]Saving {key} to {out_path}[/bold blue]")
            save_image(results_corr[key], out_path)
        else:
            print(f"[yellow]Warning: {key} not found in results.[/yellow]")

if __name__ == "__main__":
    main()