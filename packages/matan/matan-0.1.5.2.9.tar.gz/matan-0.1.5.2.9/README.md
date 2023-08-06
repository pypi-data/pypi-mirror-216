**This package is still under development. Be aware of often updates!**
# MaTan

Shortcut comes from **Mat**erial **An**analysis - ultimately is should contains modules allowing user to calculate metals and polymers properties from tensile, HDT (polymers) and DSC tests, as well as the others. There are few similar  packages in PyPI, but none of them I found good to me, so I wrote new one. 

For now it includes:
- ISO:527-1 (polymers analysis)

# [Documentation](https://matan.codeberg.page)


# Abstract

Nowadays, Python is one of the most popular programming languages, even in non-informatics fields like mechanical engineering, due to its simplicity, and computer analysis solvers using FEM methods are part of almost all components, albeit access to material data is sometimes hard due to inadequate data in the datasheets, problems with calculations, inconsistent information, etc. To overcome this problem, the Python package was created, which allows to calculate the stress, strains, tensile modulus, and other properties from force and elongation data from a machine. For now, it includes only polymer tests according to the ISO-527-1 standard, but in the future, other standards should be included.

Moreover, the package would need a graphical user interface, which could make it even simpler to use and, more importantly, allow users to upload their obtained results into OpenAccess databases and export plastic strains, tensile modulus, and other properties needed to perform FEM and other numerical analysis. That could make FEM methods even more accessible, which would lead to a decrease in the use of unnecessary materials and, due to this, less CO2 pollution.


# How to use it?

Just simply put elongation and force arrays into sample

Be aware that sometimes csv files can have diffrent extension depends on machine manufacturer. To be sure just check it using simples notepad, or try to read it by pandas.

```python
import matan as mt
import pandas as pd

path_to_your_CSV = r"path/to/your/CSV"


'''
Be aware that somethimes some software machines uses diffrent encoding! Check the documentation of pandas.read_csv for more
'''
df = pd.read_csv(path_to_your_CSV)

elongation_array=df["elongation"]
force_array=df["force"]

# This uses N ewtons and mm by default to ensure [N/mm^2] as it is equal to MPa
# by default force units are Newtons and lenght units are mm
example=mt.sample(name="your sample name",
thickness = 5,
width= 5,
elongation_array=elongation_array,
force_array=force_array
)




#Use method below to convert engineering values into  real
example.calculate_real_values()

# tensile modulus values between engineering value and real value
print(ext.eng_values.tensile_modulus,
ext.real_values.tensile_modulus)

# Engineering values
# Value of strenght
print(ext.eng_values.strength.value,
ext.eng_values.strength.strain)

# Values at break
print(ext.eng_values.at_break.stress,
ext.eng_values.at_break.strain)

# Yield strenght values
print(ext.eng_values.yield_strength.value,
ext.eng_values.yield_strength.strain)

# Real values
# Value of strenght
print(ext.real_values.strength.value,
ext.real_values.strength.strain)

# Values at break
print(ext.real_values.at_break.stress,
ext.real_values.at_break.strain)

# Yield strenght values
print(ext.real_values.yield_strength.value,
ext.real_values.yield_strength.strain)

```



