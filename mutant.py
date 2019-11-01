#!/usr/bin/env python3.6
import numpy
import re
import logging
import logging.config
import yaml
import sys
import json
import datetime

helmet_ascii = \
"""
       ___________________
      /.-------+-+------.\\\\
     //        :|:     :::\\\\
    //         :|:       ::\\\\
   //          :|:       :::\\\\
  //           :|:       ::::\\\\
 //            :|:         :::\\\\
((             :|:          :::))
||     _______/:|:\_______   ::||
||    /.-----.\:|:/.-----.\ :.:||
||   ((       ))|((       ))  :||
||    \\\\_    //:|:\\\\    _//   :||
||:     \\\\  (( :|: ))  //     :||
||::     \\\\  \\\\:|://  //     ::||
||::      \\\\  \\\\_//  //     :::||
||::       \\\\  `-'  //     ::::||
||::        ))     ((  <<()>>::||
||::       //       \\\\   ::::::||
((::      //         \\\\ :::::::))
 \\\\______//           \\\\______//
  `------'             `------'
"""


with open('logger.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

_logger = logging.getLogger(__name__)
_logger.info(helmet_ascii)

DNA_WORD_REGEX = "^([ATGC]*)$"
MUTANT_SEQ_REGEX = r'([ATGC])\1{3}'
COUNT_GT_POSITIVE = 1
positive_seq = re.compile(MUTANT_SEQ_REGEX)


def split(word):
    return [char for char in word]


def get_matrix_from_array(array_string):
    matrix = [dna_word for dna_word in array_string]
    return matrix


class DNAExpert:

    def isMutant(self, matrix=[]):

        def __check_matrix_order(matrix):
            shape = numpy.shape(matrix)[0]
            return all([shape == len(m) for m in matrix])

        def __check_regex(array_string):
            error = 0
            for dna_string in array_string:
                if not re.compile(DNA_WORD_REGEX):
                    error = 1
                if error:
                    break
            return not error

        if not matrix:
            _logger.debug("Matrix empty")
            return False
        if not __check_matrix_order(matrix):
            _logger.debug("Bad order matrix %s" % str(matrix))
            return False
        if not __check_regex(matrix):
            _logger.debug("Bad regex matrix %s" % str(matrix))
            return False

        is_mutant = None

        matrix_order = numpy.shape(matrix)[0]
        contador = 0
        while is_mutant is None:
            for dna_word in matrix:
                contador += positive_seq.search(dna_word) != None
            if contador > COUNT_GT_POSITIVE:
                _logger.debug("horizontal")
                is_mutant = True
                break
            else:
                matrix_letters = [[ch for ch in word] for word in matrix]
                matrix_rotated = numpy.transpose(matrix_letters)
                for dna_word in matrix_rotated:
                    contador += positive_seq.search(''.join(dna_word)) != None
                if contador > COUNT_GT_POSITIVE:
                    _logger.debug("vertical")
                    is_mutant = True
                    break
                else:
                    diagonal = numpy.diagonal(matrix_letters)
                    contador += positive_seq.search(''.join(diagonal)) != None
                    if contador > COUNT_GT_POSITIVE:
                        _logger.debug("diagonal 1")
                        is_mutant = True
                        break
                    else:
                        for x in range(1, matrix_order):
                            aux = numpy.transpose(matrix_letters).tolist()
                            newm = aux[1:]
                            newm.append(aux[0])
                            newm = numpy.transpose(newm).tolist()
                            diagonal = numpy.diagonal(newm)
                            contador += positive_seq.search(''.join(diagonal)) != None
                            if contador > COUNT_GT_POSITIVE:
                                _logger.debug("diagonal 1")
                                is_mutant = True
                                break
            is_mutant = False

        _logger.debug("Resultado: %s %s %s" % (matrix, is_mutant, ':)' if is_mutant else ':('))
        return is_mutant


def run():
    if '{' in sys.argv[1]:
        args = sys.argv[1].replace('{', '').replace('}', '').replace(';', '').replace('"', '').split(',')
        array_string = [str(arg) for arg in args]
    else:
        array_string = [str(arg) for arg in sys.argv[1:]]
    matrix = get_matrix_from_array(array_string)
    _logger.warning(datetime.datetime.now())
    for x in range(0,999999):
        DNAExpert().isMutant(matrix)
    _logger.warning(datetime.datetime.now())



if __name__ == "__main__":
    run()
