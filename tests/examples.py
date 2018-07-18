# -*- coding: utf-8 -*-

"""Example BEL graphs for testing PyBEL-CX."""

from pybel import BELGraph
from pybel.constants import (
    CITATION_REFERENCE, CITATION_TYPE, CITATION_TYPE_OTHER, DECREASES, DIRECTLY_INCREASES, HAS_VARIANT, INCREASES,
    NEGATIVE_CORRELATION, POSITIVE_CORRELATION,
)
from pybel.dsl import (
    abundance, activity, bioprocess, complex_abundance, gene, gmod, named_complex_abundance, pathology, pmod, protein,
    protein_fusion, protein_substitution, reaction, rna,
)


class _BELGraph(BELGraph):
    def add_increases(self, u, v, citation, evidence, annotations=None, subject_modifier=None, object_modifier=None):
        if not isinstance(evidence, str):
            raise TypeError
        return self.add_qualified_edge(u, v, INCREASES, evidence, citation, annotations=annotations,
                                       subject_modifier=subject_modifier, object_modifier=object_modifier)

    def add_directly_increases(self, u, v, citation, evidence, *, annotations=None, subject_modifier=None,
                               object_modifier=None):
        if not isinstance(evidence, str):
            raise TypeError
        return self.add_qualified_edge(u, v, DIRECTLY_INCREASES, evidence, citation, annotations=annotations,
                                       subject_modifier=subject_modifier, object_modifier=object_modifier)

    def add_decreases(self, u, v, citation, evidence, annotations=None, subject_modifier=None, object_modifier=None):
        if not isinstance(evidence, str):
            raise TypeError
        return self.add_qualified_edge(u, v, DECREASES, evidence, citation, annotations=annotations,
                                       subject_modifier=subject_modifier, object_modifier=object_modifier)

    def add_positive_correlation(self, u, v, evidence, citation, *, annotations=None, subject_modifier=None,
                                 object_modifier=None):
        if not isinstance(evidence, str):
            raise TypeError
        return self.add_qualified_edge(u, v, POSITIVE_CORRELATION, evidence, citation, annotations=annotations,
                                       subject_modifier=subject_modifier, object_modifier=object_modifier)

    def add_negative_correlation(self, u, v, evidence, citation, *, annotations=None, subject_modifier=None,
                                 object_modifier=None):
        if not isinstance(evidence, str):
            raise TypeError
        return self.add_qualified_edge(u, v, NEGATIVE_CORRELATION, evidence, citation, annotations=annotations,
                                       subject_modifier=subject_modifier, object_modifier=object_modifier)


example_graph = _BELGraph()

example_graph.namespace_url['HGNC'] = ''
example_graph.namespace_pattern['DBSNP'] = '^rs\d+$'
example_graph.annotation_url['Species'] = ''
example_graph.annotation_pattern['Number'] = '^\d+$'
example_graph.annotation_list['Confidence'] = {'High', 'Low'}

ptk2 = protein(namespace='HGNC', name='PTK2', variants=[pmod('Ph', 'Tyr', 925)])
mapk1 = protein(namespace='HGNC', name='MAPK1')
mapk3 = protein(namespace='HGNC', name='MAPK3')
grb2 = protein(namespace='HGNC', name='GRB2')
sos1 = protein(namespace='HGNC', name='SOS1')
ptk2_rgb2_sos1 = complex_abundance([mapk1, grb2, sos1])

ras_family = protein(namespace='SFAM', name='RAS Family')
pi3k_complex = named_complex_abundance(namespace='SFAM', name='p85/p110 PI3Kinase Complex')

kinase_activity = activity('kin')
catalytic_activity = activity('cat')
gtp_activity = activity('gtp')

