import unittest
import os
from main import convert_txt_file

class TestConvertTxtFile(unittest.TestCase):
    def test_convert_txt_file(self):
        # Test case with valid input file and output file paths
        input_file_path = 'input_file.txt'
        output_file_path = 'output_file.txt'
        convert_txt_file(input_file_path, output_file_path)
        self.assertTrue(os.path.exists(output_file_path))
        
        # Test case with empty input file path
        input_file_path = ''
        output_file_path = 'output_file.txt'
        with self.assertRaises(SystemExit) as cm:
            convert_txt_file(input_file_path, output_file_path)
        self.assertEqual(cm.exception.code, 0)
        
        # Add more test cases as needed
        
        # Clean up created files
        if os.path.exists(output_file_path):
            os.remove(output_file_path)

if __name__ == '__main__':
    unittest.main()
