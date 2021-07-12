# coding:utf-8
# Created by Equator at 2021/7/11
import os
import re
import sys


def build_path(base_path, file_name_set={'index.md'}):
    """
    递归获取文件路径，获取符合指定规则的文件路径
    :param file_name_set:
    :param base_path:
    :return:
    """
    file_path_list = []
    paths = os.listdir(base_path)
    for path in paths:
        full_path = os.path.join(base_path, path)
        if not os.path.exists(full_path):
            continue
        if os.path.isfile(full_path):
            if path in file_name_set:
                file_path_list.append(full_path)
                # print(f"文件：{full_path} 满足筛选条件")
        else:
            children_file_name_list = build_path(full_path, file_name_set)
            if children_file_name_list is not None:
                file_path_list.extend(children_file_name_list)
    return file_path_list


def normalize_path(path):
    return re.sub(r'/|\|\\', re.escape(os.sep), path)


def test_normalize_path():
    print(normalize_path('X:\\libinkai.github.io\\pages\\justdoit\\陪你读书\\index.md'))
    print(normalize_path('X:\libinkai.github.io\pages\justdoit\陪你读书\index.md'))
    print(normalize_path('X:/libinkai.github.io/pages/justdoit/陪你读书/index.md'))


def build_markdown_path(raw_path):
    return re.sub(re.escape(os.sep), '/', raw_path)


def test_build_markdown_path():
    print(build_markdown_path('X:\libinkai.github.io\pages\justdoit\陪你读书\index.md'))


def build_markdown_statement(file_path_list):
    """
    构建符合Markdown语法的目录片段，提取最后一个目录名作为展示名
    :param file_path_list:
    :return:
    """
    result_list = []
    for path in file_path_list:
        if path.count(os.sep) >= 2:
            result_list.append(f"- [{extract_name(path)}]({build_markdown_path(path)})")
        else:
            result_list.append(f"- [{path}]({build_markdown_path(path)})")
    return result_list


def extract_name(file_name):
    end = file_name.rindex(os.sep)
    start = file_name.rindex(os.sep, None, end) + 1
    return file_name[start: end]


def test_build_path():
    build_path('X:\libinkai.github.io\pages\justdoit\陪你读书')
    build_path('.', {'index.md', 'haha.md'})


def test_str():
    file_name = 'X:\libinkai.github.io\pages\justdoit\陪你读书\index.md'
    end = file_name.rindex(os.sep)
    start = file_name.rindex(os.sep, None, end) + 1
    print(start, end)
    print(file_name[start: end])


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # 默认参数
        base_path = '.'
    else:
        base_path = normalize_path(sys.argv[1])
    paths = build_path(base_path)
    statement = build_markdown_statement(paths)
    for s in statement:
        print(s)
