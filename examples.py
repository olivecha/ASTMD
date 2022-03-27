import ASTMD

# A report file is created for each standard

# ASTM D790 test report (bending stiffness)
sample_files = [f'test/test_data_D790/sample{i}.txt' for i in range(1, 7)]  # change for your files
sample_widths = [10, 10.1, 9.9, 10, 10.1, 9.9]  # mm # Width of all samples
sample_depths = [1.05, 1.03, 0.97, 0.98, 1.02, 0.99]  # mm  # Depth of all samples
span_used = 100  # mm
ASTMD.D790(sample_files, sample_widths, sample_depths, span_used, mtr_name="carbon")

# ASTM D3039 test report (tensile modulus)
sample_files = [f'test/test_data_D3039/sample{i}.txt' for i in range(1, 4)]
sample_widths = [15.05, 14.95, 14.97, 15.02]
sample_thicknesses = [1.01, 1.02, 0.99, 0.98]
sample_lengths = [250.5, 249.5, 250.3, 249.8]
ASTMD.D3039(sample_files, sample_widths, sample_thicknesses, sample_lengths, mtr_name='Flax',
            extensiometer_length=50.8)

# ASTM D5868 test report (Lap shear adhesion)
filenames = [f'test/test_data_D5868/sample{i}.txt' for i in range(1, 3)]
areas = [25.3 * 25.4, 25.4 * 25.5]
ASTMD.D5868(filenames, areas, mtr_name='flax and wood glue')
