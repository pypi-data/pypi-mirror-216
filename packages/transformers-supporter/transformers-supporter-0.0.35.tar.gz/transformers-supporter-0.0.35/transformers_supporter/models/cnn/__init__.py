from . import configuration_cnn
from . import modeling_cnn
from . import image_processing_cnn

def register():
    configuration_cnn.register()
    modeling_cnn.register()
    image_processing_cnn.register()
