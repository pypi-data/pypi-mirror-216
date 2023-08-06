from . import configuration_ann
from . import modeling_ann
from . import feature_extraction_ann

def register():
    configuration_ann.register()
    modeling_ann.register()
    feature_extraction_ann.register()
  
