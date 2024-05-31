---
title: mkdocs生成文档
categories: [未分类]
tags: [mkdocs, 文档]
date: 2024-05-25
updated: 2024-05-25
cover : https://mypic2016.oss-cn-beijing.aliyuncs.com/picGo/202311031815445.png
---
## 项目预览
```
test_mkdocs
│  
├─my_docs
│  │  gen_md_from_src.py
│  │  mkdocs.yml
│  │  readme.md
│  │  
│  └─docs
│      │  index.md
│      │  帮助文档.md
│      │  
│      └─API
│              fun_1.md
│              fun_2.md
│              
└─src
        fun_1.m
        fun_2.py
```

## 安装与生成文档
#### 安装与配置 mkdocs
```
pip install mkdocs
pip install mkdocs-material
cd test_mkdocs
mkdocs new my_docs
```
#### 由代码脚本的注释生成文档
```
cd my_docs
python gen_md_from_src.py
```
#### 启动本地服务器
```
mkdocs serve
浏览器打开：127.0.0.1:8000
```
## 中文搜索
修改文件 mkdocs.yml，添加plugins-search部分
```
site_name: Xdd的帮助系统
theme:
  name: material
  palette:
    primary: 'green'
plugins:
    - search:
        lang:
            - en
            - ja
        separator: '[\s\-\.]+'
```


## 部署到 github page
注意：和docsify一样，不用部署到 ***.github.io 仓库

1. 把程序上传到Github任意仓库
2. 在本地项目执行下面代码，会生成一个site文件夹
```matlab
mkdocs build
mkdocs gh-deploy --clean
```

3. 登录github--->找到对应仓库--->Settings--->Pages--->Source:Deploy from a branch--->Branch:gh-pages, root--->Save
4. 访问 usename.github.io/repo_name 即可。如 [xie-dd.github.io/mkdocs](http://xie-dd.github.io/mkdocs)

备注：如果在网页端不能使用中文搜索，可参照 [https://www.cnblogs.com/chinjinyu/p/17610438.html](https://www.cnblogs.com/chinjinyu/p/17610438.html)



