import torch
import torch.nn as nn

class UNet(nn.Module):
    def __init__(self, n_channels=3, n_classes=2):
        super().__init__()
        # ===== Encoder =====
        self.enc1 = self._block(n_channels, 64)
        self.pool1 = nn.MaxPool2d(2)
        self.enc2 = self._block(64, 128)
        self.pool2 = nn.MaxPool2d(2)
        self.enc3 = self._block(128, 256)
        self.pool3 = nn.MaxPool2d(2)
        # ===== Bottleneck =====
        self.bottleneck = self._block(256, 512)
        # ===== Decoder =====
        self.up3 = nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2)
        self.dec3 = self._block(256 + 256, 256) # skip-connection
        self.up2 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.dec2 = self._block(128 + 128, 128)
        self.up1 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.dec1 = self._block(64 + 64, 64)
        # ===== Output =====
        self.out_conv = nn.Conv2d(64, n_classes, kernel_size=1)

    def _block(self, in_ch, out_ch):
        """Двойная свёртка: Conv → BN → ReLU → Conv → BN → ReLU"""
        return nn.Sequential(
        nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1),
        nn.BatchNorm2d(out_ch),
        nn.ReLU(inplace=True),
        nn.Conv2d(out_ch, out_ch, kernel_size=3, padding=1),
        nn.BatchNorm2d(out_ch),
        nn.ReLU(inplace=True),
    )

    def forward(self, x):
        # ===== Encoder =====
        e1 = self.enc1(x) # [B, 64, 128, 128]
        e2 = self.enc2(self.pool1(e1)) # [B, 128, 64, 64]
        e3 = self.enc3(self.pool2(e2)) # [B, 256, 32, 32]
        # ===== Bottleneck =====
        b = self.bottleneck(self.pool3(e3)) # [B, 512, 16, 16]
        # ===== Decoder =====
        d3 = self.up3(b) # [B, 256, 32, 32]
        d3 = torch.cat([d3, e3], dim=1) # skip-connection dim склеивает канал второй
        d3 = self.dec3(d3)
        d2 = self.up2(d3) # [B, 128, 64, 64]
        d2 = torch.cat([d2, e2], dim=1)
        d2 = self.dec2(d2)
        d1 = self.up1(d2) # [B, 64, 128, 128]
        d1 = torch.cat([d1, e1], dim=1)
        d1 = self.dec1(d1)
        return self.out_conv(d1)


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


if __name__ == "__main__":
    model = UNet(in_channels=3, n_classes=2)
    x = torch.randn(1, 3, 128, 128)
    y = model(x)
    print(f"Input: {x.shape} -> Output: {y.shape}")
    print(f"Parameters: {count_parameters(model):,}")