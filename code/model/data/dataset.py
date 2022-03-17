from torch.utils.data import Dataset
from torchvision.transforms import ToTensor
import cv2
import pandas as pd

import os


class ImageDataset(Dataset):
    def __init__(self, data_path):
        self.img_path = os.path.join(data_path, "img")
        self.images = os.listdir(self.img_path)

        #  Grab label data
        df = pd.read_csv(os.path.join(data_path, "zalando_articles_cleaned.csv"))
        self.labels = df.category_index.to_list()

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        # Read the image
        image = cv2.imread(os.path.join(self.img_path, self.images[idx]))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image = image.transpose(1, 2, 0)

        # Define a transform to convert the image to tensor
        transform = ToTensor()
        x = transform(image)

        y = self.labels[idx]

        return (x, y)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import torch

    train_data_path = r"C:\Users\derks\OneDrive\Bureaublad\Classifying Fashion Articles\code\data\data"
    train_dataset = ImageDataset(train_data_path)

    for x, y in train_dataset:

        # # Example of target with class indices
        # loss = torch.nn.CrossEntropyLoss()
        # input = torch.randn(3, 5, requires_grad=True)
        # target = torch.empty(3, dtype=torch.long).random_(5)
        # print(target)
        # output = loss(input, target)

        # # torch.nn.functional.one_hot(tensor, num_classes=-)

        x = x.numpy().transpose([1,2,0])
        plt.imshow(x)
        plt.title(y)
        plt.show()
