# Exact point-pushing separation of the early chart

The published named graphical derivation is complete at **121 steps**, including
four explicit sphere operations. This calculation does **not** shorten that
route. It makes the proposed four-strand shortcut testable without discarding
its point-pushing kernel.

## Disk decomposition

For a disk braid fixing the last of n strands, ordinary deletion maps to
B_(n-1). Its kernel is the free point-pushing group on n-1 generators. Use

    P_i = sigma_(n-1)^-1 ... sigma_(i+1)^-1 sigma_i^2
          sigma_(i+1) ... sigma_(n-1).

These are the positive pair twists whose arcs pass under intervening points.
In this package's right-composition convention, P_i pushes along x_i and
`push(a b) = push(b) push(a)`. Every stabilizing braid has the exact disk form

    braid = push(loop) * embedded_shadow.

`split_fixed_last_strand()` retains **both** terms and an explicit reconstructed
braid word. This is not `puncture_to_boundary()`: no point is made exterior, no
complementary twist or boundary correction is removed, and no sphere move occurs.
In particular, P_i has an empty deletion shadow but remains nontrivial.

The algorithm uses negative Schreier representatives
`r_j = sigma_(n-1)^-1 ... sigma_j^-1`. Each original crossing becomes an ordinary
shadow generator, P_i, its inverse, or the identity. The retained edge records
track the moving last strand. Collecting P_i past the accumulated shadow uses
its exact action on n-1 meridians. It never expands the full source braid's
n-meridian action, searches for a geometric route, or infers disk equality from
endpoint matching. A reversed reduction stack collects the pushing loop without
repeatedly copying its entire prefix. Word/work exhaustion raises
`VerificationLimitError`; a partial result is never a certificate.

Independent tests check every signed Schreier edge for n=2 through 7, 200 mixed
random reconstructions against the faithful Artin action, the pushing basis and
multiplication order, known common frames, retained boundary kernels, and bounds.

## An exact exclusion of the simplest common-frame shortcut

Suppose the early half twists could all be placed in the same embedded B4 by
ONE common disk conjugation fixing point 5. Since B4 normalizes its own
inclusion, it suffices to conjugate by a point push z. For a split
`push(l_i) d_i`, the required free-group equation is

    l_i z = A(d_i)(z).

Abelianizing gives `(D_i - I) Z = L_i`, where D_i is the shadow permutation and
L_i is the exponent vector of the **retained** pushing loop. These are integer
difference constraints. A cycle with nonzero sum rigorously excludes a common
frame. Consistent constraints are only **inconclusive**.

For the four halves in the original early fourteen-factor chart:

| Half | Shadow permutation | Pushing exponents (x1,x2,x3,x4) |
| --- | --- | --- |
| F3 | (1 3) | (-1,0,1,0) |
| F9 | (1 3) | (1,0,-1,0) |
| F6 | (2 4) | (0,0,0,0) |
| F11 | (2 4) | (0,2,0,-2) |

F3 requires Z3-Z1=-1, while F9 requires Z3-Z1=1. Independently, F6 requires
Z4-Z2=0, while F11 requires Z4-Z2=2. Thus no single common frame fixing point 5
puts these four *original* halves inside one four-point subdisk. Their endpoints
alone do not imply a common supporting disk. This does **not** exclude Hurwitz
moves, substitutions, or a shorter derivation after actual transports.

The complete source product separates into a B4 shadow equal to the fourth
four-point boundary twist, **and** the nonempty kernel loop `(x1 x2 x3 x4)^4`.
The latter cannot be silently erased. This is an independently checked algebraic
diagnostic, not a replacement for the named graphical proof or its sphere caps.

Reproduce with `python examples/analyze_early_point_pushing.py`. Full source
words, retained Schreier edges, kernel braids, per-factor disk reconstruction
checks, and the inconsistent cycles are in
[six-seven-point-pushing.json](six-seven-point-pushing.json).

The next opportunity is to use the kernel to guide a **specific** Hurwitz or
named substitution in the four-strand shadow, then retain its actual lifted
point-pushing correction. A deletion-only argument or another search for a
simultaneous common frame cannot supply that route.