c1 = '10446041'
e1 = "FAK also combines with, and may activate, phosphoinositide 3-OH kinase (PI 3-kinase), either directly or " \
     "through the Src kinase (13). Finally, there is evidence that Src phosphorylates FAK at Tyr925, creating a" \
     " binding site for the complex of the adapter Grb2 and Ras guanosine 5'-triphosphate exchange factor mSOS (10)." \
     " These interactions link FAK to signaling pathways that modify the cytoskeleton and activate mitogen-activated" \
     " protein kinase (MAPK) cascades (Fig. 3A)."

e1 = str(hash(e1))

"""
p(HGNC:PTK2,pmod(P,Y,925)) increases kin(p(HGNC:MAPK1))
complex(p(HGNC:PTK2),p(HGNC:GRB2),p(HGNC:SOS1)) increases gtp(p(SFAM:"RAS Family"))
gtp(p(SFAM:"RAS Family")) increases kin(p(HGNC:MAPK1))
kin(p(HGNC:PTK2)) increases complex(p(HGNC:PTK2),p(HGNC:GRB2),p(HGNC:SOS1))
kin(p(HGNC:PTK2)) increases kin(p(HGNC:MAPK1))
kin(p(HGNC:PTK2)) increases kin(p(HGNC:MAPK3))
kin(p(HGNC:PTK2)) increases kin(complex(SCOMP:"p85/p110 PI3Kinase Complex"))
"""

example_graph.add_increases(ptk2, mapk1, e1, c1, object_modifier=kinase_activity)
example_graph.add_increases(ptk2_rgb2_sos1, ras_family, e1, c1, object_modifier=gtp_activity)
example_graph.add_increases(ras_family, mapk1, e1, c1, subject_modifier=gtp_activity, object_modifier=kinase_activity)
example_graph.add_increases(ptk2, ptk2_rgb2_sos1, e1, c1, subject_modifier=kinase_activity)
example_graph.add_increases(ptk2, mapk1, e1, c1, subject_modifier=kinase_activity, object_modifier=kinase_activity)
example_graph.add_increases(ptk2, mapk3, e1, c1, subject_modifier=kinase_activity, object_modifier=kinase_activity)
example_graph.add_increases(ptk2, pi3k_complex, e1, c1, subject_modifier=kinase_activity,
                            object_modifier=kinase_activity)

"""
SET Evidence=" two common MTHFR polymorphisms, namely 677C>T (Ala222Val) and 1298A>C (Glu429Ala), are known to reduce MTHFR activity. \
It has been shown that the MTHFR 677T allele is associated with increased total plasma Hcy levels (tHcy) and decreased serum folate levels, mainly in 677TT homozygous subjects.\
the MTHFR 677C>T polymorphism as a candidate AD risk factor"

SET Subgraph = "Epigenetic modification subgraph"
g(HGNC:MTHFR,sub(C,677,T)) =| p(HGNC:MTHFR)
g(HGNC:MTHFR,sub(A,1298,C)) =| p(HGNC:MTHFR)
g(HGNC:MTHFR,sub(C,677,T)) neg a(CHEBI:"folic acid")
g(HGNC:MTHFR,sub(C,677,T)) pos path(MESH:"Alzheimer Disease")
"""

c2 = '21119889'
e2 = "Two common MTHFR polymorphisms, namely 677C>T (Ala222Val) and 1298A>C (Glu429Ala), are known to reduce MTHFR activity. \
It has been shown that the MTHFR 677T allele is associated with increased total plasma Hcy levels (tHcy) and decreased serum folate levels, mainly in 677TT homozygous subjects.\
the MTHFR 677C>T polymorphism as a candidate AD risk factor"
e2 = str(hash(e2))

mthfr = protein('HGNC', 'MTHFR')
mthfr_c677t = protein('HGNC', 'MTHFR', variants=[protein_substitution('Ala', 222, 'Val')])
mthfr_a1298c = protein('HGNC', 'MTHFR', variants=[protein_substitution('Glu', 429, 'Ala')])
folic_acid = abundance('CHEBI', 'folic acid')
alzheimer_disease = pathology('MESH', 'Alzheimer Disease')

