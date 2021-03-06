from torch.nn import ConvTranspose2d
from torch.nn import BatchNorm2d
from torch.nn import Conv2d
from torch.nn import Linear
from torch.nn import LeakyReLU
from torch.nn import ReLU
from torch.nn import Tanh
from torch.nn import Sigmoid
from torch import flatten
from torch import nn

class Generator(nn.Module):
    
    def __init__(self, input_dims=100, output_dims=512, output_channels=1):
        super(Generator, self).__init__()
        
        self.ct1 = ConvTranspose2d(in_channels=input_dims, out_channels=128, kernel_size=4, stride=2, padding=0, bias=False)
        self.relu1 = ReLU()
        self.batch1 = BatchNorm2d(128)
        
        self.ct2 = ConvTranspose2d(in_channels=128, out_channels=64, kernel_size=3, stride=2, padding=1, bias=False)
        self.relu2 = ReLU()
        self.batch2 = BatchNorm2d(64)
        
        self.ct3 = ConvTranspose2d(in_channels=64, out_channels=32, kernel_size=4, stride=2, padding=1, bias=False)
        self.relu3 = ReLU()
        self.batch3 = BatchNorm2d(32)
        
        self.ct4 = ConvTranspose2d(in_channels=32, out_channels=output_channels, kernel_size=4, stride=2, padding=1, bias=False)
        self.tanh = Tanh()
        
    def forward(self, x):
        x = self.ct1(x)
        x = self.relu1(x)
        x = self.batch1(x)
        
        x = self.ct2(x)
        x = self.relu2(x)
        x = self.batch2(x)
        
        x = self.ct3(x)
        x = self.relu3(x)
        x = self.batch3(x)
        
        x = self.ct4(x)
        output = self.tanh(x)
        
        return output
    
class Discriminator(nn.Module):
    
    def __init__(self, depth, alpha=0.2):
        super(Discriminator, self).__init__()
        
        self.conv1 = Conv2d(in_channels=depth, out_channels=32, kernel_size=4, stride=2, padding=1)
        self.leaky1 = LeakyReLU(alpha, inplace=True)
        
        self.conv2 = Conv2d(in_channels=32, out_channels=64, kernel_size=4, stride=2, padding=1)
        self.leaky2 = LeakyReLU(alpha, inplace=True)
        
        self.fc1 = Linear(in_features=3136, out_features=512)
        self.leaky3 = LeakyReLU(alpha, inplace=True)
        
        self.fc2 = Linear(in_features=512, out_features=1)
        self.sigmoid = Sigmoid()
        
    def forward(self, x):
        x = self.conv1(x)
        x = self.leaky1(x)
        
        x = self.conv2(x)
        x = self.leaky2(x)
        
        x = flatten(x, 1)
        x = self.fc1(x)
        x = self.leaky3(x)
        
        x = self.fc2(x)
        output = self.sigmoid(x)
        
        return output
