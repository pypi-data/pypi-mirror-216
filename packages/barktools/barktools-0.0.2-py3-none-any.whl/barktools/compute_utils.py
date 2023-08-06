import numpy as np
import pandas as pd

class MultiBaseNumber:
    """ Class representing a 'multi-base number', i.e. a number whose digits stem from different bases

        E.g. number 1020 with multi-base [2,2,3,4] would be equal to 32

        Parameters
        ---------------
        bases : sequence
            Ordered collection of bases.
            bases[0] is the leftmost base
        digits : sequence
            Digits of the number
            digits[0] is the leftmost digit
    """

    def __init__(self, bases, digits=None):
        if self.__check_bases(bases):
            self.bases = bases
        else:
            raise ArithmeticError('Provided bases are not eligible')

        if digits is None:
            self.digits = [0]*len(self.bases)
        else:
            if self.__check_digits(digits):
                self.digits = digits
            else:
                raise ArithmeticError('Provided digits not compatible with specified bases')

    def __check_bases(self, bases):
        return all([base > 0 for base in bases])

    def __check_digits(self, digits):
        """ Checks if 'digits' is compatible with 'bases'

            Parameters
            ---------------
            digits : sequence 
                Digits of the number

            Returns : bool
                True of digits are compatible with bases, False otherwise
        """
        if len(digits) != len(self.bases): return False
        return all([digits[i] < self.bases[i] for i in range(len(digits))])

    def __eq__(self, other):
        return self.base_10() == other.base_10()

    def __ne__(self, other):
        return self.base_10() != other.base_10()

    def __lt__(self, other):
        return self.base_10() < other.base_10()

    def __gt__(self, other):
        return self.base_10() > other.base_10()

    def __le__(self, other):
        return self.base_10() <= other.base_10()

    def __ge__(self, other):
        return self.base_10() >= other.base_10()

    def base_10(self):
        """ Return the base 10 value of the MultiBaseNumber

            Returns : int
        """
        n, b = 0, 1
        for i in reversed(range(len(self.digits))):
            n = n + b*self.digits[i]
            b = b*self.bases[i]
        return n

class MinusInf:
    def __eq__(self, other):
        return False
    def __ne__(self, other):
        return True
    def __lt__(self, other):
        return True
    def __gt__(self, other):
        return False
    def __le__(self, other):
        return True
    def __ge__(self, other):
        return False
    def __str__(self):
        return '-inf'

class PlusInf():
    def __eq__(self, other):
        return False
    def __ne__(self, other):
        return True
    def __lt__(self, other):
        return False
    def __gt__(self, other):
        return True
    def __le__(self, other):
        return False
    def __ge__(self, other):
        return True
    def __str__(self):
        return '+inf'

def get_brackets(df, col, bracket_edges):
    brackets = pd.Series(np.nan, index=df.index)
    n_brackets = len(bracket_edges)+1
    for iBracket in range(n_brackets):
        lower = bracket_edges[iBracket-1] if (iBracket > 0) else MinusInf()
        upper = bracket_edges[iBracket] if (iBracket < n_brackets-1) else PlusInf()
        brackets.loc[(lower<df[col]) & (df[col]<upper)] = iBracket
    return brackets

# #TODO: Enable include_beyond functionality
# def conditional_group_by(df, col, bracket_edges, include_beyond='both'):
#     ''' Returns a groupby object for df where rows with col in bins defined by bracket_edges grouped together
    
#         Parameters
#         ------------
#         col : str
#             The single column for which to produce brackets w.r.t
#         bracket_edges : list
#             Ordered values (ascending) defining the bracket edges of the column specified by col
#         include_beyond : {'none', 'left', 'right', 'both'}
#             'left' => samples with col value < bracket_edges[0] will be included
#             'right' => samples with col value > bracket_edges[-1] will be included
#             'both' => both 'left' and 'right'
#     '''
#     brackets = get_brackets(df, col, bracket_edges, include_beyond=include_beyond)    
#     return df.groupby(brackets)


'''
Converts an angle in radians in the specified range of 2pi radians of angular length from the lower bound

Examples:
    bind_angle(10deg, 0) == 10deg
    bind_angle(-10deg, 0) == 350deg
    bind_angle(370deg, 0) == 10deg
    bind_angle(-370deg, 0) == 350deg

    bind_angle(10deg, -np.pi) == 10deg
    bind_angle(-10deg, -np.pi) == -10deg
    bind_angle(370deg, -np.pi) == 10deg
    bind_angle(-370deg, -np.pi) == -10deg
'''
def bind_angle(angle, lower_bound):
    return (angle - lower_bound) % (2*np.pi) + lower_bound

'''
Converts an angle in degrees in the specified range of 360 degrees of angular length from the lower bound

Examples:
    bind_angle(10, 0) == 10
    bind_angle(-10, 0) == 350
    bind_angle(370, 0) == 10
    bind_angle(-370, 0) == 350 

    bind_angle(10, -180) == 10
    bind_angle(-10, -180) == -10
    bind_angle(370, -180) == 10
    bind_angle(-370, -180) == -10
'''
def bind_angle_degrees(angle, lower_bound):
    return (angle - lower_bound) % 360 + lower_bound

'''
Returns the minimum signed angular difference between two angles in radians (how many radians in the shortest rotation direction do we need to travel from a to b).
Only when the actual difference between the angles is less than 3pi radians

Examples:
    angular_diff(30deg, 20deg) == 10deg
    angular_diff(20deg, 30deg) == -10deg
    angular_diff(10deg, 350deg) == 20deg
    angular_diff(350deg, 10deg) == -20deg
    angular_diff(180deg, 0deg) == 180deg or -180deg, either one is fine
    angular_diff(0deg, 180deg) == 180deg or -180deg, either one is fine
    angular_diff(90deg, 200deg) == -110deg
    angular_diff(10deg, 200deg) == 170deg
    angular_diff(200deg, 10deg) == -170deg
'''
def angular_diff(b, a):
    if np.abs(b-a)>np.pi:
        return np.sign(a-b)*2*np.pi + (b-a)
    else:
        return (b-a)

'''
Returns the minimum signed angular difference between two angles in degrees (how many degrees in the shortest rotation direction do we need to travel from a to b).
Only when the actual difference between the angles is less than 540 degrees

Examples:
    angular_diff(30, 20) == 10
    angular_diff(20, 30) == -10
    angular_diff(10, 350) == 20
    angular_diff(350, 10) == -20
    angular_diff(180, 0) == 180 or -180, either one is fine
    angular_diff(0, 180) == 180 or -180, either one is fine
    angular_diff(90, 200) == -110
    angular_diff(10, 200) == 170
    angular_diff(200, 10) == -170
'''
def angular_diff_degrees(b, a):
    if np.abs(b-a)>180:
        return np.sign(a-b)*360 + (b-a)
    else:
        return (b-a)
