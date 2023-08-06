from typing import Optional
import numpy as np
import io
from mmcv.image.io import supported_backends as mmcv_supported_backends
from mmcv.image.io import use_backend as mmcv_use_backend
from mmcv.image.io import imfrombytes as mmcv_imfrombytes
try:
    import rasterio as rio
except ImportError:
    rio = None

supported_backends=mmcv_supported_backends+['geotiff']
# mmcv_io.supported_backends=mmcv_supported_backends
def use_backend(backend: str) -> None:
    """Select a backend for image decoding.

    Args:
        backend (str): The image decoding backend type. Options are `cv2`,
        `pillow`, `turbojpeg` (see https://github.com/lilohuang/PyTurboJPEG)
        , `tifffile`and `GTiff`. `turbojpeg` is faster but it only supports `.jpeg`
        file format.
    """
    assert backend in supported_backends, f'backend: {backend} is not supported'
    global imread_backend
    imread_backend = backend
   
    if imread_backend == 'geotiff':
        if rio is None:
            raise ImportError('`rasterio` is not installed')
    mmcv_use_backend(backend)

# mmcv_io.use_backend=use_backend

def imfrombytes(content: bytes,
                flag: str = 'color',
                channel_order: str = 'bgr',
                backend: Optional[str] = None) -> np.ndarray:
    
    if backend is None:
        backend = imread_backend
    if backend not in supported_backends:
        raise ValueError(
            f'backend: {backend} is not supported. Supported '
            "backends are 'cv2', 'turbojpeg', 'pillow', 'tifffile' and 'geotiff'.")
    if backend == 'geotiff':
        with io.BytesIO(content) as buff,rio.io.MemoryFile(buff) as memfile:
            with memfile.open() as dataset:
                img = dataset.read()
            return img.transpose(1,2,0)
    else:
        return mmcv_imfrombytes(content, flag, channel_order, backend)

# mmcv_io.imfrombytes=imfrombytes