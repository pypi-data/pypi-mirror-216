from setuptools import setup, find_packages

setup(
    name='tissue-tag',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'bokeh',
        'matplotlib',
        'seaborn',
        'scipy',
        'skimage',
        'tqdm',
        'cellpose',
        'opencv-python'
    ],
    author=['Oren Amsalem', 'Nadav Yayon'],
    author_email='oren.a4@gmail.com, nadav.yayon@mail.huji.ac.il',
    description='TBD',
    url='https://github.com/nadavyayon/TissueTag',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)

