import torch
from torch import nn
from torchvision.models import resnet18,regnet_x_8gf


class TestConv2d(nn.Module):
    def __init__(self, in_channels, out_channels, **kwargs):
        super(TestConv2d, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, **kwargs)
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(True)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x


class TestModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = TestConv2d(3, 32, kernel_size=3)
        self.conv2 = TestConv2d(32, 64, kernel_size=3)
        self.dropout = nn.Dropout(0.3)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.dropout(x)
        return x


model= resnet18()
model2=regnet_x_8gf()