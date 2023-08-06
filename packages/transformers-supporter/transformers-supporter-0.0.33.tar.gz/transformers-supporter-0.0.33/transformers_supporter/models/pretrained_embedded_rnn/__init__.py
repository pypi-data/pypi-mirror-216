from . import configuration_pretrained_embedded_rnn
from . import modeling_pretrained_embedded_rnn

def register():
    configuration_pretrained_embedded_rnn.register()
    modeling_pretrained_embedded_rnn.register()
