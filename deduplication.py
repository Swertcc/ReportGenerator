import os
import re

def delete_duplicate_files_in_pdfs():
    target_directory = os.path.join(os.getcwd(), 'pdfs')

    if not os.path.exists(target_directory):
        print(f"目录未创建")
        return

    files = os.listdir(target_directory)

    file_info = {}
    pattern = re.compile(r'题号(\d{4}).*判题编号_(\d{7})')

    for filename in files:
        match = pattern.search(filename)
        if match:
            question_number = match.group(1)
            judge_number = int(match.group(2))

            if question_number not in file_info:
                file_info[question_number] = []

            file_info[question_number].append((judge_number, filename))

    files_to_delete = []

    for question_number, info in file_info.items():
        if len(info) > 1:
            info.sort()  # 按judge_number排序
            files_to_delete.extend([filename for _, filename in info[1:]])

    for filename in files_to_delete:
        file_path = os.path.join(target_directory, filename)
        os.remove(file_path)
        print(f"已删:{filename}")


delete_duplicate_files_in_pdfs()
