#!/usr/bin/env python3.6
import json
import os

with open('test/demo_data.json', 'r') as f:
    demo_data = json.load(f)

humans = demo_data['humans']

from mutant import DNAExpert

import logging.config
import yaml

with open('logger.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

_logger = logging.getLogger(__name__)

if __name__ == "__main__":
    _logger.info("✓ Inicio tests del experto")
    bad_matrix_msg = "Deberia ser None, ya que la matriz mal formada"
    assert DNAExpert().isMutant([]) == None, bad_matrix_msg
    assert DNAExpert().isMutant(["AD"]) == None, bad_matrix_msg
    assert DNAExpert().isMutant([["AD"], 2]) == None, bad_matrix_msg
    assert DNAExpert().isMutant([["AD"], ["DDER"]]) == None, bad_matrix_msg
    assert DNAExpert().isMutant([["AAAA"], ["GGGG"]]) == None, bad_matrix_msg
    assert DNAExpert().isMutant([["AA"], ["GG"]]) == None, bad_matrix_msg
    _logger.info("✓ Probado Matrices mal vacias / mal formadas")
    for human in humans[0]['notmutants']:
        isMutant = DNAExpert().isMutant(human)
        assert isMutant == False, "Mutante deberia ser falso"
    _logger.info("✓ Probado DNA de Humanos No Mutantes")
    for human in humans[1]['mutants']:
        isMutant = DNAExpert().isMutant(human)
        assert isMutant == True, "Mutante deberia ser verdadero"
    _logger.info("✓ Probado DNA de Humanos Mutantes")





