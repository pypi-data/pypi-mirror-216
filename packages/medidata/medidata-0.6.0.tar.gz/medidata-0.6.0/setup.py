from setuptools import setup, find_packages

setup(
    name='medidata',
    version='0.6.0',
    description='A Python library for working with medical image datasets.',
    author='Alperen T.',
    author_email='alperent@mail.com',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/erenalpt/medidata',
    packages=find_packages(),
    install_requires=[
        'tqdm>=4.65.0',
        'numpy>=1.23.4',
        'scikit-learn>=1.2.2',
        'opencv-python>=3.4.4'
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
    package_dir={"medidata": "medidata"},
    package_data={
        "medidata": ["br35h/*.jpg", "br35h/no/*.jpg", "br35h/yes/*.jpg"]
    },
    include_package_data = True,
)
