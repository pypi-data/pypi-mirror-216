import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='intercode-bench',
    author='John Yang',
    author_email='byjohnyang@gmail.com',
    description='The official InterCode benchmark package - a framework for interactive code tasks',
    keywords='nlp, benchmark, interaction, code, rl, decision making',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/intercode-benchmark/intercode-benchmark',
    project_urls={
        'Documentation': 'https://github.com/intercode-benchmark/intercode-benchmark',
        'Bug Reports': 'https://github.com/intercode-benchmark/intercode-benchmark/issues',
        'Source Code': 'https://github.com/intercode-benchmark/intercode-benchmark',
        'Website': 'https://intercode-benchmark.github.io/',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'gymnasium',
        'mysql-connector-python',
        'scikit-learn>=1.2.2',
        'pandas',
        'rich',
        'docker'
    ],
)