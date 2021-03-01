import ASTMD_util
import numpy as np
import matplotlib.pyplot as plt


#  Standard Test Methods for Flexural Properties of Unreinforced and Reinforced Plastics and
#  Electrical Insulating Materials
class D790(object):
    def __init__(self, filenames, widths, depths, span, mtr_name="", largespan=False, validate_modulus=False):
        self.tests = list()  # individual tests for the samples
        self.widths = widths  # widths of the samples (list)
        self.depths = depths  # depths of the samples (list)
        self.span = span  # span used to test the samples (float)
        self.name = mtr_name
        self.stresses = list()  # allocate namespace for individual stresses
        self.strains = list()  # allocate namespace for individual strains
        self.largespan = largespan  # special case for large span samples
        self.filenames = filenames
        self.get_test_data()
        self.get_stress_strain()
        self.plot_stress_strain()
        self.get_rupture()
        self.get_tgt_modulus()
        self.plot_modulus()
        self.print_results()
        if validate_modulus:
            self.plot_all_modulus()

    # get the test data
    get_test_data = ASTMD_util.get_test_data

    # Compute stress and strain from deflexion and load
    def get_stress_strain(self):

        for index, test in enumerate(self.tests):
            stress = list()
            strain = list()

            # Calculate stress for standard span
            if self.largespan:
                for force, pos in zip(test["Load"].astype(float), test["Crosshead"].astype(float)):
                    # Eq. 4 in ASTM D790 section 12.3
                    stress.append((3 * force * self.span) / (2 * self.widths[index] * self.depths[index] ** 2) *
                                  (1 + 6 * (pos / self.span) ** 2 - 4 * (self.depths[index] / self.span) * (
                                          pos / self.span)))
                self.stresses.append(stress)

            # Calculate stress for large span
            else:
                for force in test["Load"].astype(float):
                    # Eq. 3 in ASTM D790 section 12.2
                    print(type(force))
                    stress.append((3 * force * self.span) / (2 * self.widths[index] * self.depths[index] ** 2))
                self.stresses.append(stress)

            # Calculate flexural strain at max strain
            for pos in test["Crosshead"].astype(float):
                # Eq. 5 in ASTM D790 section 12.4
                strain.append((6 * float(pos) * self.depths[index]) / (self.span ** 2))

            self.strains.append(strain)

        # Compute the average flexural stress and strains
        self.avg_strain = ASTMD_util.avg(self.strains)
        self.avg_stress = ASTMD_util.avg(self.stresses)

    # get the rupture stress
    def get_rupture(self):
        # max stress = strength
        self.strengths = [max(column) for column in self.stresses]

        # Compute average strength
        self.avg_strength = sum(self.strengths) / len(self.stresses)

        # Compute Standard deviation from all samples
        if len(self.stresses) > 1:
            self.sd_strength = np.sqrt(
                (sum([x ** 2 for x in self.strengths]) - len(self.stresses) * self.avg_strength ** 2) / (
                        len(self.stresses) - 1))
        else:
            self.sd_strength = 0

    # get the tangent modulus
    def get_tgt_modulus(self):

        self.modulus = list()  # allocate namespace for modulus
        #  Compute the modulus for each test
        for test, width, depth in zip(self.tests, self.widths, self.depths):

            # Get max slope in the load - deflection plot
            loads = [load for load in test["Load"].astype(float)]
            loads = [load for load in loads[:loads.index(max(loads))]]
            deflexions = [deflexion for deflexion in test["Crosshead"].astype(float)]
            deflexions = [deflexion for deflexion in deflexions[:len(loads)]]

            slopes = list()
            for e in range(0, len(loads) - 25, 5):
                slopes.append((loads[e + 25] - loads[e]) / (deflexions[e + 25] - deflexions[e]))

            m = max(slopes)

            # Eq. 6 dans ASTM D790 section 12.5
            self.modulus.append((self.span ** 3 * m) / (4 * width * depth ** 3))

        if len(self.modulus) > 1:
            self.avg_modulus = sum(self.modulus)/len(self.modulus)
            self.sd_modulus = np.sqrt(
                (sum([x ** 2 for x in self.modulus]) - len(self.modulus) * self.avg_modulus ** 2) / (
                        len(self.modulus) - 1))
        else:
            self.avg_modulus = self.modulus[0]
            self.sd_modulus = 0

    # print the test results in a text file
    def print_results(self):
        path = self.filenames[0].split("/")
        name = "results_D790.txt"
        if len(path) > 1:
            path = "/".join(path[:-1]) + "/" + name
        else:
            path = name

        result_file = open(path, "w")
        result_file.write("ASTM D790 Standard Report" + "\n")
        result_file.write("\n")
        result_file.write("1. Testing parameters" + "\n")
        result_file.write("Material name : " + self.name + "\n")
        result_file.write("Width of samples : " + "mm, ".join(map(str, self.widths)) + "mm" + "\n")
        result_file.write("Depths of samples : " + "mm, ".join(map(str, self.depths)) + "mm" + "\n")
        result_file.write("Span used : " + str(self.span))
        if self.largespan:
            result_file.write(" (Large span)" + "\n")
        else:
            result_file.write("\n")
        result_file.write("\n")
        result_file.write("2. Test Results" + "\n")
        result_file.write("Tangent modulus : " + str(round(self.avg_modulus, 0)) + " MPa" + "\n")
        result_file.write("Standard Deviation : " + "(" + str(round(self.sd_modulus, 0)) + ")" + "\n")
        result_file.write("Flexural strength : " + str(round(self.avg_strength, 0)) + " MPa" + "\n")
        result_file.write("Standard Deviation : " + "(" + str(round(self.sd_strength, 0)) + ")" + "\n")

    # plot the stress strain curves with average
    def plot_stress_strain(self):
        # Plot the stress strain curve
        plt.figure("Flexural Stress_Strain")
        for stress, strain in zip(self.stresses, self.strains):
            plot1, = plt.plot(strain, stress, "#B2B2B2")
        plot1.set_label("Samples")
        plot1, = plt.plot(self.avg_strain, self.avg_stress, "r")
        plot1.set_label("Average")
        plt.legend()
        plt.title("Stress-Strain curve")
        plt.ylabel("Stress at bottom face of the sample (MPa)")
        plt.xlabel("Strain at the bottom face of the sample (mm/mm)")
        plt.grid(which='both')

    # plot the average modulus line on the stress strain graph
    def plot_modulus(self):
        # Plot the modulus with the stress strain curve
        plt.figure("Flexural Modulus")
        plot1, = plt.plot(self.avg_strain, self.avg_stress)
        plot1.set_label("SS Curve")
        plot1, = plt.plot(self.avg_strain[:self.avg_stress.index(max(self.avg_stress))],
                          [strain * self.avg_modulus for strain in self.avg_strain][
                          :self.avg_stress.index(max(self.avg_stress))], "r")
        plot1.set_label("Modulus")
        plt.legend()
        plt.title("Tangent modulus and Stress Strain curve")
        plt.ylabel("Stress (MPa)")
        plt.xlabel("Strain (mm/mm)")
        plt.grid(which='both')

    # Plot all modulus values with stress strain curves for validation
    def plot_all_modulus(self):
        plt.figure("All Flex")
        for module, stress, strain in zip(self.modulus, self.stresses[1:], self.strains[1:]):
            plot1, = plt.plot(strain, stress, "#B2B2B2")
            plot2, = plt.plot(strain[:stress.index(max(stress))],
                              [value * module for value in strain][:stress.index(max(stress))], "r")
        plot1.set_label("Samples")
        plot2.set_label("modulus")


