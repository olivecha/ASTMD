import ASTMD

#Test_Material1 = ASTMD.D790(["Flexion/g3_4.txt", "Flexion/g3_6.txt"], [25.4, 24.5], [1, 1.1], 150, mtr_name="Test Material")

#Test_Material2 = ASTMD.D3039(["Tension/0_1.txt", "Tension/0_2.txt"], [12.5, 12.4], [1, 1.1], [250, 250], mtr_name="Tensile Test")

Test_Material3 = ASTMD.D5868(["Lap Shear/S_1.txt", "Lap Shear/S_2.txt"], [25.4**2, 25**2])
