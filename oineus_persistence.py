import argparse
import sys

import numpy as np


def compute_diagram(input_dataset):
    # read Perseus Cubical Grid
    with open(input_dataset) as src:
        dim = int(src.readline())
        extent = [0] * dim
        for i in range(dim):
            extent[i] = int(src.readline())
        data = np.fromfile(src, dtype=np.int32, count=-1, sep="\n")
        grid = data.reshape(extent)

        import oineus

        # compute diagram
        return oineus.compute_diagrams_ls(
            grid,
            negate=False,
            wrap=False,
            top_d=3,
            n_threads=4,
        )


def main(input_dataset, output_diagram):
    diag = compute_diagram(input_dataset)
    with open(output_diagram, "w") as dst:
        for i, pairs in enumerate(diag):
            for pair in pairs:
                dst.write(f"{i} {pair[0]} {pair[1]}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply Oineus on the given dataset")

    parser.add_argument(
        "input_dataset",
        type=str,
        help="Path to input dataset",
        default="datasets/fuel_64x64x64_uint8_order_impl.pers",
    )
    parser.add_argument(
        "-o",
        "--output_diagram",
        type=str,
        help="Output diagram file name",
        default="out.gudhi",
    )
    parser.add_argument(
        "-p",
        "--oineus_path",
        type=str,
        help="Path to Oineus Python module",
        default="build_oineus/bindings/python",
    )

    args = parser.parse_args()
    sys.path.append(args.oineus_path)
    main(args.input_dataset, args.output_diagram)