# Tensile Properties of Polymer Matrix Composite Materials
class D3039(object):
    def __init__(self, filenames, widths, thicknesses, lengths, mtr_name="", extensiometer_length=50.8, validate_modulus=False):
        self.name = mtr_name  # Material name
        self.tests = list()  # individual tests for the samples
        self.widths = widths  # widths of the samples (list)
        self.thicknesses = thicknesses  # Thickness of the samples
        self.lengths = lengths  # span used to test the samples (float)
        self.extensiometer_length = extensiometer_length
        self.stresses = list()  # allocate namespace for individual stresses
        self.strains = list()  # allocate namespace for individual strains
        self.filenames = filenames  # filenames of the test data
        self.get_test_data()  # Import the the test data
        self.get_stress_strain()  # Compute stress and strains
        self.trim_stress_strain()  # Trim the values above max stress
        self.plot_stress_strain()  # Plot the stress strain graph
        self.get_rupture()  # Compute the max stress (break)
        self.get_chord_modulus()  # Compute the tangent modulus
        self.plot_modulus()  # Plot the modulus with stress-strain
        self.print_results()  # Print result values to text file
        if validate_modulus:
            self.plot_all_modulus()

    # Function to import the test data
    get_test_data = ASTMD_util.get_test_data

    # Compute stress and strain from Extensometer and load
    def get_stress_strain(self):

        for test, width, thickness in zip(self.tests, self.widths, self.thicknesses):
            stress = list()
            strain = list()

            for force in test["Load"].astype(float):
                #Eq. 6 Standard ASTM D3039 Section 13
                stress.append(force / (width * thickness))

            for extension in test["Extensometer"].astype(float):
                #Eq. 7 Standard ASTM D3039 Section 13
                strain.append(extension / self.extensiometer_length)

            self.stresses.append(stress)
            self.strains.append(strain)

    # Trim stress strain values after max stress (rupture)
    def trim_stress_strain(self):

        # Trim stress strain to max stress
        trimmed_stress = list()
        trimmed_strain = list()
        for stress, strain in zip(self.stresses, self.strains):
            stress = stress[:stress.index(max(stress))]
            trimmed_stress.append(stress)
            strain = strain[:len(stress)]
            trimmed_strain.append(strain)
        self.stresses = trimmed_stress
        self.strains = trimmed_strain

        # Get the length of the shortest vector
        lengths = list()
        for stress in self.stresses:
            lengths.append(len(stress))
        self.min_len = min(lengths)

        # Trim the average stress strains
        self.avg_strain = ASTMD_util.avg(self.strains)
        self.avg_strain = self.avg_strain[:self.min_len]
        self.avg_stress = ASTMD_util.avg(self.stresses)
        self.avg_stress = self.avg_stress[:self.min_len]

    # Get the stress at break
    def get_rupture(self):
        #  Max stress from Eq. 5 Standard ASTM D3039 Section 13
        self.strengths = [max(column) for column in self.stresses]
        # Compute average strength
        self.avg_strength = sum(self.strengths) / len(self.stresses)
        # Compute Standard deviation from all samples
        if len(self.stresses) > 1:
            self.sd_strength = np.sqrt(
                (sum([x ** 2 for x in self.strengths]) - len(self.stresses) * self.avg_strength ** 2) / (
                        len(self.stresses) - 1))
        else:
            self.sd_strength = 0

    # get the tangent modulus
    def get_chord_modulus(self):

        self.modulus = list()  # allocate namespace for modulus
        #  Compute the modulus for each test
        for stress, strain in zip(self.stresses, self.strains):
            # find closest indexes to 0.001 and 0.002 in strains
            # As per table 3 in ASTM D3039
            i_1 = ASTMD_util.find_index(strain, 0.001)
            i_2 = ASTMD_util.find_index(strain, 0.002)

            # Eq. 8 in ASTM D3039 Section 13
            E_chord = (stress[i_2] - stress[i_1])/(strain[i_2] - strain[i_1])
            self.modulus.append(E_chord)

        if len(self.modulus) > 1:
            self.avg_modulus = sum(self.modulus) / len(self.modulus)
            self.sd_modulus = np.sqrt(
                (sum([x ** 2 for x in self.modulus]) - len(self.modulus) * self.avg_modulus ** 2) / (
                        len(self.modulus) - 1))
        else:
            self.avg_modulus = self.modulus[0]
            self.sd_modulus = 0

    # print the test results in a text file
    def print_results(self):
        path = self.filenames[0].split("/")
        name = "results_D3039.txt"
        if len(path) > 1:
            path = "/".join(path[:-1]) + "/" + name
        else:
            path = name

        result_file = open(path, "w")
        result_file.write("ASTM D3039 Standard Report" + "\n")
        result_file.write("\n")
        result_file.write("1. Testing parameters" + "\n")
        result_file.write("Material name : " + self.name + "\n")
        result_file.write("Width of samples : " + "mm, ".join(map(str, self.widths)) + "mm" + "\n")
        result_file.write("Thickness of samples : " + "mm, ".join(map(str, self.thicknesses)) + "mm" + "\n")
        result_file.write("Lengths of samples : " + "mm, ".join(map(str, self.lengths)) + "mm" + "\n")
        result_file.write("Extensometer length : " + str(self.extensiometer_length) + "mm" + "\n")
        result_file.write("\n")
        result_file.write("2. Test Results" + "\n")
        result_file.write("Chord tensile modulus : " + str(round(self.avg_modulus, 0)) + " MPa" + "\n")
        result_file.write("Standard Deviation : " + "(" + str(round(self.sd_modulus, 0)) + ")" + "\n")
        result_file.write("Tensile strength : " + str(round(self.avg_strength, 0)) + " MPa" + "\n")
        result_file.write("Standard Deviation : " + "(" + str(round(self.sd_strength, 0)) + ")" + "\n")

    # plot the stress strain curves with average
    def plot_stress_strain(self):
        # Plot the stress strain curve
        plt.figure("Tensile Stress_Strain")
        for stress, strain in zip(self.stresses, self.strains):
            plot1, = plt.plot(strain, stress, "#B2B2B2")
        plot1.set_label("Samples")
        plot1, = plt.plot(self.avg_strain, self.avg_stress, "r")
        plot1.set_label("Average")
        plt.legend()
        plt.title("Stress-Strain curve")
        plt.ylabel("Tensile stress (MPa)")
        plt.xlabel("Strain at the middle of the sample (mm/mm)")
        plt.grid(which='both')

    # plot the average modulus line on the stress strain graph
    def plot_modulus(self):
        plt.figure("Tensile Modulus")
        plot1, = plt.plot(self.avg_strain, self.avg_stress)
        plot1.set_label("SS Curve")
        plot1, = plt.plot(self.avg_strain[:self.avg_stress.index(max(self.avg_stress))],
                          [strain * self.avg_modulus for strain in self.avg_strain][
                          :self.avg_stress.index(max(self.avg_stress))], "r")
        plot1.set_label("Modulus")
        plt.legend()
        plt.title("Secant modulus and Stress Strain curve")
        plt.ylabel("Stress (MPa)")
        plt.xlabel("Strain (mm/mm)")
        plt.grid(which='both')

        # Plot all modulus values with stress strain curves for validation

    # plot all the modulus to verify results
    def plot_all_modulus(self):
        plt.figure("Tensile All")
        for module, stress, strain in zip(self.modulus, self.stresses[1:], self.strains[1:]):
            plot1, = plt.plot(strain, stress, "#B2B2B2")
            plot2, = plt.plot(strain[:stress.index(max(stress))],
                              [value * module for value in strain][:stress.index(max(stress))], "r")
        plot1.set_label("Tests")
        plot2.set_label("Modulus")


