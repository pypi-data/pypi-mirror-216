# Medidata - Medical Image Dataset

MediData is a Python library that provides access to medical image datasets. It aims to simplify the process of loading and working with medical image data in various machine learning and data analysis projects.

## Features

Load and preprocess medical image datasets.
Resize images to the desired dimensions.
Access images and corresponding labels as numpy arrays.
Support for various medical imaging formats.
Easily integrate with machine learning workflows.

## Installation

You can install MediData using pip:
```
pip install medidata
```

## Usage

To use the Medidata dataset, you can install the Medidata library and import it into your Python project. You can then access the dataset using the provided functions and utilities. Here's an example of how to load the dataset:

To use MediData, follow these steps:
1) Import the medidata module:
```
import medidata
```

2) Load the BR35H dataset using the load_br35h function:
```
X, y, labels = medidata.load_br35h()
```
This function loads the BR35H dataset from the default directory path and returns the resized images and corresponding labels as numpy arrays.

3) You can now use the X, y, and labels variables in your data analysis or machine learning workflows.

## Example

Here's an example of how to use MediData to load and process the BR35H dataset:
```
import medidata

X, y, labels = medidata.load_br35h()

# Perform further operations on the loaded dataset
# ...
```

## Contributing
We welcome contributions to the Medidata library, including the addition of new medical image datasets. If you have other medical image datasets that you would like to include in Medidata, please reach out to us or submit a pull request.

Together, let's build a comprehensive and valuable resource for medical image analysis.

## Citation
If you use the Medidata dataset in your research or projects, we kindly request that you cite the original source of the dataset. The dataset can be found at:

[Br35H Dataset on Kaggle](https://www.kaggle.com/datasets/ahmedhamada0/brain-tumor-detection)

Please refer to the original dataset and follow any additional citation guidelines provided by the dataset creators.


## Contact
For any questions or inquiries regarding the Medidata dataset, please contact [alperent@mail.com](mailto:alperent@mail.com).

## References
[1] Ahmed Hamada. (2023). Br35H: Brain Tumor Detection Dataset. Kaggle Datasets. Retrieved from https://www.kaggle.com/datasets/ahmedhamada0/brain-tumor-detection