# ASTMD
Python code to do the computations for ASTM D series standards

See example.py which computes the results files from example data for every available standard


### includes the following standards : 

## ASTM D790 : Standard Test Methods for Flexural Properties of Unreinforced and Reinforced Plastics and Electrical Insulating Material
```python
ASTMD.D790(filenames, widths, depths, span_used, mtr_name="", largespan=False)
```
```filenames``` : List of paths to the test data files\
```widths``` : List of the samples widths\
```depths``` : List of the samples depths (thickness)\
```span``` : Span used to test the material\
```mtr_name``` : String for the material name (optional)\
```largespan``` : ```True``` if the test were done using the largespan procedure\

A `.docx` file is written with the name `ASTM_D790_test_report.docx`.


## ASTM D3039 : Standard Test Method for Tensile Properties of Polymer Matrix Composite Materials
```python
Material = ASTMD.D3039(filenames, widths, thicknesses, lengths, mtr_name="", extensiometer_length=50.8)
```
```filenames``` : List of paths to the test data files\
```widths``` : List of the samples widths\
```thicknesses``` : List of the samples thicknesses\
```lenths``` : List of the samples lengths \
```mtr_name``` : String for the material name\
```extensiometer_length``` : Length of the extensiometer used to measure deformation (mm)\

A `.docx` file is written with the name `ASTM_D3039_test_report.docx`.


## ASTM D5868 : Test Method for Lap Shear Adhesion for Fiber Reinforced Plastic (FRP) Bonding
```
Material = ASTMD.D5868(filenames, areas, mtr_name="")
```
```filenames``` : List of paths to the test data files\
```areas``` : List of the samples areas (mm$^2$)\
```mtr_name``` : String for the material name (optional)\

A `.docx` file is written with the name `ASTM_D5868_test_report.docx`.


### Dependencies
numpy/
pandas/
mathplotlib.pyplot/
python-docx/
