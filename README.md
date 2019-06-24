# elucidateMULT
A stripped down package to convert MODFLOW mult inputs to Arrays

## Requirements
Numpy
FloPy

## Installation
Download the package and open a command prompt or anaconda prompt  
cd to the elucidateMult directory (where setup.py is located) and run
```
pip install -e .
```

## Example usage
```python
import emult
import os
import matplotlib.pyplot as plt


ws = "./MULT/"
mult = "SVIHM_v3.MUL"

mlt = emult.ModflowMlt.load(os.path.join(ws, mult),
                            nrow=976, ncol=272, ext_unit_dict={})


hk2 = mlt.mult_dict["hk_lay2"]

plt.imshow(hk2.array, interpolation="None")
plt.show()
```

<p align="center">
  <img src="https://raw.githubusercontent.com/jlarsen-usgs/elucidateMULT/master/examples/example.png" alt="example"/>
</p>

## Note
All external arrays defined in the MULT package file must have their path defined relative to the user's python script location.  
See the SVHIM.py and the example mult package file in the examples directory  
https://github.com/jlarsen-usgs/elucidateMULT/tree/master/examples
