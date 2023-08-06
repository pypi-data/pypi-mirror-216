import os
import numpy as np
from PIL import Image

current_dir = os.getcwd()

dataset_dir = current_dir + "\\medidata\\br35h\\"

X = []
y = []
image_size = [100, 100]  # Resim boyutlarını saklamak için yeni bir liste

no_dir = os.path.join(dataset_dir, "no")
yes_dir = os.path.join(dataset_dir, "yes")
data_dir = no_dir
for label in os.listdir(data_dir):
    label_dir = os.path.join(data_dir, label)

    if label.endswith(".jpg") or label.endswith(".png"):
        img = Image.open(label_dir)  # label_dir olarak değiştirildi
        img = img.resize(image_size)  # Resmi belirtilen boyuta yeniden boyutlandır
        img_array = np.array(img)
        X.append(img_array)
        print("Label", label)
        y.append(label)

# X, y ve image_sizes veri setlerini numpy dizilerine dönüştür
X = np.array(X)
y = np.array(y)
image_sizes = np.array(image_size)

# X ve y veri setlerini kullanarak istediğiniz şekilde devam edebilirsiniz
print(X.shape)
print(y.shape)
