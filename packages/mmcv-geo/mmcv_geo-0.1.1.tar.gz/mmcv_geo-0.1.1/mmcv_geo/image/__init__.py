from .io import supported_backends,use_backend,imfrombytes
from mmcv.image import io as mmcv_io
def init():
    mmcv_io.supported_backends+=['geotiff']
    mmcv_io.use_backend=use_backend
    mmcv_io.imfrombytes=imfrombytes