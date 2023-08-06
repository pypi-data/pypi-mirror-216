from . import configuration_custom_bert
from . import modeling_custom_bert

def register():
    configuration_custom_bert.register()
    modeling_custom_bert.register()
