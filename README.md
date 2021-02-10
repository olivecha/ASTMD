# ASTMD
Python code to do the computations for ASTM D series standards\
```import ASTMD```\
includes the following standards : 

## ASTM D790 : Standard Test Methods for Flexural Properties of Unreinforced and Reinforced Plastics and Electrical Insulating Material
```
Material = ASTMD.D790(filenames, widths, depths, span, mtr_name="", largespan=False, validate_modulus=False)
```
```filenames``` : List of paths to the test data files\
```widths``` : List of the samples widths\
```depths``` : List of the samples depths (thickness)\
```span``` : Span used to test the material\
```mtr_name``` : String for the material name (optional)\
```largespan``` : ```True``` if the test were done using the largespan procedure\
```validate_modulus``` : if ```True``` Adds a plot of all the modulus lines to visualise the data\

- Computes the flexural stress and strain with equations in ASTM D790 
- Finds average flexural stress for all samples
- Finds average tangent modulus 
- Plots the stress-strain curve
- Plots the modulus line 
- Returns a result_D790.txt file in the same directory as the test data


## ASTM D3039 : Standard Test Method for Tensile Properties of Polymer Matrix Composite Materials
```
Material = ASTMD.D3039(filenames, widths, thicknesses, lengths, mtr_name="", extensiometer_length=50.8, validate_modulus=False)
```
```filenames``` : List of paths to the test data files\
```widths``` : List of the samples widths\
```thicknesses``` : List of the samples thicknesses\
```lenths``` : List of the samples lengths \
```mtr_name``` : String for the material name (optional)\
```extensiometer_length``` : Length of the extensiometer used to measure deformation\
```validate_modulus``` :  if ```True``` Adds a plot of all the modulus lines to visualise the data\

- Computes the tensile stress and strain with equations in ASTM D3039
- Finds average tensile strenght
- Finds average chord modulus from data points at strain = 0.001 and strain  = 0.002 as per ASTM D3039 standard
- Plots the stress-strain curve
- Plots the modulus line 
- Returns a result_D3039.txt file in the same directory as the test data


## ASTM D5868 : Test Method for Lap Shear Adhesion for Fiber Reinforced Plastic (FRP) Bonding
```
Material = ASTMD.D5868(filenames, areas, mtr_name="")
```
```filenames``` : List of paths to the test data files\
```areas``` : List of the samples areas\
```mtr_name``` : String for the material name (optional)\

1. Computes the shear stress at the bonded joint
2. Finds the average shear strength
3. Plots the stress-time curve (just to show the data)
4. Returns a result_D5868.tct file in the same directory as the test data


