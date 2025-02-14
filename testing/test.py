from parse_clean import remove_unwanted_newlines, process_file, remove_punctuation, rm_stop_words, remove_single_letters
from concat_state_abs import concat_state_abs_func
import unittest

class TestWholeCleaning(unittest.TestCase):

    def test1(self):
        
        with open("/home/frankwoods/Desktop/lab/test_parse/test1.csv", "r") as test_file:
            test_lines = test_file.readlines()

        new_line_removed = remove_unwanted_newlines(test_lines)

        cleaned_lines = []

        for line in new_line_removed:
            # for csv first line case
            if line == new_line_removed[0]:
                cleaned_lines.append(line)
                continue

            line = process_file(line)
            if line == 0: continue # continue to next line
            line = " ".join(line.split())
            line = line.lower()
            line = remove_punctuation(line)
            line = remove_single_letters(line)
            line = rm_stop_words(line)
            cleaned_lines.append(line + '\n')


        with open("/home/frankwoods/Desktop/lab/test_parse/test1_key.csv", "r") as test_key_file:
            test_key = test_key_file.readlines()
        self.assertEqual(cleaned_lines, test_key)
        
    def test2(self):
        
        with open("/home/frankwoods/Desktop/lab/test_parse/test2.csv", "r") as test_file:
            test_lines = test_file.readlines()

        new_line_removed = remove_unwanted_newlines(test_lines)

        cleaned_lines = []

        for line in new_line_removed:
            # for csv first line case
            if line == new_line_removed[0]:
                cleaned_lines.append(line)
                continue

            line = process_file(line)
            if line == 0: continue # continue to next line
            line = " ".join(line.split())
            line = line.lower()
            line = remove_punctuation(line)
            line = remove_single_letters(line)
            line = rm_stop_words(line)
            cleaned_lines.append(line + '\n')


        with open("/home/frankwoods/Desktop/lab/test_parse/test2_key.csv", "r") as test_key_file:
            test_key = test_key_file.readlines()
        
        self.assertEqual(cleaned_lines, test_key)

class TestConcat(unittest.TestCase):
    
    def test1(self):
        input = "/home/frankwoods/Desktop/lab/test_concat/test_concat1.csv"
        output = "/home/frankwoods/Desktop/lab/test_concat/test_concat1_out.csv"
        concat_state_abs_func(input, output)

    def test2(self):
        input = "/home/frankwoods/Desktop/lab/test_concat/test_concat2.csv"
        output = "/home/frankwoods/Desktop/lab/test_concat/test_concat2_out.csv"
        concat_state_abs_func(input, output)


class TestRmSingleChar(unittest.TestCase):

    def test1(self):
        line = "2024,or,here i will give test single a d e here"
        cleaned_line = remove_single_letters(line)
        self.assertEqual(cleaned_line, "2024,or,here will give test single here")

    def test2(self):
        line = "2023,wa,i start with a word end o"
        cleaned_line = remove_single_letters(line)
        self.assertEqual(cleaned_line, "2023,wa,start with word end")

class TestLemmatizer(unittest.TestCase):

    def test1(self):
        line = "2024,or,here i will give test single a d e here"

if __name__ == "__main__":
    unittest.main()