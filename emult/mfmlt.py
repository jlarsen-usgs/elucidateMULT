"""
mfmlt module.  Contains the ModflowMlt class. Note that the user can access
the ModflowMlt class as `flopy.modflow.ModflowMlt`.

Additional information for this MODFLOW package can be found at the `Online
MODFLOW Guide
<http://water.usgs.gov/ogw/modflow-nwt/MODFLOW-NWT-Guide/mult.htm>`_.

"""
import collections
import numpy as np

from flopy.utils import Util2d
from .expression_parser import FunctionParser, ExpressionParser


class ModflowMlt(object):
    """
    MODFLOW Mult Package Class.

    Parameters
    ----------
    mult_dict : dict
        Dictionary with mult data for the model. mult_dict is typically
        instantiated using load method.

    Attributes
    ----------

    Methods
    -------

    See Also
    --------


    Examples
    --------

    >>> import emult
    >>>
    >>> mlt = emult.ModflowMlt.load("test.mult", nrow=10, ncol=10)

    """

    def __init__(self, mult_dict=None, mult_equations=None):

        self.nml = 0
        if mult_dict is not None:
            self.nml = len(mult_dict)
            self.mult_dict = mult_dict
            self.mult_equations = mult_equations

    def __getattr__(self, item):
        """
        Syntactic sugar!!!!!

        Parameters:
            item: attiribute name

        Returns:
            attribute or numpy array!
        """
        if item in self.mult_dict:
            return self.mult_dict[item].array
        else:
            super(self, ModflowMlt).__getattribute__(item)

    @staticmethod
    def load(f, nrow, ncol, ext_unit_dict=None):
        """
        Load an existing package.

        Parameters
        ----------
        f : filename or file handle
            File to load.
        nrow : int
            number of rows.
        ncol : int
            number of columns.
        ext_unit_dict : dictionary, optional
            If the arrays in the file are specified using EXTERNAL,
            or older style array control records, then `f` should be a file
            handle.  In this case ext_unit_dict is required, which can be
            constructed using the function
            :class:`flopy.utils.mfreadnam.parsenamefile`.

        Returns
        -------
        zone : ModflowMult dict

        Examples
        --------

        >>> import flopy
        >>> m = flopy.modflow.Modflow()
        >>> mlt = flopy.modflow.ModflowMlt.load('test.mlt', m)

        """
        import flopy as fp

        model = fp.modflow.Modflow("imadummy")

        if not hasattr(f, 'read'):
            filename = f
            f = open(filename, 'r')
        # dataset 0 -- __header
        while True:
            line = f.readline()
            if line[0] != '#':
                break

        # dataset 1
        t = line.strip().split()
        nml = int(t[0])

        # read zone data
        mult_dict = collections.OrderedDict()
        mult_equations = collections.OrderedDict()
        for n in range(nml):
            line = f.readline()
            while True:
                if line.strip().startswith("#"):
                    line = f.readline()
                else:
                    break
            print("Reading : {}".format(line.strip().split()[0]))
            t = line.strip().split()
            if len(t[0]) > 10:
                mltnam = t[0][0:10].lower()
            else:
                mltnam = t[0].lower()

            readArray = True
            kwrd = None
            if len(t) > 1:
                if 'function' in t[1].lower() or 'expression' in t[1].lower():
                    readArray = False
                    kwrd = t[1].lower()
            # load data
            if readArray:
                t = Util2d.load(f, model, (nrow, ncol), np.float32, mltnam,
                                ext_unit_dict)

            else:
                line = f.readline().rstrip()
                t = [kwrd, line]
                if kwrd == 'function':
                    parser = FunctionParser(line, mult_dict)
                elif kwrd == 'expression':
                    parser = ExpressionParser(line, mult_dict)
                else:
                    raise TypeError('{}: not a Function or Expression'
                                    .format(kwrd))
                mult_equations[mltnam] = {'keyword': kwrd,
                                          'equation': line}

                t = Util2d(model, parser.result.shape, np.float32,
                           parser.result, mltnam)

            mult_dict[mltnam] = t

        # create mlt dictionary
        mlt = ModflowMlt(mult_dict=mult_dict,
                         mult_equations=mult_equations)

        return mlt

    @staticmethod
    def ftype():
        return 'MULT'

    @staticmethod
    def defaultunit():
        return 1002
