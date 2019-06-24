import emult
import os
import matplotlib.pyplot as plt
import numpy as np


ws = "./MULT/"
mult = "SVIHM_v3.MUL"

mlt = emult.ModflowMlt.load(os.path.join(ws, mult),
                            nrow=976, ncol=272, ext_unit_dict={})

# items in mult_dict are objects,
mult_dict = mlt.mult_dict

# to get the array of hk_lay2
hk2 = mult_dict["hk_lay2"].array

# alternately you can call hk_lay2 attribute and get the array
hk2 = mlt.hk_lay2

# to loop through and plot everything!
for key, value in mult_dict.items():
    plt.imshow(value.array, interpolation="None")
    plt.colorbar()
    plt.title(key)
    plt.show()

# to write everything in the dict into array files
ws = "output_arrays"
for key, value in mult_dict.items():
    fname = key + ".txt"
    np.savetxt(os.path.join(ws, fname), value.array, delimiter=" ", fmt="%.6f")

# to plot
plt.imshow(hk2, interpolation="None")
plt.show()
