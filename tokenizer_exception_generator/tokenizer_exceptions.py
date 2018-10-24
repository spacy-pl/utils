# encoding: utf8
from __future__ import unicode_literals

from ...symbols import ORTH, LEMMA, POS, ADV, ADJ, NOUN, ADP

_exc = {}

for exc_data in [
    {ORTH: "m.in.", LEMMA: "między innymi", POS: ADV},
    {ORTH: "inż.", LEMMA: "inżynier", POS: NOUN},
    {ORTH: "mgr.", LEMMA: "magister", POS: NOUN},
    {ORTH: "tzn.", LEMMA: "to znaczy", POS: ADV},
    {ORTH: "tj.", LEMMA: "to jest", POS: ADV},
    {ORTH: "tzw.", LEMMA: "tak zwany", POS: ADJ},
    {ORTH: "adw.", LEMMA: "adwokat", POS: NOUN},
    {ORTH: "afr.", LEMMA: "afrykański", POS: ADJ},
    {ORTH: "c.b.d.o.", LEMMA: "co było do okazania", POS: ADV},
    {ORTH: "cbdu.", LEMMA: "co było do udowodnienia", POS: ADV},
    {ORTH: "mn.w.", LEMMA: "mniej więcej", POS: ADV},
    {ORTH: "nt.", LEMMA: "na temat", POS: ADP},
    {ORTH: "ok.", LEMMA: "około"},
    {ORTH: "n.p.u.", LEMMA: "na psa urok"},
    {ORTH: "ww.", LEMMA: "wyżej wymieniony", POS: ADV}]:
    _exc[exc_data[ORTH]] = [exc_data]

for orth in [
    "w.", "r.", "br.", "bm.", "b.r.", "amer.", "am.", "bdb.", "św.", "p.", "lit.",
    "wym.", "czyt.", "daw.", "d.", "zob.", "gw.", "dn.", "dyr.", "im.", "mł.",
    "min.", "dot.", "muz.", "k.k.", "k.p.a.", "k.p.c.", "n.p.m.", "p.p.m.", "nb.",
    "ob.", "n.e.", "p.n.e.", "zw.", "zool.", "zach.", "żarg.", "żart.", "wzgl.",
    "wyj.", "xx.", "ks.", "x.", "wyd.", "wsch.", "o.o."]:
    _exc[orth] = [{ORTH: orth}]

