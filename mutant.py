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
COUNT_GT_LETTERS = 3
positive_seq = re.compile(MUTANT_SEQ_REGEX)


def split(word):
    return [char for char in word]


def get_matrix_from_array(array_string):
    matrix = [dna_word for dna_word in array_string]
    return matrix

def get_diagonals(matrix):
    n = len(matrix)
    # diagonals_1 = []  # lower-left-to-upper-right diagonals
    # diagonals_2 = []  # upper-left-to-lower-right diagonals
    for p in range(2*n-1):
        yield [matrix[p-q][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)]
        yield [matrix[n-p+q-1][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)]


class DNAExpert:

    def isMutant(self, matrix=[]):

        try:
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
              return None

            if not __check_matrix_order(matrix):
               _logger.debug("Bad order matrix %s" % str(matrix))
               return None

            if not __check_regex(matrix):
               _logger.debug("Bad regex matrix %s" % str(matrix))
               return None


            is_mutant = None
            matrix_order = numpy.shape(matrix)[0]
            contador = 0
            for dna_word in matrix:
                contador += dna_word.find('AAAA') != -1 or 0
                contador += dna_word.find('CCCC') != -1 or 0
                contador += dna_word.find('TTTT') != -1 or 0
                contador += dna_word.find('GGGG') != -1 or 0
                if contador > COUNT_GT_POSITIVE:
                    _logger.debug("horizontal")
                    is_mutant = True
                    break
            if not is_mutant:
                matrix_letters = [[ch for ch in word] for word in matrix]
                words = numpy.transpose(matrix_letters)
                for dna_word in words:
                    word = ''.join(dna_word)
                    contador += word.find('AAAA') != -1 or 0
                    contador += word.find('CCCC') != -1 or 0
                    contador += word.find('TTTT') != -1 or 0
                    contador += word.find('GGGG') != -1 or 0
                    if contador > COUNT_GT_POSITIVE:
                        _logger.debug("vertical")
                        is_mutant = True
                        break
            if not is_mutant:
                for dna_word in get_diagonals(matrix_letters):
                    if len(dna_word) > COUNT_GT_LETTERS:
                        word = ''.join(dna_word)
                        contador += word.find('AAAA') != -1 or 0
                        contador += word.find('CCCC') != -1 or 0
                        contador += word.find('TTTT') != -1 or 0
                        contador += word.find('GGGG') != -1 or 0
                        if contador > COUNT_GT_POSITIVE:
                            _logger.debug("diagonal")
                            is_mutant = True
                            break
            if is_mutant == None:
               is_mutant = False
            _logger.debug("Resultado: %s %s %s" % (matrix, is_mutant, ':)' if is_mutant else ':('))
            return is_mutant
        except Exception as e:
            _logger.warning("Error con %s" % str(matrix))
            _logger.warning(e)
            return None


def run():
    if '{' in sys.argv[1]:
        args = sys.argv[1].replace('{', '').replace('}', '').replace(';', '').replace('"', '').split(',')
        array_string = [str(arg) for arg in args]
    else:
        array_string = [str(arg) for arg in sys.argv[1:]]
    matrix = get_matrix_from_array(array_string)
    DNAExpert().isMutant(matrix)

if __name__ == "__main__":
    run()
