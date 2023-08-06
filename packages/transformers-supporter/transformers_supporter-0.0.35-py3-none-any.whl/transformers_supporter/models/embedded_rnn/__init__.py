from . import configuration_embedded_rnn
from . import modeling_embedded_rnn
from . import feature_extraction_embedded_rnn

def register():
    configuration_embedded_rnn.register()
    modeling_embedded_rnn.register()
    feature_extraction_embedded_rnn.register()
