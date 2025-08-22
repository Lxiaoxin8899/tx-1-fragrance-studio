#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flavor Lab Pro 安装脚本
"""

from setuptools import setup, find_packages
import os

# 读取README文件
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# 读取requirements.txt
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="flavor-lab-pro",
    version="2.0.0",
    description="专业电子烟雾化物配方设计工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Lxiaoxin8899",
    author_email="",
    url="https://github.com/Lxiaoxin8899/tx-1-fragrance-studio",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: User Interfaces",
    ],
    python_requires=">=3.8",
    entry_points={
        "gui_scripts": [
            "flavor-lab-pro=main:main",
        ],
    },
    keywords="electronic-cigarette, flavor, recipe, design, pyqt",
    project_urls={
        "Bug Reports": "https://github.com/Lxiaoxin8899/tx-1-fragrance-studio/issues",
        "Source": "https://github.com/Lxiaoxin8899/tx-1-fragrance-studio",
    },
)