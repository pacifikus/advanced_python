from pathlib import Path
import os
from fib_ast import get_ast_image


def get_header(body):
    return \
        "\\documentclass{article}\n\\usepackage{graphicx}\n\\begin{document}\n" + body


def get_tail(body):
    return body + "\n\\end{document}"


def save_to_text(data, filename='result.tex'):
    with open(filename, mode='w') as f:
        f.write(data)


def generate_single_row(row_items):
    return '&'.join([str(item) for item in row_items]) + '\\\\'


def generate_table(data):
    table = f'\\begin{{center}}\\begin{{tabular}}{{{"c"*len(data)}}}\n'
    table += '\n'.join(list(map(generate_single_row, data)))
    table += f'\n\\end{{tabular}}\\end{{center}}\n'
    return table


def insert_image(filepath):
    img_filepath = Path(filepath)
    img_file = img_filepath.stem
    folder_path = str(img_filepath.resolve().parent)
    latex = f"\graphicspath{{{folder_path}}}\n\includegraphics[scale=0.35]{{{img_file}}}"
    return latex


task = 'medium'
input_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

if task == 'easy':
    table_result = get_header(get_tail(generate_table(input_data)))
    save_to_text(table_result, 'artifacts/easy_result.tex')
elif task == 'medium':
    ast_image_path = 'ast.png'
    get_ast_image(filepath=ast_image_path)
    doc_body = generate_table(input_data) + insert_image(ast_image_path)
    result = get_header(get_tail(doc_body))

    tex_filename = 'artifacts/medium_result.tex'
    save_to_text(result, tex_filename)
    os.system(
       f'C:/texlive/2023/bin/windows/pdflatex.exe -no-shell-escape '
       f'-interaction=nonstopmode -output-format=pdf '
       f'-output-directory=artifacts {tex_filename}'
    )

