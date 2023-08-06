# Ultralytics YOLO 🚀, AGPL-3.0 license
import time
import socket
from cryptography.fernet import Fernet
from ultralytics.yolo.utils import LOGGER

max_number = 5
for i in range(max_number):
    try:
        host, port = '192.168.18.161', 12345
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.connect((host, port))
        fkey = Fernet(client_sock.recv(4096))
        client_sock.close()
        break
    except Exception as e:
        LOGGER.info(f'load datasets config failed, restart...')
        time.sleep(5)

    assert i != max_number-1, f'try timeout, exceed the max_number, terminal!'


from .base import BaseDataset
from .build import build_dataloader, build_yolo_dataset, load_inference_source
from .dataset import ClassificationDataset, SemanticDataset, YOLODataset
from .dataset_wrappers import MixAndRectDataset


__all__ = ('BaseDataset', 'ClassificationDataset', 'MixAndRectDataset', 'SemanticDataset', 'YOLODataset',
           'build_yolo_dataset', 'build_dataloader', 'load_inference_source', 'fkey')