exceptions = ['Ad.', 'ad.', 'Adw.', 'adw.', 'afr.', 'akad.', 'Al.', 'al.', 'am.', 'amer.', 'arch.', 'Art.', 'art.',
              'artyst.', 'astr.', 'austr.', 'bałt.', 'bdb.', 'bł.', 'bm.', 'bryg.', 'bryt.', 'centr.', 'ces.', 'chem.',
              'chiń.', 'chir.', 'c.k.', 'c.o.', 'cyg.', 'cyw.', 'cyt.', 'czes.', 'cz.', 'czw.', 'Cd.', 'cd.', 'czyt.',
              'ćw.', 'ćwicz.', 'daw.', 'dcn.', 'dekl.', 'demokr.', 'det.', 'diec.', 'dł.', 'dn.', 'dost.', 'dosł.',
              'h.c.', 'ds.', 'dst.', 'duszp.', 'dypl.', 'egz.', 'ekol.', 'ekon.', 'elektr.', 'em.', 'ew.', 'fab.',
              'farm.', 'fot.', 'fr.', 'gat.', 'gastr.', 'geogr.', 'geol.', 'gimn.', 'głęb.', 'gm.', 'godz.', 'górn.',
              'gosp.', 'gr.', 'gram.', 'hist.', 'hiszp.', 'Hr.', 'hr.', 'hot.', 'id.', 'in.', 'im.', 'iron.', 'jn.',
              'kard.', 'kat.', 'katol.', 'k.k.', 'kk.', 'kl.', 'kol.', 'k.p.a.', 'kpc.', 'k.p.c.', 'kpt.', 'kr.',
              'k.r.', 'krak.', 'k.r.o.', 'kryt.', 'kult.', 'laic.', 'łac.', 'niem.', 'woj.', 'Nb.', 'nb.', 'Np.', 'np.',
              'pol.', 'pow.', 'm.in.', 'Pt.', 'pt.', 'Ps.', 'ps.', 'cdn.', 'jw.', 'Ryc.', 'ryc.', 'Rys.', 'rys.', 'tj.',
              'Tzw.', 'tzw.', 'tzn.', 'Zob.', 'zob.', 'słow.', 'pw.', 'pn.', 'pl.', 'ang.', 'ul.', 'ub.', 'ul.', 'ub.',
              'al.', 'k.', 'n.', 'ww.', 'wł.', 'ur.', 'zm.', 'żyd.', 'żarg.', 'żyw.', 'wył.', 'wyd.', 'wym.', 'bp.',
              'up.', 'wyst.', 'Tow.', 'tow.', 'o.', 'sp.', 'Sp.', 'st.', 'Spółdz.', 'spółdz.', 'społ.', 'spółgł.',
              'Stoł.', 'stoł.', 'Stow.', 'stow.', 'zn.', 'zew.', 'zewn.', 'zdr.', 'zazw.', 'zast.', 'zaw.', 'zał.',
              'zal.', 'zam.', 'zak.', 'zakł.', 'zagr.', 'zach.', 'Adw.', 'adw.', 'Lek.', 'lek.', 'med.', 'Mec.', 'mec.',
              'Doc.', 'doc.', 'Dyw.', 'dyw.', 'Dyr.', 'dyr.', 'Inż.', 'inż.', 'mgr.', 'dh.', 'Dh.', 'dr.', 'Dr.',
              'Red.', 'red.', 'Red.)', 'red.)', 'prof.', 'prok.', 'hab.', 'Płk.', 'płk.', 'Nadkom.', 'nadkom.',
              'Podkom.', 'podkom.', 'ks.', 'Ks.', 'gen.', 'por.', 'Reż.', 'reż.', 'Przyp.', 'przyp.', 'p.n.e.',
              'dyr. muz.', 'śp.', 'Śp.', 'św.', 'Św.', 'śW.', 'ŚW.', 'Szer.', 'szer.', 'tel.', 'poz.', 'pok.', 'OO.',
              'oO.', 'Oo.', 'oo.', ', s.', 'u s.', 'o s.', 'i s.', 'Najśw.', 'najśw.', 'Na os.', 'na os.',
              'A. A.', 'Ą. A.', 'B. A.', 'C. A.', 'Ć. A.', 'D. A.',
              'E. A.', 'Ę. A.', 'F. A.', 'G. A.', 'H. A.', 'I. A.', 'J. A.', 'K. A.', 'L. A.', 'Ł. A.', 'M. A.',
              'N. A.', 'Ń. A.', 'O. A.', 'Ó. A.', 'P. A.', 'R. A.', 'S. A.', 'Ś. A.', 'T. A.', 'U. A.', 'W. A.',
              'Y. A.', 'Z. A.', 'Ź. A.', 'Ż. A.', 'A. Ą.', 'Ą. Ą.', 'B. Ą.', 'C. Ą.', 'Ć. Ą.', 'D. Ą.', 'E. Ą.',
              'Ę. Ą.', 'F. Ą.', 'G. Ą.', 'H. Ą.', 'I. Ą.', 'J. Ą.', 'K. Ą.', 'L. Ą.', 'Ł. Ą.', 'M. Ą.', 'N. Ą.',
              'Ń. Ą.', 'O. Ą.', 'Ó. Ą.', 'P. Ą.', 'R. Ą.', 'S. Ą.', 'Ś. Ą.', 'T. Ą.', 'U. Ą.', 'W. Ą.', 'Y. Ą.',
              'Z. Ą.', 'Ź. Ą.', 'Ż. Ą.', 'A. B.', 'Ą. B.', 'B. B.', 'C. B.', 'Ć. B.', 'D. B.', 'E. B.', 'Ę. B.',
              'F. B.', 'G. B.', 'H. B.', 'I. B.', 'J. B.', 'K. B.', 'L. B.', 'Ł. B.', 'M. B.', 'N. B.', 'Ń. B.',
              'O. B.', 'Ó. B.', 'P. B.', 'R. B.', 'S. B.', 'Ś. B.', 'T. B.', 'U. B.', 'W. B.', 'Y. B.', 'Z. B.',
              'Ź. B.', 'Ż. B.', 'A. C.', 'Ą. C.', 'B. C.', 'C. C.', 'Ć. C.', 'D. C.', 'E. C.', 'Ę. C.', 'F. C.',
              'G. C.', 'H. C.', 'I. C.', 'J. C.', 'K. C.', 'L. C.', 'Ł. C.', 'M. C.', 'N. C.', 'Ń. C.', 'O. C.',
              'Ó. C.', 'P. C.', 'R. C.', 'S. C.', 'Ś. C.', 'T. C.', 'U. C.', 'W. C.', 'Y. C.', 'Z. C.', 'Ź. C.',
              'Ż. C.', 'A. Ć.', 'Ą. Ć.', 'B. Ć.', 'C. Ć.', 'Ć. Ć.', 'D. Ć.', 'E. Ć.', 'Ę. Ć.', 'F. Ć.', 'G. Ć.',
              'H. Ć.', 'I. Ć.', 'J. Ć.', 'K. Ć.', 'L. Ć.', 'Ł. Ć.', 'M. Ć.', 'N. Ć.', 'Ń. Ć.', 'O. Ć.', 'Ó. Ć.',
              'P. Ć.', 'R. Ć.', 'S. Ć.', 'Ś. Ć.', 'T. Ć.', 'U. Ć.', 'W. Ć.', 'Y. Ć.', 'Z. Ć.', 'Ź. Ć.', 'Ż. Ć.',
              'A. D.', 'Ą. D.', 'B. D.', 'C. D.', 'Ć. D.', 'D. D.', 'E. D.', 'Ę. D.', 'F. D.', 'G. D.', 'H. D.',
              'I. D.', 'J. D.', 'K. D.', 'L. D.', 'Ł. D.', 'M. D.', 'N. D.', 'Ń. D.', 'O. D.', 'Ó. D.', 'P. D.',
              'R. D.', 'S. D.', 'Ś. D.', 'T. D.', 'U. D.', 'W. D.', 'Y. D.', 'Z. D.', 'Ź. D.', 'Ż. D.', 'A. E.',
              'Ą. E.', 'B. E.', 'C. E.', 'Ć. E.', 'D. E.', 'E. E.', 'Ę. E.', 'F. E.', 'G. E.', 'H. E.', 'I. E.',
              'J. E.', 'K. E.', 'L. E.', 'Ł. E.', 'M. E.', 'N. E.', 'Ń. E.', 'O. E.', 'Ó. E.', 'P. E.', 'R. E.',
              'S. E.', 'Ś. E.', 'T. E.', 'U. E.', 'W. E.', 'Y. E.', 'Z. E.', 'Ź. E.', 'Ż. E.', 'A. Ę.', 'Ą. Ę.',
              'B. Ę.', 'C. Ę.', 'Ć. Ę.', 'D. Ę.', 'E. Ę.', 'Ę. Ę.', 'F. Ę.', 'G. Ę.', 'H. Ę.', 'I. Ę.', 'J. Ę.',
              'K. Ę.', 'L. Ę.', 'Ł. Ę.', 'M. Ę.', 'N. Ę.', 'Ń. Ę.', 'O. Ę.', 'Ó. Ę.', 'P. Ę.', 'R. Ę.', 'S. Ę.',
              'Ś. Ę.', 'T. Ę.', 'U. Ę.', 'W. Ę.', 'Y. Ę.', 'Z. Ę.', 'Ź. Ę.', 'Ż. Ę.', 'A. F.', 'Ą. F.', 'B. F.',
              'C. F.', 'Ć. F.', 'D. F.', 'E. F.', 'Ę. F.', 'F. F.', 'G. F.', 'H. F.', 'I. F.', 'J. F.', 'K. F.',
              'L. F.', 'Ł. F.', 'M. F.', 'N. F.', 'Ń. F.', 'O. F.', 'Ó. F.', 'P. F.', 'R. F.', 'S. F.', 'Ś. F.',
              'T. F.', 'U. F.', 'W. F.', 'Y. F.', 'Z. F.', 'Ź. F.', 'Ż. F.', 'A. G.', 'Ą. G.', 'B. G.', 'C. G.',
              'Ć. G.', 'D. G.', 'E. G.', 'Ę. G.', 'F. G.', 'G. G.', 'H. G.', 'I. G.', 'J. G.', 'K. G.', 'L. G.',
              'Ł. G.', 'M. G.', 'N. G.', 'Ń. G.', 'O. G.', 'Ó. G.', 'P. G.', 'R. G.', 'S. G.', 'Ś. G.', 'T. G.',
              'U. G.', 'W. G.', 'Y. G.', 'Z. G.', 'Ź. G.', 'Ż. G.', 'A. H.', 'Ą. H.', 'B. H.', 'C. H.', 'Ć. H.',
              'D. H.', 'E. H.', 'Ę. H.', 'F. H.', 'G. H.', 'H. H.', 'I. H.', 'J. H.', 'K. H.', 'L. H.', 'Ł. H.',
              'M. H.', 'N. H.', 'Ń. H.', 'O. H.', 'Ó. H.', 'P. H.', 'R. H.', 'S. H.', 'Ś. H.', 'T. H.', 'U. H.',
              'W. H.', 'Y. H.', 'Z. H.', 'Ź. H.', 'Ż. H.', 'A. I.', 'Ą. I.', 'B. I.', 'C. I.', 'Ć. I.', 'D. I.',
              'E. I.', 'Ę. I.', 'F. I.', 'G. I.', 'H. I.', 'I. I.', 'J. I.', 'K. I.', 'L. I.', 'Ł. I.', 'M. I.',
              'N. I.', 'Ń. I.', 'O. I.', 'Ó. I.', 'P. I.', 'R. I.', 'S. I.', 'Ś. I.', 'T. I.', 'U. I.', 'W. I.',
              'Y. I.', 'Z. I.', 'Ź. I.', 'Ż. I.', 'A. J.', 'Ą. J.', 'B. J.', 'C. J.', 'Ć. J.', 'D. J.', 'E. J.',
              'Ę. J.', 'F. J.', 'G. J.', 'H. J.', 'I. J.', 'J. J.', 'K. J.', 'L. J.', 'Ł. J.', 'M. J.', 'N. J.',
              'Ń. J.', 'O. J.', 'Ó. J.', 'P. J.', 'R. J.', 'S. J.', 'Ś. J.', 'T. J.', 'U. J.', 'W. J.', 'Y. J.',
              'Z. J.', 'Ź. J.', 'Ż. J.', 'A. K.', 'Ą. K.', 'B. K.', 'C. K.', 'Ć. K.', 'D. K.', 'E. K.', 'Ę. K.',
              'F. K.', 'G. K.', 'H. K.', 'I. K.', 'J. K.', 'K. K.', 'L. K.', 'Ł. K.', 'M. K.', 'N. K.', 'Ń. K.',
              'O. K.', 'Ó. K.', 'P. K.', 'R. K.', 'S. K.', 'Ś. K.', 'T. K.', 'U. K.', 'W. K.', 'Y. K.', 'Z. K.',
              'Ź. K.', 'Ż. K.', 'A. L.', 'Ą. L.', 'B. L.', 'C. L.', 'Ć. L.', 'D. L.', 'E. L.', 'Ę. L.', 'F. L.',
              'G. L.', 'H. L.', 'I. L.', 'J. L.', 'K. L.', 'L. L.', 'Ł. L.', 'M. L.', 'N. L.', 'Ń. L.', 'O. L.',
              'Ó. L.', 'P. L.', 'R. L.', 'S. L.', 'Ś. L.', 'T. L.', 'U. L.', 'W. L.', 'Y. L.', 'Z. L.', 'Ź. L.',
              'Ż. L.', 'A. Ł.', 'Ą. Ł.', 'B. Ł.', 'C. Ł.', 'Ć. Ł.', 'D. Ł.', 'E. Ł.', 'Ę. Ł.', 'F. Ł.', 'G. Ł.',
              'H. Ł.', 'I. Ł.', 'J. Ł.', 'K. Ł.', 'L. Ł.', 'Ł. Ł.', 'M. Ł.', 'N. Ł.', 'Ń. Ł.', 'O. Ł.', 'Ó. Ł.',
              'P. Ł.', 'R. Ł.', 'S. Ł.', 'Ś. Ł.', 'T. Ł.', 'U. Ł.', 'W. Ł.', 'Y. Ł.', 'Z. Ł.', 'Ź. Ł.', 'Ż. Ł.',
              'A. M.', 'Ą. M.', 'B. M.', 'C. M.', 'Ć. M.', 'D. M.', 'E. M.', 'Ę. M.', 'F. M.', 'G. M.', 'H. M.',
              'I. M.', 'J. M.', 'K. M.', 'L. M.', 'Ł. M.', 'M. M.', 'N. M.', 'Ń. M.', 'O. M.', 'Ó. M.', 'P. M.',
              'R. M.', 'S. M.', 'Ś. M.', 'T. M.', 'U. M.', 'W. M.', 'Y. M.', 'Z. M.', 'Ź. M.', 'Ż. M.', 'A. N.',
              'Ą. N.', 'B. N.', 'C. N.', 'Ć. N.', 'D. N.', 'E. N.', 'Ę. N.', 'F. N.', 'G. N.', 'H. N.', 'I. N.',
              'J. N.', 'K. N.', 'L. N.', 'Ł. N.', 'M. N.', 'N. N.', 'Ń. N.', 'O. N.', 'Ó. N.', 'P. N.', 'R. N.',
              'S. N.', 'Ś. N.', 'T. N.', 'U. N.', 'W. N.', 'Y. N.', 'Z. N.', 'Ź. N.', 'Ż. N.', 'A. Ń.', 'Ą. Ń.',
              'B. Ń.', 'C. Ń.', 'Ć. Ń.', 'D. Ń.', 'E. Ń.', 'Ę. Ń.', 'F. Ń.', 'G. Ń.', 'H. Ń.', 'I. Ń.', 'J. Ń.',
              'K. Ń.', 'L. Ń.', 'Ł. Ń.', 'M. Ń.', 'N. Ń.', 'Ń. Ń.', 'O. Ń.', 'Ó. Ń.', 'P. Ń.', 'R. Ń.', 'S. Ń.',
              'Ś. Ń.', 'T. Ń.', 'U. Ń.', 'W. Ń.', 'Y. Ń.', 'Z. Ń.', 'Ź. Ń.', 'Ż. Ń.', 'A. O.', 'Ą. O.', 'B. O.',
              'C. O.', 'Ć. O.', 'D. O.', 'E. O.', 'Ę. O.', 'F. O.', 'G. O.', 'H. O.', 'I. O.', 'J. O.', 'K. O.',
              'L. O.', 'Ł. O.', 'M. O.', 'N. O.', 'Ń. O.', 'O. O.', 'Ó. O.', 'P. O.', 'R. O.', 'S. O.', 'Ś. O.',
              'T. O.', 'U. O.', 'W. O.', 'Y. O.', 'Z. O.', 'Ź. O.', 'Ż. O.', 'A. Ó.', 'Ą. Ó.', 'B. Ó.', 'C. Ó.',
              'Ć. Ó.', 'D. Ó.', 'E. Ó.', 'Ę. Ó.', 'F. Ó.', 'G. Ó.', 'H. Ó.', 'I. Ó.', 'J. Ó.', 'K. Ó.', 'L. Ó.',
              'Ł. Ó.', 'M. Ó.', 'N. Ó.', 'Ń. Ó.', 'O. Ó.', 'Ó. Ó.', 'P. Ó.', 'R. Ó.', 'S. Ó.', 'Ś. Ó.', 'T. Ó.',
              'U. Ó.', 'W. Ó.', 'Y. Ó.', 'Z. Ó.', 'Ź. Ó.', 'Ż. Ó.', 'A. P.', 'Ą. P.', 'B. P.', 'C. P.', 'Ć. P.',
              'D. P.', 'E. P.', 'Ę. P.', 'F. P.', 'G. P.', 'H. P.', 'I. P.', 'J. P.', 'K. P.', 'L. P.', 'Ł. P.',
              'M. P.', 'N. P.', 'Ń. P.', 'O. P.', 'Ó. P.', 'P. P.', 'R. P.', 'S. P.', 'Ś. P.', 'T. P.', 'U. P.',
              'W. P.', 'Y. P.', 'Z. P.', 'Ź. P.', 'Ż. P.', 'A. R.', 'Ą. R.', 'B. R.', 'C. R.', 'Ć. R.', 'D. R.',
              'E. R.', 'Ę. R.', 'F. R.', 'G. R.', 'H. R.', 'I. R.', 'J. R.', 'K. R.', 'L. R.', 'Ł. R.', 'M. R.',
              'N. R.', 'Ń. R.', 'O. R.', 'Ó. R.', 'P. R.', 'R. R.', 'S. R.', 'Ś. R.', 'T. R.', 'U. R.', 'W. R.',
              'Y. R.', 'Z. R.', 'Ź. R.', 'Ż. R.', 'A. S.', 'Ą. S.', 'B. S.', 'C. S.', 'Ć. S.', 'D. S.', 'E. S.',
              'Ę. S.', 'F. S.', 'G. S.', 'H. S.', 'I. S.', 'J. S.', 'K. S.', 'L. S.', 'Ł. S.', 'M. S.', 'N. S.',
              'Ń. S.', 'O. S.', 'Ó. S.', 'P. S.', 'R. S.', 'S. S.', 'Ś. S.', 'T. S.', 'U. S.', 'W. S.', 'Y. S.',
              'Z. S.', 'Ź. S.', 'Ż. S.', 'A. Ś.', 'Ą. Ś.', 'B. Ś.', 'C. Ś.', 'Ć. Ś.', 'D. Ś.', 'E. Ś.', 'Ę. Ś.',
              'F. Ś.', 'G. Ś.', 'H. Ś.', 'I. Ś.', 'J. Ś.', 'K. Ś.', 'L. Ś.', 'Ł. Ś.', 'M. Ś.', 'N. Ś.', 'Ń. Ś.',
              'O. Ś.', 'Ó. Ś.', 'P. Ś.', 'R. Ś.', 'S. Ś.', 'Ś. Ś.', 'T. Ś.', 'U. Ś.', 'W. Ś.', 'Y. Ś.', 'Z. Ś.',
              'Ź. Ś.', 'Ż. Ś.', 'A. T.', 'Ą. T.', 'B. T.', 'C. T.', 'Ć. T.', 'D. T.', 'E. T.', 'Ę. T.', 'F. T.',
              'G. T.', 'H. T.', 'I. T.', 'J. T.', 'K. T.', 'L. T.', 'Ł. T.', 'M. T.', 'N. T.', 'Ń. T.', 'O. T.',
              'Ó. T.', 'P. T.', 'R. T.', 'S. T.', 'Ś. T.', 'T. T.', 'U. T.', 'W. T.', 'Y. T.', 'Z. T.', 'Ź. T.',
              'Ż. T.', 'A. U.', 'Ą. U.', 'B. U.', 'C. U.', 'Ć. U.', 'D. U.', 'E. U.', 'Ę. U.', 'F. U.', 'G. U.',
              'H. U.', 'I. U.', 'J. U.', 'K. U.', 'L. U.', 'Ł. U.', 'M. U.', 'N. U.', 'Ń. U.', 'O. U.', 'Ó. U.',
              'P. U.', 'R. U.', 'S. U.', 'Ś. U.', 'T. U.', 'U. U.', 'W. U.', 'Y. U.', 'Z. U.', 'Ź. U.', 'Ż. U.',
              'A. W.', 'Ą. W.', 'B. W.', 'C. W.', 'Ć. W.', 'D. W.', 'E. W.', 'Ę. W.', 'F. W.', 'G. W.', 'H. W.',
              'I. W.', 'J. W.', 'K. W.', 'L. W.', 'Ł. W.', 'M. W.', 'N. W.', 'Ń. W.', 'O. W.', 'Ó. W.', 'P. W.',
              'R. W.', 'S. W.', 'Ś. W.', 'T. W.', 'U. W.', 'W. W.', 'Y. W.', 'Z. W.', 'Ź. W.', 'Ż. W.', 'A. Y.',
              'Ą. Y.', 'B. Y.', 'C. Y.', 'Ć. Y.', 'D. Y.', 'E. Y.', 'Ę. Y.', 'F. Y.', 'G. Y.', 'H. Y.', 'I. Y.',
              'J. Y.', 'K. Y.', 'L. Y.', 'Ł. Y.', 'M. Y.', 'N. Y.', 'Ń. Y.', 'O. Y.', 'Ó. Y.', 'P. Y.', 'R. Y.',
              'S. Y.', 'Ś. Y.', 'T. Y.', 'U. Y.', 'W. Y.', 'Y. Y.', 'Z. Y.', 'Ź. Y.', 'Ż. Y.', 'A. Z.', 'Ą. Z.',
              'B. Z.', 'C. Z.', 'Ć. Z.', 'D. Z.', 'E. Z.', 'Ę. Z.', 'F. Z.', 'G. Z.', 'H. Z.', 'I. Z.', 'J. Z.',
              'K. Z.', 'L. Z.', 'Ł. Z.', 'M. Z.', 'N. Z.', 'Ń. Z.', 'O. Z.', 'Ó. Z.', 'P. Z.', 'R. Z.', 'S. Z.',
              'Ś. Z.', 'T. Z.', 'U. Z.', 'W. Z.', 'Y. Z.', 'Z. Z.', 'Ź. Z.', 'Ż. Z.', 'A. Ź.', 'Ą. Ź.', 'B. Ź.',
              'C. Ź.', 'Ć. Ź.', 'D. Ź.', 'E. Ź.', 'Ę. Ź.', 'F. Ź.', 'G. Ź.', 'H. Ź.', 'I. Ź.', 'J. Ź.', 'K. Ź.',
              'L. Ź.', 'Ł. Ź.', 'M. Ź.', 'N. Ź.', 'Ń. Ź.', 'O. Ź.', 'Ó. Ź.', 'P. Ź.', 'R. Ź.', 'S. Ź.', 'Ś. Ź.',
              'T. Ź.', 'U. Ź.', 'W. Ź.', 'Y. Ź.', 'Z. Ź.', 'Ź. Ź.', 'Ż. Ź.', 'A. Ż.', 'Ą. Ż.', 'B. Ż.', 'C. Ż.',
              'Ć. Ż.', 'D. Ż.', 'E. Ż.', 'Ę. Ż.', 'F. Ż.', 'G. Ż.', 'H. Ż.', 'I. Ż.', 'J. Ż.', 'K. Ż.', 'L. Ż.',
              'Ł. Ż.', 'M. Ż.', 'N. Ż.', 'Ń. Ż.', 'O. Ż.', 'Ó. Ż.', 'P. Ż.', 'R. Ż.', 'S. Ż.', 'Ś. Ż.', 'T. Ż.',
              'U. Ż.', 'W. Ż.', 'Y. Ż.', 'Z. Ż.', 'Ź. Ż.', 'Ż. Ż.', 'A.A.', 'Ą.A.', 'B.A.', 'C.A.', 'Ć.A.', 'D.A.',
              'E.A.', 'Ę.A.', 'F.A.', 'G.A.', 'H.A.', 'I.A.', 'J.A.', 'K.A.', 'L.A.', 'Ł.A.', 'M.A.', 'N.A.', 'Ń.A.',
              'O.A.', 'Ó.A.', 'P.A.', 'R.A.', 'S.A.', 'Ś.A.', 'T.A.', 'U.A.', 'W.A.', 'Y.A.', 'Z.A.', 'Ź.A.', 'Ż.A.',
              'A.Ą.', 'Ą.Ą.', 'B.Ą.', 'C.Ą.', 'Ć.Ą.', 'D.Ą.', 'E.Ą.', 'Ę.Ą.', 'F.Ą.', 'G.Ą.', 'H.Ą.', 'I.Ą.', 'J.Ą.',
              'K.Ą.', 'L.Ą.', 'Ł.Ą.', 'M.Ą.', 'N.Ą.', 'Ń.Ą.', 'O.Ą.', 'Ó.Ą.', 'P.Ą.', 'R.Ą.', 'S.Ą.', 'Ś.Ą.', 'T.Ą.',
              'U.Ą.', 'W.Ą.', 'Y.Ą.', 'Z.Ą.', 'Ź.Ą.', 'Ż.Ą.', 'A.B.', 'Ą.B.', 'B.B.', 'C.B.', 'Ć.B.', 'D.B.', 'E.B.',
              'Ę.B.', 'F.B.', 'G.B.', 'H.B.', 'I.B.', 'J.B.', 'K.B.', 'L.B.', 'Ł.B.', 'M.B.', 'N.B.', 'Ń.B.', 'O.B.',
              'Ó.B.', 'P.B.', 'R.B.', 'S.B.', 'Ś.B.', 'T.B.', 'U.B.', 'W.B.', 'Y.B.', 'Z.B.', 'Ź.B.', 'Ż.B.', 'A.C.',
              'Ą.C.', 'B.C.', 'C.C.', 'Ć.C.', 'D.C.', 'E.C.', 'Ę.C.', 'F.C.', 'G.C.', 'H.C.', 'I.C.', 'J.C.', 'K.C.',
              'L.C.', 'Ł.C.', 'M.C.', 'N.C.', 'Ń.C.', 'O.C.', 'Ó.C.', 'P.C.', 'R.C.', 'S.C.', 'Ś.C.', 'T.C.', 'U.C.',
              'W.C.', 'Y.C.', 'Z.C.', 'Ź.C.', 'Ż.C.', 'A.Ć.', 'Ą.Ć.', 'B.Ć.', 'C.Ć.', 'Ć.Ć.', 'D.Ć.', 'E.Ć.', 'Ę.Ć.',
              'F.Ć.', 'G.Ć.', 'H.Ć.', 'I.Ć.', 'J.Ć.', 'K.Ć.', 'L.Ć.', 'Ł.Ć.', 'M.Ć.', 'N.Ć.', 'Ń.Ć.', 'O.Ć.', 'Ó.Ć.',
              'P.Ć.', 'R.Ć.', 'S.Ć.', 'Ś.Ć.', 'T.Ć.', 'U.Ć.', 'W.Ć.', 'Y.Ć.', 'Z.Ć.', 'Ź.Ć.', 'Ż.Ć.', 'A.D.', 'Ą.D.',
              'B.D.', 'C.D.', 'Ć.D.', 'D.D.', 'E.D.', 'Ę.D.', 'F.D.', 'G.D.', 'H.D.', 'I.D.', 'J.D.', 'K.D.', 'L.D.',
              'Ł.D.', 'M.D.', 'N.D.', 'Ń.D.', 'O.D.', 'Ó.D.', 'P.D.', 'R.D.', 'S.D.', 'Ś.D.', 'T.D.', 'U.D.', 'W.D.',
              'Y.D.', 'Z.D.', 'Ź.D.', 'Ż.D.', 'A.E.', 'Ą.E.', 'B.E.', 'C.E.', 'Ć.E.', 'D.E.', 'E.E.', 'Ę.E.', 'F.E.',
              'G.E.', 'H.E.', 'I.E.', 'J.E.', 'K.E.', 'L.E.', 'Ł.E.', 'M.E.', 'N.E.', 'Ń.E.', 'O.E.', 'Ó.E.', 'P.E.',
              'R.E.', 'S.E.', 'Ś.E.', 'T.E.', 'U.E.', 'W.E.', 'Y.E.', 'Z.E.', 'Ź.E.', 'Ż.E.', 'A.Ę.', 'Ą.Ę.', 'B.Ę.',
              'C.Ę.', 'Ć.Ę.', 'D.Ę.', 'E.Ę.', 'Ę.Ę.', 'F.Ę.', 'G.Ę.', 'H.Ę.', 'I.Ę.', 'J.Ę.', 'K.Ę.', 'L.Ę.', 'Ł.Ę.',
              'M.Ę.', 'N.Ę.', 'Ń.Ę.', 'O.Ę.', 'Ó.Ę.', 'P.Ę.', 'R.Ę.', 'S.Ę.', 'Ś.Ę.', 'T.Ę.', 'U.Ę.', 'W.Ę.', 'Y.Ę.',
              'Z.Ę.', 'Ź.Ę.', 'Ż.Ę.', 'A.F.', 'Ą.F.', 'B.F.', 'C.F.', 'Ć.F.', 'D.F.', 'E.F.', 'Ę.F.', 'F.F.', 'G.F.',
              'H.F.', 'I.F.', 'J.F.', 'K.F.', 'L.F.', 'Ł.F.', 'M.F.', 'N.F.', 'Ń.F.', 'O.F.', 'Ó.F.', 'P.F.', 'R.F.',
              'S.F.', 'Ś.F.', 'T.F.', 'U.F.', 'W.F.', 'Y.F.', 'Z.F.', 'Ź.F.', 'Ż.F.', 'A.G.', 'Ą.G.', 'B.G.', 'C.G.',
              'Ć.G.', 'D.G.', 'E.G.', 'Ę.G.', 'F.G.', 'G.G.', 'H.G.', 'I.G.', 'J.G.', 'K.G.', 'L.G.', 'Ł.G.', 'M.G.',
              'N.G.', 'Ń.G.', 'O.G.', 'Ó.G.', 'P.G.', 'R.G.', 'S.G.', 'Ś.G.', 'T.G.', 'U.G.', 'W.G.', 'Y.G.', 'Z.G.',
              'Ź.G.', 'Ż.G.', 'A.H.', 'Ą.H.', 'B.H.', 'C.H.', 'Ć.H.', 'D.H.', 'E.H.', 'Ę.H.', 'F.H.', 'G.H.', 'H.H.',
              'I.H.', 'J.H.', 'K.H.', 'L.H.', 'Ł.H.', 'M.H.', 'N.H.', 'Ń.H.', 'O.H.', 'Ó.H.', 'P.H.', 'R.H.', 'S.H.',
              'Ś.H.', 'T.H.', 'U.H.', 'W.H.', 'Y.H.', 'Z.H.', 'Ź.H.', 'Ż.H.', 'A.I.', 'Ą.I.', 'B.I.', 'C.I.', 'Ć.I.',
              'D.I.', 'E.I.', 'Ę.I.', 'F.I.', 'G.I.', 'H.I.', 'I.I.', 'J.I.', 'K.I.', 'L.I.', 'Ł.I.', 'M.I.', 'N.I.',
              'Ń.I.', 'O.I.', 'Ó.I.', 'P.I.', 'R.I.', 'S.I.', 'Ś.I.', 'T.I.', 'U.I.', 'W.I.', 'Y.I.', 'Z.I.', 'Ź.I.',
              'Ż.I.', 'A.J.', 'Ą.J.', 'B.J.', 'C.J.', 'Ć.J.', 'D.J.', 'E.J.', 'Ę.J.', 'F.J.', 'G.J.', 'H.J.', 'I.J.',
              'J.J.', 'K.J.', 'L.J.', 'Ł.J.', 'M.J.', 'N.J.', 'Ń.J.', 'O.J.', 'Ó.J.', 'P.J.', 'R.J.', 'S.J.', 'Ś.J.',
              'T.J.', 'U.J.', 'W.J.', 'Y.J.', 'Z.J.', 'Ź.J.', 'Ż.J.', 'A.K.', 'Ą.K.', 'B.K.', 'C.K.', 'Ć.K.', 'D.K.',
              'E.K.', 'Ę.K.', 'F.K.', 'G.K.', 'H.K.', 'I.K.', 'J.K.', 'K.K.', 'L.K.', 'Ł.K.', 'M.K.', 'N.K.', 'Ń.K.',
              'O.K.', 'Ó.K.', 'P.K.', 'R.K.', 'S.K.', 'Ś.K.', 'T.K.', 'U.K.', 'W.K.', 'Y.K.', 'Z.K.', 'Ź.K.', 'Ż.K.',
              'A.L.', 'Ą.L.', 'B.L.', 'C.L.', 'Ć.L.', 'D.L.', 'E.L.', 'Ę.L.', 'F.L.', 'G.L.', 'H.L.', 'I.L.', 'J.L.',
              'K.L.', 'L.L.', 'Ł.L.', 'M.L.', 'N.L.', 'Ń.L.', 'O.L.', 'Ó.L.', 'P.L.', 'R.L.', 'S.L.', 'Ś.L.', 'T.L.',
              'U.L.', 'W.L.', 'Y.L.', 'Z.L.', 'Ź.L.', 'Ż.L.', 'A.Ł.', 'Ą.Ł.', 'B.Ł.', 'C.Ł.', 'Ć.Ł.', 'D.Ł.', 'E.Ł.',
              'Ę.Ł.', 'F.Ł.', 'G.Ł.', 'H.Ł.', 'I.Ł.', 'J.Ł.', 'K.Ł.', 'L.Ł.', 'Ł.Ł.', 'M.Ł.', 'N.Ł.', 'Ń.Ł.', 'O.Ł.',
              'Ó.Ł.', 'P.Ł.', 'R.Ł.', 'S.Ł.', 'Ś.Ł.', 'T.Ł.', 'U.Ł.', 'W.Ł.', 'Y.Ł.', 'Z.Ł.', 'Ź.Ł.', 'Ż.Ł.', 'A.M.',
              'Ą.M.', 'B.M.', 'C.M.', 'Ć.M.', 'D.M.', 'E.M.', 'Ę.M.', 'F.M.', 'G.M.', 'H.M.', 'I.M.', 'J.M.', 'K.M.',
              'L.M.', 'Ł.M.', 'M.M.', 'N.M.', 'Ń.M.', 'O.M.', 'Ó.M.', 'P.M.', 'R.M.', 'S.M.', 'Ś.M.', 'T.M.', 'U.M.',
              'W.M.', 'Y.M.', 'Z.M.', 'Ź.M.', 'Ż.M.', 'A.N.', 'Ą.N.', 'B.N.', 'C.N.', 'Ć.N.', 'D.N.', 'E.N.', 'Ę.N.',
              'F.N.', 'G.N.', 'H.N.', 'I.N.', 'J.N.', 'K.N.', 'L.N.', 'Ł.N.', 'M.N.', 'N.N.', 'Ń.N.', 'O.N.', 'Ó.N.',
              'P.N.', 'R.N.', 'S.N.', 'Ś.N.', 'T.N.', 'U.N.', 'W.N.', 'Y.N.', 'Z.N.', 'Ź.N.', 'Ż.N.', 'A.Ń.', 'Ą.Ń.',
              'B.Ń.', 'C.Ń.', 'Ć.Ń.', 'D.Ń.', 'E.Ń.', 'Ę.Ń.', 'F.Ń.', 'G.Ń.', 'H.Ń.', 'I.Ń.', 'J.Ń.', 'K.Ń.', 'L.Ń.',
              'Ł.Ń.', 'M.Ń.', 'N.Ń.', 'Ń.Ń.', 'O.Ń.', 'Ó.Ń.', 'P.Ń.', 'R.Ń.', 'S.Ń.', 'Ś.Ń.', 'T.Ń.', 'U.Ń.', 'W.Ń.',
              'Y.Ń.', 'Z.Ń.', 'Ź.Ń.', 'Ż.Ń.', 'A.O.', 'Ą.O.', 'B.O.', 'C.O.', 'Ć.O.', 'D.O.', 'E.O.', 'Ę.O.', 'F.O.',
              'G.O.', 'H.O.', 'I.O.', 'J.O.', 'K.O.', 'L.O.', 'Ł.O.', 'M.O.', 'N.O.', 'Ń.O.', 'O.O.', 'Ó.O.', 'P.O.',
              'R.O.', 'S.O.', 'Ś.O.', 'T.O.', 'U.O.', 'W.O.', 'Y.O.', 'Z.O.', 'Ź.O.', 'Ż.O.', 'A.Ó.', 'Ą.Ó.', 'B.Ó.',
              'C.Ó.', 'Ć.Ó.', 'D.Ó.', 'E.Ó.', 'Ę.Ó.', 'F.Ó.', 'G.Ó.', 'H.Ó.', 'I.Ó.', 'J.Ó.', 'K.Ó.', 'L.Ó.', 'Ł.Ó.',
              'M.Ó.', 'N.Ó.', 'Ń.Ó.', 'O.Ó.', 'Ó.Ó.', 'P.Ó.', 'R.Ó.', 'S.Ó.', 'Ś.Ó.', 'T.Ó.', 'U.Ó.', 'W.Ó.', 'Y.Ó.',
              'Z.Ó.', 'Ź.Ó.', 'Ż.Ó.', 'A.P.', 'Ą.P.', 'B.P.', 'C.P.', 'Ć.P.', 'D.P.', 'E.P.', 'Ę.P.', 'F.P.', 'G.P.',
              'H.P.', 'I.P.', 'J.P.', 'K.P.', 'L.P.', 'Ł.P.', 'M.P.', 'N.P.', 'Ń.P.', 'O.P.', 'Ó.P.', 'P.P.', 'R.P.',
              'S.P.', 'Ś.P.', 'T.P.', 'U.P.', 'W.P.', 'Y.P.', 'Z.P.', 'Ź.P.', 'Ż.P.', 'A.R.', 'Ą.R.', 'B.R.', 'C.R.',
              'Ć.R.', 'D.R.', 'E.R.', 'Ę.R.', 'F.R.', 'G.R.', 'H.R.', 'I.R.', 'J.R.', 'K.R.', 'L.R.', 'Ł.R.', 'M.R.',
              'N.R.', 'Ń.R.', 'O.R.', 'Ó.R.', 'P.R.', 'R.R.', 'S.R.', 'Ś.R.', 'T.R.', 'U.R.', 'W.R.', 'Y.R.', 'Z.R.',
              'Ź.R.', 'Ż.R.', 'A.S.', 'Ą.S.', 'B.S.', 'C.S.', 'Ć.S.', 'D.S.', 'E.S.', 'Ę.S.', 'F.S.', 'G.S.', 'H.S.',
              'I.S.', 'J.S.', 'K.S.', 'L.S.', 'Ł.S.', 'M.S.', 'N.S.', 'Ń.S.', 'O.S.', 'Ó.S.', 'P.S.', 'R.S.', 'S.S.',
              'Ś.S.', 'T.S.', 'U.S.', 'W.S.', 'Y.S.', 'Z.S.', 'Ź.S.', 'Ż.S.', 'A.Ś.', 'Ą.Ś.', 'B.Ś.', 'C.Ś.', 'Ć.Ś.',
              'D.Ś.', 'E.Ś.', 'Ę.Ś.', 'F.Ś.', 'G.Ś.', 'H.Ś.', 'I.Ś.', 'J.Ś.', 'K.Ś.', 'L.Ś.', 'Ł.Ś.', 'M.Ś.', 'N.Ś.',
              'Ń.Ś.', 'O.Ś.', 'Ó.Ś.', 'P.Ś.', 'R.Ś.', 'S.Ś.', 'Ś.Ś.', 'T.Ś.', 'U.Ś.', 'W.Ś.', 'Y.Ś.', 'Z.Ś.', 'Ź.Ś.',
              'Ż.Ś.', 'A.T.', 'Ą.T.', 'B.T.', 'C.T.', 'Ć.T.', 'D.T.', 'E.T.', 'Ę.T.', 'F.T.', 'G.T.', 'H.T.', 'I.T.',
              'J.T.', 'K.T.', 'L.T.', 'Ł.T.', 'M.T.', 'N.T.', 'Ń.T.', 'O.T.', 'Ó.T.', 'P.T.', 'R.T.', 'S.T.', 'Ś.T.',
              'T.T.', 'U.T.', 'W.T.', 'Y.T.', 'Z.T.', 'Ź.T.', 'Ż.T.', 'A.U.', 'Ą.U.', 'B.U.', 'C.U.', 'Ć.U.', 'D.U.',
              'E.U.', 'Ę.U.', 'F.U.', 'G.U.', 'H.U.', 'I.U.', 'J.U.', 'K.U.', 'L.U.', 'Ł.U.', 'M.U.', 'N.U.', 'Ń.U.',
              'O.U.', 'Ó.U.', 'P.U.', 'R.U.', 'S.U.', 'Ś.U.', 'T.U.', 'U.U.', 'W.U.', 'Y.U.', 'Z.U.', 'Ź.U.', 'Ż.U.',
              'A.W.', 'Ą.W.', 'B.W.', 'C.W.', 'Ć.W.', 'D.W.', 'E.W.', 'Ę.W.', 'F.W.', 'G.W.', 'H.W.', 'I.W.', 'J.W.',
              'K.W.', 'L.W.', 'Ł.W.', 'M.W.', 'N.W.', 'Ń.W.', 'O.W.', 'Ó.W.', 'P.W.', 'R.W.', 'S.W.', 'Ś.W.', 'T.W.',
              'U.W.', 'W.W.', 'Y.W.', 'Z.W.', 'Ź.W.', 'Ż.W.', 'A.Y.', 'Ą.Y.', 'B.Y.', 'C.Y.', 'Ć.Y.', 'D.Y.', 'E.Y.',
              'Ę.Y.', 'F.Y.', 'G.Y.', 'H.Y.', 'I.Y.', 'J.Y.', 'K.Y.', 'L.Y.', 'Ł.Y.', 'M.Y.', 'N.Y.', 'Ń.Y.', 'O.Y.',
              'Ó.Y.', 'P.Y.', 'R.Y.', 'S.Y.', 'Ś.Y.', 'T.Y.', 'U.Y.', 'W.Y.', 'Y.Y.', 'Z.Y.', 'Ź.Y.', 'Ż.Y.', 'A.Z.',
              'Ą.Z.', 'B.Z.', 'C.Z.', 'Ć.Z.', 'D.Z.', 'E.Z.', 'Ę.Z.', 'F.Z.', 'G.Z.', 'H.Z.', 'I.Z.', 'J.Z.', 'K.Z.',
              'L.Z.', 'Ł.Z.', 'M.Z.', 'N.Z.', 'Ń.Z.', 'O.Z.', 'Ó.Z.', 'P.Z.', 'R.Z.', 'S.Z.', 'Ś.Z.', 'T.Z.', 'U.Z.',
              'W.Z.', 'Y.Z.', 'Z.Z.', 'Ź.Z.', 'Ż.Z.', 'A.Ź.', 'Ą.Ź.', 'B.Ź.', 'C.Ź.', 'Ć.Ź.', 'D.Ź.', 'E.Ź.', 'Ę.Ź.',
              'F.Ź.', 'G.Ź.', 'H.Ź.', 'I.Ź.', 'J.Ź.', 'K.Ź.', 'L.Ź.', 'Ł.Ź.', 'M.Ź.', 'N.Ź.', 'Ń.Ź.', 'O.Ź.', 'Ó.Ź.',
              'P.Ź.', 'R.Ź.', 'S.Ź.', 'Ś.Ź.', 'T.Ź.', 'U.Ź.', 'W.Ź.', 'Y.Ź.', 'Z.Ź.', 'Ź.Ź.', 'Ż.Ź.', 'A.Ż.', 'Ą.Ż.',
              'B.Ż.', 'C.Ż.', 'Ć.Ż.', 'D.Ż.', 'E.Ż.', 'Ę.Ż.', 'F.Ż.', 'G.Ż.', 'H.Ż.', 'I.Ż.', 'J.Ż.', 'K.Ż.', 'L.Ż.',
              'Ł.Ż.', 'M.Ż.', 'N.Ż.', 'Ń.Ż.', 'O.Ż.', 'Ó.Ż.', 'P.Ż.', 'R.Ż.', 'S.Ż.', 'Ś.Ż.', 'T.Ż.', 'U.Ż.', 'W.Ż.',
              'Y.Ż.', 'Z.Ż.', 'Ź.Ż.', 'Ż.Ż.', 'Dz.U.', 'Dz. U.']

for orth in exceptions:
    _exc[orth] = [{ORTH: orth}]

TOKENIZER_EXCEPTIONS = _exc
