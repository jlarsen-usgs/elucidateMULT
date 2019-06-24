import emult
import os
import matplotlib.pyplot as plt


ws = "./MULT/"
mult = "SVIHM_v3.MUL"

mlt = emult.ModflowMlt.load(os.path.join(ws, mult),
                            nrow=976, ncol=272, ext_unit_dict={})


hk2 = mlt.mult_dict["hk_lay2"]
hk2 = mlt.hk_lay2
plt.imshow(hk2, interpolation="None")
plt.show()

print('break')