import numpy as np
import mfmlt
import os
import matplotlib.pyplot as plt


ws = "./Josh_Test/MULT/"
mult = "SVIHM_v3.MUL"

mlt = mfmlt.ModflowMlt.load(os.path.join(ws, mult),
                            nrow=976, ncol=272, ext_unit_dict={})


hk2 = mlt.mult_dict["hk_lay2"]

plt.imshow(hk2.array, interpolation="None")
plt.show()

print('break')