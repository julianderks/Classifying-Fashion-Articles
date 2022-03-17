import torch.nn as nn
import torch.nn.functional as F


class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()

        self.conv1 = nn.Conv2d(3, 12, kernel_size=3, stride=1)
        self.conv2 = nn.Conv2d(12, 24, kernel_size=3, stride=1)

        self.conv3 = nn.Conv2d(24, 48, kernel_size=3, stride=1)
        self.conv4 = nn.Conv2d(48, 96, kernel_size=3, stride=1)

        self.fc1 = nn.Linear(3456, 128)
        self.fc2 = nn.Linear(128, num_classes)

        self.dropout = nn.Dropout(p=0.5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.max_pool2d(x, kernel_size=4, stride=4)

        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = F.max_pool2d(x, kernel_size=4, stride=4)

        x = x.view(-1, 3456)
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)

        return x


if __name__ == "__main__":
    model = SimpleCNN(num_classes=10)
    print(model)
