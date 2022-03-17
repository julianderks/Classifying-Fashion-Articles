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

        # Read the label
        y = self.labels[idx]

        # Convert the image to tensor
        transform = ToTensor()
        x = transform(image)

        return (x, y)


