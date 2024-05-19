import torch
from torchvision import transforms
import torch.nn as nn
import torch.nn.functional as F

from PIL import ImageOps
from PIL import Image

import os

class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.conv3 = nn.Conv2d(16, 32, 3)
        self.fc1 = nn.Linear(32, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = torch.flatten(x, 1) # flatten all dimensions except batch
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class CustomTransform:
    def __init__(self, output_size):
        self.output_size = output_size

    def __call__(self, image):
        # Redimensionar la imagen
        resized_image = transforms.Resize(self.output_size)(image)
        # Convertir a blanco y negro y asegurarse de que tenga un solo canal
        bw_image = ImageOps.grayscale(resized_image).convert('L')
        inverted_img = Image.eval(bw_image, lambda x: 255 - x)
        # Convertir la imagen PIL en un tensor
        tensor_image = transforms.ToTensor()(bw_image)
        # Normalizar la imagen
        normalized_image = transforms.Normalize((0.5,), (0.5,))(tensor_image)
        return normalized_image

def resize_image(image):
    # Esta es la función de redimensionamiento que definimos anteriormente
    transform = transforms.Compose([
        transforms.Resize((28, 28)),
    ])
    # Redimensiona la imagen
    resized_image = transform(image)
    # Convierte la imagen a blanco y negro
    bw_image = ImageOps.grayscale(resized_image)
    return bw_image

classes = {0: 'Camiseta',
 1: 'Pantalon',
 2: 'Jersey',
 3: 'Vestido',
 4: 'Abrigo',
 5: 'Sandalia',
 6: 'Camisa',
 7: 'Tenis',
 8: 'Bolsa',
 9: 'Botas'}

PATH = os.path.dirname(__file__) + "/cifar_net_Bueno.pth"
transform = CustomTransform((28, 28))
Model_ = Model()
Model_.load_state_dict(torch.load(PATH))


def forward_image(image):
    image = resize_image(image)
    t_image = transform(image).reshape([1,1,28,28])
    pred = Model_(t_image)
    _, prediction = torch.max(pred, 1)

    return f"Prediccion {classes[prediction.item()]}"
