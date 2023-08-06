import argparse
import re
import sys
import pandas as pd
from openpyxl import Workbook

# Class object question
class Question:
    def __init__(self, statement, level, option_a, option_b, option_c, option_d,instruction , answer):
        self.statement = statement
        self.level = level
        self.option_a = option_a
        self.option_b = option_b
        self.option_c = option_c
        self.option_d = option_d
        self.instruction= instruction
        self.answer = answer

LEVEL_MAP = {
    'TH': '2_Thông hiểu',
    'VD': '3_Vận Dụng',
    'VDT': '3_Vận Dụng',
    'NB': '1_Nhận biết',
}

pattern = re.compile(r'Câu (\d+) \((.*?)\)\. (.*?)\n((?:[A-Z]\. .*?\n)+)Hướng dẫn: (.*?)\nChọn: ([A-Z])', re.DOTALL)

def convert_file_word_to_excel(input_file_path, output_file_path):
    if input_file_path == "":
        print('The file does not exist. Please check again')
        sys.exit(0)
    questions_qc=[]
    questions_final=[]
    question_len=0
    with open(input_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        questions = re.findall(pattern, content)
        question_len=len(questions)
        if len(questions)==0:
            print('The pattern is not invalid for any questions please check !')
            sys.exit(0)
        for question in questions:
            num = question[0]
            question_type = question[1]
            text = question[2].strip()
            options_text = question[3]
            options = re.findall(r'[A-Z]\. (.*?)\n', options_text)
            instruction = question[4].strip()
            chosen_option = question[5]
            option_a, option_b, option_c, option_d = options
            print(f"_Câu {num} ({question_type}): {text} passed ✅")
            questions_final.append(Question(statement=text,level=LEVEL_MAP.get(question_type, '4_Vận dụng cao'), option_a=option_a, option_b=option_b, option_c=option_c, option_d=option_d, instruction=instruction, answer=chosen_option.lower() ))
            questions_qc.append(Question(statement=f"Câu  {num} {text}", level=f" question_type ", option_a=f"A. {option_a} ", option_b=f" B. {option_b} ", option_c=f' C. {option_c}', option_d=f' D. {option_d} ', instruction=f'Hướng Dẫn: {instruction}', answer=f'Chọn: {chosen_option} ' ))

    # Convert data list to pandas data frame
    columns = ['statement', 'level', 'option_a',
               'option_b', 'option_c', 'option_d', 'answer', 'instruction']
    rows = []
    for question in questions_final:
        row = [question.statement, question.level, question.option_a,
               question.option_b, question.option_c, question.option_d, question.answer, question.instruction]
        rows.append(row)
    df_final = pd.DataFrame(rows, columns=columns)
    rows_for_qc = []
    for question in questions_qc:
        row = [question.statement, question.level, question.option_a,
               question.option_b, question.option_c, question.option_d, question.answer, question.instruction]
        rows_for_qc.append(row)
    df_qc = pd.DataFrame(rows_for_qc, columns=columns)
    # Create an Excel Workbook and add the DataFrame as a worksheet

    writer = pd.ExcelWriter('./output/output_data.xlsx' if output_file_path == "" else output_file_path, engine='openpyxl')
    # # Remove default sheet
    book  = writer.book
    df_final.to_excel(writer, index=False, header=False,
                      sheet_name='questions')
    df_qc.to_excel(writer, index=False, header=False,
                   sheet_name='question_for_qc')
    # # Save the Excel Workbook
    writer.close()

# Remove empty file input
# ==========================
def conver_txt_file(input_file_path, output_file_path):
    # Open the input file
    if input_file_path == "":
        sys.exit(0)
    with open(file=input_file_path, mode="r", encoding="utf-8") as input_file:
        # Read the contents of the file
        lines = input_file.readlines()
    # Remove empty lines from the list of lines
    lines = list(filter(lambda x: x.strip() != "", lines))

    # Open the output file and write the filtered lines to it
    with open(file='./output/output_data.txt' if output_file_path == "" else output_file_path, mode="w", encoding='utf-8') as output_file:
        output_file.writelines(lines)
