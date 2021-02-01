import os
import numpy as np


def prt(text=None):
    """ Test print text.
    :param text: str text.
    :return: None.
    """
    print("Make PyLib TEST...!!! >> {} <<".format(text))


def sq(x=0):
    """ Caculator square of number.
    :param num: number or array input.
    :return: number ** 2
    """
    return np.square(x)
