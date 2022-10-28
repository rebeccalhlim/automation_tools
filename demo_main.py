
import demo_1

import argparse

long_path = r'C:\Stuff\AML\codes\coding_projects\test123\automation_tools\files' + '\\'

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', help='name', 
                    type=str, default='')
parser.add_argument('-f', '--file', help='file', 
                    type=str, default='')
args = vars(parser.parse_args())

filename = args['file']
file_list = [long_path + filename]
file_name = args['name']

demo_1.generate(file_name, file_list)