example_graph.add_decreases(mthfr_c677t, mthfr, c2, e2, object_modifier=activity())
example_graph.add_decreases(mthfr_a1298c, mthfr, c2, e2, object_modifier=activity())
example_graph.add_negative_correlation(mthfr_c677t, folic_acid, c2, e2)
example_graph.add_positive_correlation(mthfr_c677t, alzheimer_disease, c2, e2)

c3 = '17948130'
e3 = 'A polymorphism in the NDUFB6 promoter region that creates a possible DNA methylation site (rs629566, A/G) was ' \
     'associated with a decline in muscle NDUFB6 expression with age. Although young subjects with the rs629566 G/G ' \
     'genotype exhibited higher muscle NDUFB6 expression, this genotype was associated with reduced expression in' \
     ' elderly subjects. This was subsequently explained by the finding of increased DNA methylation in the promoter ' \
     'of elderly, but not young, subjects carrying the rs629566 G/G genotype. Furthermore, the degree of DNA' \
     ' methylation correlated negatively with muscle NDUFB6 expression, which in turn was associated with insulin ' \
     'sensitivity.'
e3 = str(hash(e3))

rs629566 = gene('DBSNP', 'rs629566', variants=[gmod('Me')])
ndufb6_gene = gene('HGNC', 'NDUFB6')
ndufb6_rna = rna('HGNC', 'NDUFB6')

example_graph.add_unqualified_edge(ndufb6_gene, rs629566, HAS_VARIANT)
example_graph.add_negative_correlation(rs629566, ndufb6_rna, c3, e3, annotations={'Confidence': 'Low', 'Number': '50'})

"""
SET Evidence = "% Entrez Gene summary: Rat: SUMMARY: precursor protein of kinin which is found in plasma; cysteine protease inhibitor and a major acute phase reactant [RGD] OMIM summary: (summary is not available from this source) kininogens; Endogenous peptides present in most body fluids. Certain enzymes convert them to active kinins which are involved in inflammation, blood clotting, complement reactions, etc. Kininogens belong to the cystatin superfamily. They are cysteine proteinase inhibitors. High-molecular-weight kininogen (hmwk) is split by plasma kallikrein to produce bradykinin. Low-molecular-weight kininogen (lmwk) is split by tissue kallikrein to produce kallidin. kinins; Inflammatory mediators that cause dilation of blood vessels and altered vascular permeability.  Kinins are small peptides produced from kininogen by kallikrein and are broken down by kininases. Act on phospholipase and increase arachidonic acid release and thus prostaglandin (PGE2) production. bradykinin; Vasoactive nonapeptide (RPPGFSPFR) formed by action of proteases on kininogens. Very similar to kallidin (which has the same sequence but with an additional N terminal lysine). Bradykinin is a very potent vasodilator and increases permeability of post capillary venules, it acts on endothelial cells to activate phospholipase A2. It is also spasmogenic for some smooth muscle and will cause pain. kallidin; Decapeptide (lysyl bradykinin, amino acid sequence KRPPGFSPFR) produced in kidney. Like bradykinin, an inflammatory mediator (a kinin), causes dilation of renal blood vessels and increased water excretion."
SET Species = 9606
SET Citation = {"Other","Genstruct Kininogen Overview","Genstruct Kininogen Overview","","",""}

bp(GOBP:"inflammatory response") increases rxn(reactants(p(HGNC:KNG1)),products(a(SCHEM:Kallidin)))
path(SDIS:"tissue damage") increases rxn(reactants(p(HGNC:KNG1)),products(a(SCHEM:Kallidin)))
a(SCHEM:Kallidin) increases cat(p(HGNC:BDKRB1))
cat(p(HGNC:BDKRB1)) increases cat(p(SFAM:"PLA2 Family"))
"""

