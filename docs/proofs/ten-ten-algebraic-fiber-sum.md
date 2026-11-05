# An algebraic fiber sum of the imported (10,10)

The imported genus-two \((10,10)\) fibration admits a fiber sum of a \((6,7)\) and a \((4,3)\). An exact positive Hurwitz sequence gives both summands in the original fiber marking, with identity gluing. The diagram route with a support cap of 20 remains open. The recorded diagram preview stops at support 21 before the second crossing.

The [certificate](ten-ten-algebraic-fiber-sum.json) uses the exact twenty factors from [the imported derivation](fibration-derivations/10-10.json). It retains their order and ancestry at every block boundary. The resulting \((6,7)\) is specified by its thirteen factors in the certificate.

## The donor and the seven-factor relation

Write the source order as

\[
U\,a\,P\,b\,e\,Q\,A\,S\,K\,M.
\]

| Block | Actual factors in source order |
| --- | --- |
| \(U\) | C.1, C.2 |
| \(a\) | B.7 |
| \(P\) | B.1, B.2, B.3, B.4 |
| \(b,e\) | B.5, B.6 |
| \(Q\) | A.4 |
| \(A=(x,y)\) | A.6, A.7 |
| \(S\) | A.1, A.2, lantern.1, lantern.2 |
| \(K\) | lantern.3, C.4 |
| \(M\) | C.5, C.6 |

Set \(d=H_{56}=\sigma_5\) and \(c=d^{-1}ad\). The certificate checks \(Pd=dP\) and \(P^{-1}cP=H_\star\) using the full faithful disk action. The [standalone target](ten-ten-short-four-three-target.json) gives

\[
cPM=PH_\star M=D(2..6)^2.
\]

For the actual donor, set \(z={} ^{AKA^{-1}}x\), where \({}^g f=gfg^{-1}\), and set \(d'={} ^{be}z\). Thus the transported factor has A.6 ancestry. Its marked-sphere action agrees with \(d\) on all five chain arcs, and the discrepancy has chosen lift \(+I\). Its disk support word has length 40.

## The algebraic Hurwitz sequence

For ordered blocks \(X,Y\), a forward block interchange sends \(XY\) to \(({}^X Y)X\), where \(X\) in the conjugator denotes the product of that block. The inverse interchange sends \(XY\) to \(Y({}^{Y^{-1}}X)\). Both are products of adjacent Hurwitz moves on positive factors.

| Step | Interchange | Adjacent identities |
| --- | --- | ---: |
| 1 | Carry \(A\) right across \(S\) | 8 |
| 2 | Carry \(A\) right across \(K\) | 4 |
| 3 | Carry the conjugated \(K\) right across \(x\), producing \(z\) | 2 |
| 4 | Carry \(z\) left across \(Q\) and the conjugated \(S\) | 5 |
| 5 | Carry \(e\), then \(b\), right across \(z\), producing \(d'\) | 2 |
| 6 | Carry \(P\) right across \(d'\), producing \(d''={}^P d'\) | 4 |
| 7 | Carry \(d''\) left across \(a\), producing \(c'=(d'')^{-1}ad''\) | 1 |
| 8 | Carry \(M\) left across the ten intervening residual factors | 20 |

The first five rows give \(U\,a\,P\,d'\,W\,M\), with

\[
W=(b,e,{}^{z^{-1}}(Q\,{}^A S),{}^A K,y).
\]

The endpoint is

\[
U\,d''\;[c'PM]\;{}^{M^{-1}}W.
\]

The actual disk factors \(d'\) and \(d''\) stay in the word calculation throughout. The sphere and lift checks identify \(c'\) with \(c\). Each block identity preserves the entire disk product by free reduction.

## Closure and gluing

The contiguous block \(c'PM\) consists of four nonseparating and three separating twists. The remaining ordered tuple \(U\,d''\,{}^{M^{-1}}W\) consists of six nonseparating and seven separating twists. The certificate checks the complete five-arc sphere identity and the chosen \(+I\) lift separately for both tuples.

Enclose the seven contiguous critical values by a separating circle in the base. The bundle over that circle has identity monodromy in the common genus-two marking. Cap the two sides with trivial marked fiber bundles over disks. Removing the caps and identifying the marked fibers by the identity recovers the original fibration. This gives the claimed gluing.

Both disk products fix strand six. The certificate gives each full nonabelian point-pushing loop as an ordered product of signed meridians under explicit shadow actions. It also includes the complete disk braid of the kernel and the smaller shadow. Forty-six faithful Schreier edge equalities and forty signed shadow-generator identities verify reconstruction by free telescoping and collection.

## Reproducing the certificate

Run `python examples/analyze_ten_ten_algebraic_fiber_sum.py` from the repository with the package available on the Python path. The generator checks the pinned source and target bytes and writes the certificate. The test reconstructs all 46 adjacent identities independently from their recorded indices and checks byte-for-byte regeneration.

The raw diagram preview starts by carrying A.7 across A.1 and A.2. The changed A.2 support has length 21 on the second crossing. All diagram previews remain unapplied.
