import torch
import torch.nn as nn
import torchvision.models as models

class DoubleConv(nn.Module):
    """Двойная свёртка: Conv → BN → ReLU ×2"""
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )
    def forward(self, x):
        return self.conv(x)


class UNetPretrained(nn.Module):
    """U-Net с предобученным ResNet34 в качестве encoder'а"""
    def __init__(self, n_classes=2, freeze_encoder=False):
        super().__init__()
        
        # Загружаем предобученный ResNet34
        resnet = models.resnet34(weights=models.ResNet34_Weights.DEFAULT)
        
        # ===== Encoder (из ResNet34) — 5 уровней даунсемплинга =====
        self.enc1 = nn.Sequential(resnet.conv1, resnet.bn1, resnet.relu)  # /2, 64 канала
        self.pool1 = resnet.maxpool                                        # /4
        self.enc2 = resnet.layer1                                          # /4, 64 канала
        self.enc3 = resnet.layer2                                          # /8, 128 каналов
        self.enc4 = resnet.layer3                                          # /16, 256 каналов
        self.enc5 = resnet.layer4                                          # /32, 512 каналов (бывший bottleneck)
        
        # ===== Decoder — 5 уровней апсемплинга (было 4!) =====
        self.up5 = nn.ConvTranspose2d(512, 256, 2, stride=2)               # 512 → 256
        self.dec5 = DoubleConv(256 + 256, 256)  # skip: e5(256) + up(bottleneck)
        
        self.up4 = nn.ConvTranspose2d(256, 128, 2, stride=2)               # 256 → 128
        self.dec4 = DoubleConv(128 + 128, 128)  # skip: e4(128) + up
        
        self.up3 = nn.ConvTranspose2d(128, 64, 2, stride=2)                # 128 → 64
        self.dec3 = DoubleConv(64 + 64, 64)     # skip: e3(64) + up
        
        self.up2 = nn.ConvTranspose2d(64, 64, 2, stride=2)                 # 64 → 64
        self.dec2 = DoubleConv(64 + 64, 64)     # skip: e2(64) + up
        
        self.up1 = nn.ConvTranspose2d(64, 64, 2, stride=2)                 # 64 → 64
        self.dec1 = DoubleConv(64 + 64, 64)     # skip: e1(64) + up
        
        # ===== Output =====
        self.out_conv = nn.Conv2d(64, n_classes, 1)
        
        # Заморозка encoder'а при необходимости
        if freeze_encoder:
            for param in list(self.enc1.parameters()) + \
                         list(self.enc2.parameters()) + \
                         list(self.enc3.parameters()) + \
                         list(self.enc4.parameters()) + \
                         list(self.enc5.parameters()):
                param.requires_grad = False
    
    def forward(self, x):
        # ===== Encoder =====
        e1 = self.enc1(x)           # [B, 64, H/2, W/2]
        e2 = self.enc2(self.pool1(e1))  # [B, 64, H/4, W/4]
        e3 = self.enc3(e2)          # [B, 128, H/8, W/8]
        e4 = self.enc4(e3)          # [B, 256, H/16, W/16]
        e5 = self.enc5(e4)          # [B, 512, H/32, W/32]
        
        # ===== Decoder с 5 skip-connections =====
        d5 = self.up5(e5)           # [B, 256, H/16, W/16]
        d5 = torch.cat([d5, e4], dim=1)
        d5 = self.dec5(d5)
        
        d4 = self.up4(d5)           # [B, 128, H/8, W/8]
        d4 = torch.cat([d4, e3], dim=1)
        d4 = self.dec4(d4)
        
        d3 = self.up3(d4)           # [B, 64, H/4, W/4]
        d3 = torch.cat([d3, e2], dim=1)
        d3 = self.dec3(d3)
        
        d2 = self.up2(d3)           # [B, 64, H/2, W/2]
        d2 = torch.cat([d2, e1], dim=1)
        d2 = self.dec2(d2)
        
        d1 = self.up1(d2)           # [B, 64, H, W]
        # d1 = torch.cat([d1, ???], dim=1)  # Нет skip для самого первого слоя
        
        return self.out_conv(d1)