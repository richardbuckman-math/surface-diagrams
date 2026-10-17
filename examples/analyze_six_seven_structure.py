"""Print reproducible structural certificates for the continuing (6,7) search."""
import json
from dataclasses import asdict
from surface_diagrams.factorization_explorer import initial_factors
from surface_diagrams.six_seven_structure import (
    nonseparating_intersection_certificate, six_seven_lattice_certificate,
    sphere_genus_two_lantern,
)

if __name__=='__main__':
    lantern=sphere_genus_two_lantern()
    for side in ('left','right'):
        lantern[side]=[dict(asdict(f),word=f.word) for f in lantern[side]]
    print(json.dumps(dict(
        intersection_obstruction=nonseparating_intersection_certificate(initial_factors()),
        rank_two_monodromy=six_seven_lattice_certificate(),
        sphere_lantern=lantern,
        complete_structural_derivation_found=False),indent=2))
