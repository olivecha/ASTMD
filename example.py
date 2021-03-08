import ASTMD

Material_1 = ASTMD.D790(["Sample_Data.txt"], [25.4], [1], 150, mtr_name="Flexural Test")
Material_2 = ASTMD.D3039(["Sample_Data.txt"], [12.5], [1], [250], extensiometer_length=50.8, mtr_name="Tensile Test")
Material_3 = ASTMD.D5868(["Sample_Data.txt"], [25.4**2])