# Test Method for Lap Shear Adhesion for Fiber Reinforced Plastic (FRP) Bonding
class D5868(object):
    def __init__(self, filenames, areas, mtr_name=""):
        self.name = mtr_name  # Material name
        self.tests = list()  # individual tests for the samples
        self.areas = areas  # widths of the samples (list)
        self.stresses = list()  # allocate namespace for individual stresses
        self.filenames = filenames  # filenames of the test data
        self.get_test_data()  # Import the the test data
        self.get_stress()  # Compute stress and strains
        self.plot_stress()  # Plot the stress strain graph
        self.get_rupture()  # Compute the max stress (break)
        self.print_results()  # Print result values to text file

    # get the test data
    get_test_data = ASTMD_util.get_test_data

    # Compute stress and strain from Extensometer and load
    def get_stress(self):
        self.stresses = [[force/area for force in test["Load"].astype(float)] for test, area in zip(self.tests, self.areas)]
        self.times = [[time for time in test["Time"].astype(float)] for test in self.tests]
        self.trimmed_stresses = [stress[:stress.index(max(stress))] for stress in self.stresses]
        self.avg_times = ASTMD_util.avg(self.times)
        self.avg_stress = ASTMD_util.avg(self.stresses)

    # Get the stress at break
    def get_rupture(self):
        #  Max stress
        self.strengths = [max(stress) for stress in self.stresses]
        # Compute average strength
        self.avg_strength = sum(self.strengths) / len(self.stresses)
        # Compute Standard deviation from all samples
        if len(self.stresses) > 1:
            self.sd_strength = np.sqrt(
                (sum([x ** 2 for x in self.strengths]) - len(self.stresses) * self.avg_strength ** 2) / (
                        len(self.stresses) - 1))
        else:
            self.sd_strength = 0

    # print the test results in a text file
    def print_results(self):
        path = self.filenames[0].split("/")
        name = "results_D5868.txt"
        if len(path) > 1:
            path = "/".join(path[:-1]) + "/" + name
        else:
            path = name

        result_file = open(path, "w")
        result_file.write("ASTM D5868 Standard Report" + "\n")
        result_file.write("\n")
        result_file.write("1. Testing parameters" + "\n")
        result_file.write("Material name : " + self.name + "\n")
        result_file.write("Areas of bonded joints : " + " mm^2, ".join(map(str, self.areas)) + " mm^2" + "\n")
        result_file.write("\n")
        result_file.write("2. Test Results" + "\n")
        strengths = [round(strength, 3) for strength in self.strengths]
        result_file.write("Individual Shear strengths : " + "Mpa, ".join(map(str, strengths)) + " MPa" + "\n")
        result_file.write("Average Shear strength : " + str(round(self.avg_strength, 2)) + " MPa" + "\n")
        result_file.write("Standard Deviation : " + "(" + str(round(self.sd_strength, 2)) + ")" + "\n")

    # plot the stress strain curves with average
    def plot_stress(self):
        # Plot the stress strain curve
        plt.figure("Shear Stress Time")
        for time, stress in zip(self.times, self.trimmed_stresses):
            plt.plot(time[:len(stress)], stress, "#2f3030")
        plt.title("Stress-Time curves")
        plt.ylabel("Shear stress (MPa)")
        plt.xlabel("Time (s)")
        plt.grid(which='both')

