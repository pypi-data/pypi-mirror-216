#!/usr/bin/env python
# coding: utf-8

# In[1]:


import setuptools


# In[3]:

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CNUfof_utils",
    version = '1.0.3',
    author = "Dong Yun Kwak",
    author_email = '98ehddbs@naver.com',
    description = "Python package for Galaxy Group finding algorithm using Mutliprocessing package",
    long_description = long_description,
    long_description_content_type = "text",
    url="https://github.com/Dong-yunkwak/KDY.git",
    packages=['PFOF'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
    ],
)
