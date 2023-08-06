from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    description = fh.read()

setup(
    name='opensense',
    version='0.0.1',
    author='Jianfei',
    author_email='yang0478@e.ntu.edu.sg',
    description='A python library for wireless sensing',
    long_description = description,
    long_description_content_type="text/markdown",

    url="https://github.com/xyanchen/WiFi-CSI-Sensing-Benchmark",

    packages=['opensense'],
    install_requires=[
        'torch',
        'numpy',
        'scipy',
        'tsmoothie',
    ],
    python_requires='>=3.6',
)