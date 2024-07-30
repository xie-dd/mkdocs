# -*- coding: utf-8 -*-
# @Author    : xdd2026@qq.com
# @CreateData: 2024-05-23
# @Filename  : gen_md_by_src.py
# @Purpose   : 从代码的注释中获得文档
# @Help      : https://www.yuque.com/xdd1997/ek3kug/oown6is8ts58iyde?singleDoc# 密码：rzab

import os
import re
import shutil


# 获得一个文件夹下的所有文件
def get_src_file(src_path, language):
    src_files = []

    if language == "python":
        for root, dirs, files in os.walk(src_path):
            for file in files:
                if file.endswith('.py') or file.endswith('.PY'):
                    src_files.append(os.path.join(root, file))

    if language == "matlab":
        for root, dirs, files in os.walk(src_path):
            for file in files:
                if file.endswith('.m'):
                    src_files.append(os.path.join(root, file))

    return src_files


# 从 python 代码脚本中获得注释
def gen_md_from_python_src(file):
    md = {}

    with open(file, "r", encoding='utf-8') as f:
        lines = f.readlines()

    fun_line = []
    fun_name = []
    for index, ii in enumerate(lines):
        tmp = ii.strip()
        pattern = r'def\s+(\w+)\s*\(.*\):.*'
        resu = re.search(pattern, tmp)
        if resu is not None:
            fun_line.append(index)
            fun_name.append(re.search(pattern, tmp).group(1))

    for index, item in enumerate(fun_line):
        src_content = []
        content = lines[item+1:]
        for jj in content:
            tmp = jj.strip()
            # 识别注释的逻辑是: 找到函数所在的行, 再找到下面第一个非注释的行，之间的为函数注释
            if len(tmp) >= 1 and tmp[0].isalpha():  # isalpha 全是字母
                break
            elif tmp != '':
                src_content.append(tmp[1:].strip() + '\n')
        if not src_content == []:
            md[fun_name[index]] = src_content

    return md


# 从 matlab 代码脚本中获得注释
def gen_md_from_matlab_src(file):
    md = {}

    with open(file, "r", encoding='utf-8') as f:
        lines = f.readlines()

    # 存储处理后的内容
    processed_lines = []
    xuHangList = []

    for line in lines:
        tmp = line.strip()
        # 合并函数定义时的...续行
        if tmp.startswith('function') or xuHangList:
            if tmp.endswith('...'):
                xuHangList.append(tmp[:-3].strip())
            else:
                xuHangList.append(tmp)
                full_function = ' '.join(xuHangList).replace('\n', ' ')
                processed_lines.append(full_function)
                xuHangList = []
        else:
            processed_lines.append(line.strip())
    lines = processed_lines

    # 记录各个函数定义所在的行与函数名称
    fun_line = []
    fun_name = []
    for index, ii in enumerate(lines):
        tmp = ii.strip()

        # 定义匹配 MATLAB 函数名的正则表达式
        pattern1 = r'function\s+(\w+)\s*\(.*\)'
        pattern2 = r'function\s+\w+\s*=\s*(\w+)\s*\(.*\)'
        pattern3 = r'function\s*\[\w+(?:,\w+)*\]\s*=\s*(\w+)\s*\(.*\)'

        # 使用正则表达式进行匹配
        match1 = re.search(pattern1, tmp)
        match2 = re.search(pattern2, tmp)
        match3 = re.search(pattern3, tmp)

        # 如果匹配成功，返回函数名
        if match1:
            index_tmp = index
            name_tmp = match1.group(1)
        elif match2:
            index_tmp = index
            name_tmp = match2.group(1)
        elif match3:
            index_tmp = index
            name_tmp = match3.group(1)
        else:
            index_tmp = []

        if not index_tmp == []:
            fun_line.append(index_tmp)
            fun_name.append(name_tmp)

    # 记录各个函数的注释内容
    for index, item in enumerate(fun_line):
        src_content = []
        content = lines[item+1:]
        for jj in content:
            tmp = jj.strip()
            if len(tmp) >= 1 and tmp[0].isalpha():  # isalpha 全是字母
                break
            elif tmp != '':
                src_content.append(tmp[1:].strip() + '\n')

        # 处理注释最后一行是空白或者注释的情况
        if not src_content == []:
            while True:
                tmp = src_content[-1].strip()
                if tmp == '' or tmp[0] == '%':
                    src_content.pop()
                else:
                    break
            assert src_content[-1][0] != '%'
            assert len(src_content)>0

            md[fun_name[index]] = src_content

    return md



if __name__ == "__main__":
    current_dir = os.path.abspath(os.path.dirname(__file__))
    proj_dir = os.path.abspath(os.path.join(current_dir, ".."))
    src_path = os.path.join(proj_dir, "src")
    gen_md_path = os.path.join(current_dir, "docs", "API")

    # 删除原来的注释文档文件夹
    del_folder = 1
    if del_folder == 1:
        if os.path.exists(gen_md_path):
            shutil.rmtree(gen_md_path)

    if not os.path.exists(gen_md_path):
        os.makedirs(gen_md_path)

    # 获得脚本文件路径列表
    language = "matlab"
    src_files = get_src_file(src_path, language)
    print(src_files)

    
    for fil_ii in src_files:
        # 获得脚本文件的注释内容
        if language == "matlab":
            md_dict = gen_md_from_matlab_src(fil_ii)
        elif language == "python":
            md_dict = gen_md_from_python_src(fil_ii)
        else:
            pass

        # 将注释内容写入md文档
        filName = os.path.splitext(os.path.basename(fil_ii))[0]
        for fun_name, fun_md in md_dict.items():
            os.path.splitext(os.path.basename(fil_ii))
            fil_md_gen = os.path.join(gen_md_path, filName + '.' + fun_name) + '.md'
            with open(fil_md_gen, 'w', encoding='utf-8') as file:
                meta = f'---\ntitle: {filName}.{fun_name}\n---\n\n'
                file.writelines(meta)
                file.writelines(fun_md)
            print(f"gen doc: {fil_md_gen}")

