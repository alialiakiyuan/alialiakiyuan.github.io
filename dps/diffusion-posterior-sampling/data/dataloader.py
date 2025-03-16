from glob import glob
from PIL import Image
from typing import Callable, Optional
from torch.utils.data import DataLoader
from torchvision.datasets import VisionDataset
import torchvision.transforms as T  # 给导入的 transforms 模块起别名

__DATASET__ = {}


def register_dataset(name: str):
    def wrapper(cls):
        if __DATASET__.get(name, None):
            raise NameError(f"Name {name} is already registered!")
        __DATASET__[name] = cls
        return cls

    return wrapper


def get_dataset(name: str, root: str, **kwargs):
    if __DATASET__.get(name, None) is None:
        raise NameError(f"Dataset {name} is not defined.")
    return __DATASET__[name](root=root, **kwargs)


def get_dataloader(dataset: VisionDataset,
                   batch_size: int,
                   num_workers: int,
                   train: bool):
    dataloader = DataLoader(dataset,
                            batch_size,
                            shuffle=train,
                            num_workers=num_workers,
                            drop_last=train)
    return dataloader


@register_dataset(name='ffhq')
class FFHQDataset(VisionDataset):
    def __init__(self, root: str, transforms: Optional[Callable] = None):
        if transforms is None:
            # 使用别名 T 来调用 Compose 方法
            transforms = T.Compose([
                T.ToTensor()
            ])
        super().__init__(root, transforms)

        self.fpaths = sorted(glob(root + '/**/*.png', recursive=True))
        assert len(self.fpaths) > 0, "File list is empty. Check the root."

    def __len__(self):
        return len(self.fpaths)

    def __getitem__(self, index: int):
        fpath = self.fpaths[index]
        img = Image.open(fpath).convert('RGB')

        if self.transforms is not None:
            img = self.transforms(img)

        return img


# 新增的数据集类
@register_dataset(name='newdata')
class NewDataset(VisionDataset):
    def __init__(self, root: str, transforms: Optional[Callable] = None):
        if transforms is None:
            # 使用别名 T 来调用 Compose 方法
            transforms = T.Compose([
                T.ToTensor()
            ])
        super().__init__(root, transforms)

        self.fpaths = sorted(glob(root + '/**/*.jpg', recursive=True))
        assert len(self.fpaths) > 0, "File list is empty. Check the root."

    def __len__(self):
        return len(self.fpaths)

    def __getitem__(self, index: int):
        fpath = self.fpaths[index]
        img = Image.open(fpath).convert('RGB')

        if self.transforms is not None:
            img = self.transforms(img)

        return img