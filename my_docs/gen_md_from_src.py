# -*- coding: utf-8 -*-
# @Author    : xdd2026@qq.com
# @CreateData: 2024-05-23
# @Filename  : gen_md_by_src.py
# @Purpose   : 从代码的注释中获得文档

import os
import shutil


current_dir = os.path.abspath(os.path.dirname(__file__))
proj_dir = os.path.abspath(os.path.join(current_dir, ".."))
src_path = os.path.join(proj_dir, "src")
gen_md_path = os.path.join(current_dir, "docs","API")

# print(current_dir)
# print(proj_dir)
# print(src_path)
# print(gen_md_path)


# 删除原来的注释文档
if os.path.exists(gen_md_path):
    shutil.rmtree(gen_md_path)
os.makedirs(gen_md_path)


# 获得一个文件夹下的所有文件
src_files = []
for root, dirs, files in os.walk(src_path):
    for file in files:
        if file.endswith('.m') or file.endswith('.py'):
            src_files.append(os.path.join(root, file))


# 从代码脚本中获得注释
def gen_md_from_src(file):
    ben_flag = 0
    md = []
    with open(file,"r", encoding='utf-8') as f:
        lines = f.readlines()
    
    for ii in lines:
        tmp = ii.strip()
        # 识别注释的逻辑是: 找到函数所在的行, 再找到下面第一个非注释的行，之间的为函数注释
        # Python: def
        # Matlab: function
        # Fortran: function, subroutine
        flag_1 = len(tmp)>=8 and tmp[0:8].lower()=="function"
        flag_2 = len(tmp)>=8 and tmp[0:3].lower()=="def"
        flag_3 = len(tmp)>=8 and tmp[0:10].lower()=="subroutine"
        if flag_1 or flag_2 or flag_3:
            ben_flag = 1
            continue
        if ben_flag==1 and len(tmp)>=1 and tmp[0].isalpha():
            break
        if ben_flag==1:
            md.append(tmp[1:].strip()+'\n')

    return md


# 从代码脚本中获得注释
print(src_files)
for fil_ii in src_files:
    md_content = gen_md_from_src(fil_ii)

    fil_md_gen = os.path.join(gen_md_path,os.path.basename(fil_ii))
    fil_md_gen = os.path.splitext(fil_md_gen)[0]+'.md'
    with open(fil_md_gen, 'w', encoding='utf-8') as file:
        file.writelines(md_content)
    print(f"gen doc: {fil_md_gen}")

