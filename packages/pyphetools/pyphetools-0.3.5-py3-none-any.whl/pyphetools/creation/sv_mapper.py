
from .structural_variant import StructuralVariant


class SvMapper:
    def __init__(self,  
                 gene_symbol,
                 gene_id,
                 sequence_ontology_id,
                 sequence_ontology_label,
                 genotype) -> None:
        self._gene_symbol = gene_symbol
        self._gene_id = gene_id
        self._sequence_ontology_id = sequence_ontology_id
        self._sequence_ontology_label = sequence_ontology_label
        self._genotype = genotype
        
    def map_cell(self, cell_contents, variant_id=None):
        return StructuralVariant(cell_contents=cell_contents,
                                 gene_symbol=self._gene_symbol,
                                 gene_id=self._gene_id,
                                 sequence_ontology_id=self._sequence_ontology_id,
                                 sequence_ontology_label=self._sequence_ontology_label,
                                 genotype=self._genotype,
                                 variant_id=variant_id)