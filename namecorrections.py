
import numpy as np
import pandas as pd

import unicodedata

def strip_accents(text):
    """
    https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def rearrange_name(player_name):
    """toggles names between last,first and first last """
    if ',' in player_name:
        return player_name.split(',')[1]+' '+player_name.split(',')[0]
    else:
        name_length = len(player_name.split(' '))
        if name_length==2:
            return player_name.split(' ')[1]+', '+player_name.split(' ')[0]
        if name_length==3:
            return player_name.split(' ')[1]+' '+player_name.split(' ')[2]+', '+player_name.split(' ')[0]


switchdict = dict()
switchdict['Cedric Mullins'] = 'Cedric Mullins II'
switchdict['Hyun Jin Ryu'] = 'Hyun-Jin Ryu'
switchdict['Kwang Hyun Kim'] = 'Kwang-hyun Kim'
switchdict['Alfonso Rivas'] = 'Alfonso Rivas III'
switchdict['Andrew Young'] = 'Andy Young'
switchdict['AJ Pollock'] = 'A.J. Pollock'
switchdict['J.C. Mejia'] = 'JC Mejia'
switchdict['DJ Stewart'] = 'D.J. Stewart'
switchdict['Ha-Seong Kim'] = 'Ha-seong Kim'
switchdict['JD Hammer'] = 'J.D. Hammer'
switchdict['TJ Friedl'] = 'T.J. Friedl'
