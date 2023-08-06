from setuptools import setup
def readme():
    with open('README.md','r') as f:
        return f.read()
setup(
    name='PythonHuff',
    version='1.0.4',
    packages=['pyhuff'],
    description='Huffman compression and decompression (Pure Python implementation)',
    long_description=readme(),
    long_description_content_type='text/markdown',
    keywords=['huffman','compression','decompression','algorithm'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
    ],entry_points={
        'console_scripts':[
            'pyhuff=pyhuff:_script'
        ]
    }
)