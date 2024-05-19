import torch
from torchvision import transforms
import torch.nn as nn
import torch.nn.functional as F

from PIL import ImageOps
from PIL import ImageOps

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

classes = {0: 'T-Shirt. The different ways in which you can reycle it are:\n- Cut it into cleaning rags.\n- Use it as fabric for DIY projects like quilting or pillow stuffing.\n- Donate it to clothing recycling programs or thrift stores.',
 1: 'Pants. The different ways in which you can reycle them are:\n- Cut them into shorts or capris.\n- Use the fabric for patchwork projects.\n- Donate them to textile recycling centers or thrift stores.',
 2: 'Jersey. The different ways in which you can reycle it are:\n- Turn it into throw pillows or cushion covers.\n- Use it for DIY tote bags or grocery bags.\n- Donate it to charity organizations or thrift stores.',
 3: 'Dress. The different ways in which you can reycle it are:\n- Repurpose it into skirts or tops.\n- Use the fabric for craft projects like hair accessories or pouches.\n- Donate it to clothing recycling programs or thrift stores.',
 4: 'Coat. The different ways in which you can reycle it are:\n- Donate it to homeless shelters or charitable organizations.\n- Repurpose the fabric into smaller items like scarves or hats.\n- Donate it to clothing recycling programs or thrift stores.',
 5: "Sandals. The different ways in which you can reycle them are:\n- If they're still wearable, donate them to shoe recycling programs or thrift stores.\n- If they're no longer wearable, check if the materials are recyclable in your area.",
 6: 'Shirt. The different ways in which you can reycle it are:\n- Cut it it cleaning cloths or handkerchiefs.\n- Use it for DIY projects like quilting or patchwork.\n- Donate it to textile recycling centers or thrift stores.',
 7: 'Sneakers. The different ways in which you can reycle them are:\n- Donate them to shoe recycling programs or thrift stores.\n- Some shoe brands offer recycling programs for old sneakers.',
 8: 'Bag. The different ways in which you can reycle it are:\n- Repurpose it as storage bags for shoes or accessories.\n- Donate it to charity shops or textile recycling programs.\n- Use it for organizing items in your home or when traveling.',
 9: 'Boots. The different ways in which you can reycle them are:\n- Repair and reuse them if possible.\n- Donate them to shoe repair shops or charity organizations.\n- Check if the materials are recyclable in your area.'}

PATH = os.path.dirname(__file__) + "/cifar_net_Bueno.pth"
transform = CustomTransform((28, 28))
Model_ = Model()
Model_.load_state_dict(torch.load(PATH))


def forward_image(image):
    image = resize_image(image)
    t_image = transform(image).reshape([1,1,28,28])
    pred = Model_(t_image)
    _, prediction = torch.max(pred, 1)

    answer = f"Detected: {classes[prediction.item()]}\n"
    
    return answer
