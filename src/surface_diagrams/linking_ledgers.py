"""Necessary positive full-twist ledgers from the COMPLETE pair-linking matrix.

This is a disk obstruction/target diagnostic, never a geometric chart match.
"""
from itertools import combinations
from .mapping_classes import VerificationLimitError


def positive_linking_ledgers(matrix, *, max_distinct_supports=4, max_work=20000):
    """Exhaust all aggregated positive clique ledgers within an explicit bound.

    A record supported on S contributes its positive power to every edge of S.
    Equal enclosed sets are aggregated ONLY for this necessary invariant. Their
    actual curve classes need not agree, so a ledger does not combine factors.
    Every endform of at most k records has at most k distinct support sets.
    """
    matrix=tuple(tuple(row) for row in matrix);n=len(matrix)
    if n<2 or any(len(row)!=n for row in matrix):raise ValueError('Use a square linking matrix')
    if any(type(x) is not int or x<0 for row in matrix for x in row):raise ValueError('Use nonnegative integer linking numbers')
    if any(matrix[i][i] or matrix[i][j]!=matrix[j][i] for i in range(n) for j in range(n)):
        raise ValueError('The linking matrix must be symmetric with zero diagonal')
    if any(type(x) is not int or x<1 for x in (max_distinct_supports,max_work)):
        raise ValueError('Use positive integer search bounds')
    edges=tuple(combinations(range(n),2));target=tuple(matrix[i][j] for i,j in edges)
    work=0
    def charge():
        nonlocal work
        work+=1
        if work>max_work:raise VerificationLimitError('Positive linking-ledger enumeration exhausted its work bound')
    candidates=[]
    for size in range(2,n+1):
        for support in combinations(range(n),size):
            charge()
            positions=tuple(k for k,(i,j) in enumerate(edges) if i in support and j in support)
            if all(target[k]>0 for k in positions):candidates.append((tuple(x+1 for x in support),positions))
    solutions=[]
    def visit(index,residual,chosen):
        charge()
        if not any(residual):solutions.append(tuple(chosen));return
        if index==len(candidates) or len(chosen)==max_distinct_supports:return
        support,positions=candidates[index]
        # Zero multiplicity and every possible positive multiplicity are retained.
        visit(index+1,residual,chosen)
        for power in range(1,min(residual[k] for k in positions)+1):
            changed=tuple(x-power if k in positions else x for k,x in enumerate(residual))
            visit(index+1,changed,chosen+[(support,power)])
    visit(0,target,[])
    return dict(strands=n,linking_matrix=matrix,candidate_supports=tuple(s for s,_ in candidates),
        ledgers=tuple(solutions),max_distinct_supports=max_distinct_supports,work=work,
        exhaustive_within_bound=True,minimum_distinct_supports=min(map(len,solutions)) if solutions else None,
        geometric_match_asserted=False,scope='Necessary aggregated support incidences only; no ordered product, common disk chart, factor combination, or reached substitution is inferred.')
