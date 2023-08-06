from . import configuration_rnn
from . import modeling_rnn
from . import feature_extraction_rnn

def register():
    configuration_rnn.register()
    modeling_rnn.register()
    feature_extraction_rnn.register()