c4 = {
    CITATION_TYPE: CITATION_TYPE_OTHER,
    CITATION_REFERENCE: 'Genstruct Reference',
}
e4 = '% Entrez Gene summary: Rat: SUMMARY: precursor protein of kinin which is found in plasma; cysteine protease inhibitor and a major acute phase reactant [RGD] OMIM summary: (summary is not available from this source) kininogens; Endogenous peptides present in most body fluids. Certain enzymes convert them to active kinins which are involved in inflammation, blood clotting, complement reactions, etc. Kininogens belong to the cystatin superfamily. They are cysteine proteinase inhibitors. High-molecular-weight kininogen (hmwk) is split by plasma kallikrein to produce bradykinin. Low-molecular-weight kininogen (lmwk) is split by tissue kallikrein to produce kallidin. kinins; Inflammatory mediators that cause dilation of blood vessels and altered vascular permeability.  Kinins are small peptides produced from kininogen by kallikrein and are broken down by kininases. Act on phospholipase and increase arachidonic acid release and thus prostaglandin (PGE2) production. bradykinin; Vasoactive nonapeptide (RPPGFSPFR) formed by action of proteases on kininogens. Very similar to kallidin (which has the same sequence but with an additional N terminal lysine). Bradykinin is a very potent vasodilator and increases permeability of post capillary venules, it acts on endothelial cells to activate phospholipase A2. It is also spasmogenic for some smooth muscle and will cause pain. kallidin; Decapeptide (lysyl bradykinin, amino acid sequence KRPPGFSPFR) produced in kidney. Like bradykinin, an inflammatory mediator (a kinin), causes dilation of renal blood vessels and increased water excretion.'
e4 = str(hash(e4))

bdkrb1 = protein('HGNC', 'BDKRB1')
inflammatory_process = bioprocess('GO', 'inflammatory process')
kng1 = protein('HGNC', 'KNG1')
kallidin = abundance('CHEBI', 'Kallidin')
pla2_family = protein('SFAM', 'PLA2 Family')
kng1_to_kallidin = reaction(reactants=[kng1], products=[kallidin])

example_graph.add_increases(inflammatory_process, kng1_to_kallidin, c4, e4)
example_graph.add_increases(kallidin, bdkrb1, c4, e4, object_modifier=catalytic_activity)
example_graph.add_increases(bdkrb1, pla2_family, c4, e4, subject_modifier=catalytic_activity,
                            object_modifier=catalytic_activity)

c5 = '10866298'
e5 = 'We found that PD180970 inhibited in vivo tyrosine phosphorylation of p210Bcr-Abl (IC50 = 170 nM) and the p210BcrAbl substrates Gab2 and CrkL (IC50 = 80 nM) in human K562 chronic myelogenous leukemic cells. In vitro, PD180970 potently inhibited autophosphorylation of p210Bcr-Abl (IC50 = 5 nM) and the kinase activity of purified recombinant Abl tyrosine kinase (IC50 = 2.2 nM).'

"""
SET Species = 9606
SET Citation = {"PubMed","Cancer Res 2000 Jun 15 60(12) 3127-31","10866298","","",""}

kin(p(HGNC:BCR,fus(HGNC:ABL1))) directlyIncreases p(HGNC:CRKL,pmod(P,Y))
kin(p(HGNC:BCR,fus(HGNC:ABL1))) directlyIncreases p(HGNC:GAB2,pmod(P,Y))
"""

bcr_abl1_fus = protein_fusion(partner_5p=protein('HGNC', 'BCR'), partner_3p=protein('HGNC', 'ABL1'))
crkl_ph = protein('HGNC', 'CRKL', variants=[pmod('Ph', 'Tyr')])
gab2_ph = protein('HGNC', 'GAB2', variants=[pmod('Ph', 'Tyr')])

example_graph.add_directly_increases(bcr_abl1_fus, crkl_ph, c5, e5,
                                     annotations={'Species': '9606', 'Confidence': 'High'},
                                     subject_modifier=kinase_activity)
example_graph.add_directly_increases(bcr_abl1_fus, gab2_ph, c5, e5, annotations={'Species': '9606'},
                                     subject_modifier=kinase_activity)
