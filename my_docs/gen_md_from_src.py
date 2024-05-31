# -*- coding: utf-8 -*-
# @Author    : xdd2026@qq.com
# @CreateData: 2024-05-23
# @Filename  : gen_md_by_src.py
# @Purpose   : 从代码的注释中获得文档

import os
import re
import shutil


# 获得一个文件夹下的所有文件
def get_src_file(src_path,language):
    if language == "python":     
        src_files = []
        for root, dirs, files in os.walk(src_path):
            for file in files:
                if file.endswith('.py') or file.endswith('.PY'):
                    src_files.append(os.path.join(root, file))

    if language == "matlab":     
        src_files = []
        for root, dirs, files in os.walk(src_path):
            for file in files:
                if file.endswith('.m'):
                    src_files.append(os.path.join(root, file))

    return src_files


# 从 python 代码脚本中获得注释
def gen_md_from_python_src(file):
    md = {}

    with open(file,"r", encoding='utf-8') as f:
        lines = f.readlines()

    fun_line = []
    function_name = []
    for id, ii in enumerate(lines):
        tmp = ii.strip()
        pattern = r'def\s+(\w+)\s*\(.*'
        resu = re.search(pattern, tmp)
        if resu is not None:
            fun_line.append(id)
            function_name.append(re.search(pattern, tmp).group(1))
        
    
    for id, ii in enumerate(fun_line):
        src_content = []
        lines_content = lines[ii+1:]
        for jj in lines_content:
            tmp = jj.strip()
            # 识别注释的逻辑是: 找到函数所在的行, 再找到下面第一个非注释的行，之间的为函数注释
            # Python: def
            if len(tmp)>=1 and tmp[0].isalpha():  # isalpha 是字母或数字
                break
            else:
                src_content.append(tmp[1:].strip()+'\n')
        if not src_content == []:
            md[function_name[id]] = src_content

    return md


def gen_md_from_src(file):
    """ 这个方法适用于一个文档仅有一个函数 """

    ben_flag = 0
    md = []
    with open(file, "r", encoding='utf-8') as f:
        lines = f.readlines()

    for ii in lines:
        tmp = ii.strip()
        # 识别注释的逻辑是: 找到函数所在的行, 再找到下面第一个非注释的行，之间的为函数注释
        # Matlab: function
        # Fortran: function, subroutine
        flag_1 = len(tmp) >= 8 and tmp[0:8].lower() == "function"
        flag_2 = len(tmp) >= 8 and tmp[0:10].lower() == "subroutine"
        if flag_1 or flag_2:
            ben_flag = 1
            continue
        if ben_flag == 1 and len(tmp) >= 1 and tmp[0].isalpha():
            break
        if ben_flag == 1:
            md.append(tmp[1:].strip() + '\n')

    return md


if __name__ == "__main__":
    current_dir = os.path.abspath(os.path.dirname(__file__))
    proj_dir = os.path.abspath(os.path.join(current_dir, ".."))
    src_path = os.path.join(proj_dir, "src")
    gen_md_path = os.path.join(current_dir, "docs","API")

    # 删除原来的注释文档文件夹
    del_folder = 1
    if del_folder == 1:
        if os.path.exists(gen_md_path):
            shutil.rmtree(gen_md_path)

    if not os.path.exists(gen_md_path):
        os.makedirs(gen_md_path)
 
    # 获得脚本地址
    language = "python"
    src_files = get_src_file(src_path, language)
    print(src_files)

    for fil_ii in src_files:
        if language == "python":
            md = gen_md_from_python_src(fil_ii)
            name_1 = os.path.splitext(os.path.basename(fil_ii))[0]
            for key, value in md.items():
                os.path.splitext(os.path.basename(fil_ii))
                fil_md_gen = os.path.join(gen_md_path, name_1 + '.' + key) + '.md'
                with open(fil_md_gen, 'w', encoding='utf-8') as file:
                    file.writelines(value)
                print(f"gen doc: {fil_md_gen}")

        elif language == "matlab":
            md = gen_md_from_src(fil_ii)
            fil_md_gen = os.path.join(gen_md_path, os.path.basename(fil_ii))
            fil_md_gen = os.path.splitext(fil_md_gen)[0] + '.md'
            with open(fil_md_gen, 'w', encoding='utf-8') as file:
                file.writelines(md)
            print(f"gen doc: {fil_md_gen}")
        else:
            pass



