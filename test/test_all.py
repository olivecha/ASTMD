import unittest
import ASTMD
import os


class MyTestCase(unittest.TestCase):

    def test_D790(self):
        sample_files = [f'test_data_D790/sample{i}.txt' for i in range(1, 7)]
        sample_widths = [10, 10.1, 9.9, 10, 10.1, 9.9]  # mm
        sample_depths = [1.05, 1.03, 0.97, 0.98, 1.02, 0.99]  # mm
        span_used = 100  # mm
        report = ASTMD.D790(sample_files, sample_widths, sample_depths, span_used, mtr_name="carbon")
        self.assertIsInstance(report, ASTMD.D790)
        self.assertTrue('ASTM_D790_test_report.docx' in os.listdir())
        os.remove(report.report_file)

    def test_D3039(self):
        sample_files = [f'test_data_D3039/sample{i}.txt' for i in range(1, 4)]
        sample_widths = [15.05, 14.95, 14.97, 15.02]
        sample_thicknesses = [1.01, 1.02, 0.99, 0.98]
        sample_lengths = [250.5, 249.5, 250.3, 249.8]
        report = ASTMD.D3039(sample_files, sample_widths, sample_thicknesses, sample_lengths,
                             mtr_name='Flax', extensiometer_length=50.8)
        self.assertIsInstance(report, ASTMD.D3039)
        self.assertTrue('ASTM_D3039_test_report.docx' in os.listdir())
        os.remove(report.report_file)

    def test_D5868(self):
        filenames = [f'test_data_D5868/sample{i}.txt' for i in range(1, 3)]
        areas = [25.3 * 25.4, 25.4 * 25.5]
        report = ASTMD.D5868(filenames, areas, mtr_name='flax and wood glue')
        self.assertIsInstance(report, ASTMD.D5868)
        self.assertTrue('ASTM_D5868_test_report.docx' in os.listdir())
        os.remove(report.report_file)

if __name__ == '__main__':
    unittest.main()
