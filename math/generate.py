"""Export a deterministic point approximation of the fixed Porous Lantern."""
import argparse
from pathlib import Path
import json
import numpy as np
from model import points, R, FACTOR


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--depth', type=int, default=5, choices=range(0, 8))
    p.add_argument('--output', type=Path, default=Path('.build/lantern.csv'))
    p.add_argument('--display-units', action='store_true')
    args = p.parse_args()
    data = points(args.depth)
    factor = FACTOR if args.display_units else 1.
    data *= factor
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(args.output, data, delimiter=',', header='x,y,z', comments='')
    print(json.dumps({'output': str(args.output), 'points': len(data),
                      'depth': args.depth, 'display_units': args.display_units,
                      'exact_point_set_Hausdorff_error_bound': factor*(27/20+1)*R**args.depth,
                      'note': 'Float coordinate errors are additional to the exact finite-set bound.'}, indent=2))


if __name__ == '__main__':
    main()
