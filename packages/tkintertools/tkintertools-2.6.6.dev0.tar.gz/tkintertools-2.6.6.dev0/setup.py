""" 上传 PyPi """

import setuptools

setuptools.setup(
    name='tkintertools',
    version='2.6.6.dev',
    description='An auxiliary module of the tkinter module.',
    long_description=open('README.md', encoding='utf-8').read(),
    author='Xiaokang2022',
    author_email='2951256653@qq.com',
    maintainer='Xiaokang2022',
    maintainer_email='2951256653@qq.com',
    url='https://github.com/Xiaokang2022/tkintertools',
    packages=setuptools.find_packages(),
    license='MulanPSL-2.0',
    keywords=['tkinter', 'tkintertools', 'GUI'],
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)',
        'Operating System :: OS Independent',
    ],
)

# python -m pip install --user --upgrade setuptools wheel [检查更新]

# python setup.py sdist bdist_wheel [打包]
# python -m twine upload dist/* [上传]

# pip install -U pypistats [数据分析]
# pip install socksio [数据分析]

# pypistats overall tkintertools [数据分析]
# pypistats recent tkintertools
# pypistats system tkintertools
# pypistats python_minor tkintertools
# pypistats python_major tkintertools

# https://pypistats.org/packages/tkintertools [数据分析]
