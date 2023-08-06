from setuptools import setup, find_packages

setup(
    name='medidata',
    version='0.2.0',
    description='A Python library for working with various medical image datasets.',
    author='Alperen T.',
    author_email='your_email@example.com',
    readme = "README.md",
    url='https://github.com/erenalpt/medidata',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.23.4',
        'opencv-python>=3.4.4',
        'tqdm>=4.65.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
