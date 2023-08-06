from . import configuration_embedded_1dcnn
from . import modeling_embedded_1dcnn

def register():
    configuration_embedded_1dcnn.register()
    modeling_embedded_1dcnn.register()
