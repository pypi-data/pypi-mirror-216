from . import models
from . import pipelines

#

from .models.ann import configuration_ann
from .models.ann import feature_extraction_ann
from .models.ann import modeling_ann

from .models.cnn import configuration_cnn
from .models.cnn import modeling_cnn
from .models.cnn import image_processing_cnn

from .models.custom_bert import configuration_custom_bert
from .models.custom_bert import modeling_custom_bert

from .models.embedded_1dcnn import configuration_embedded_1dcnn
from .models.embedded_1dcnn import modeling_embedded_1dcnn

from .models.embedded_rnn import configuration_embedded_rnn
from .models.embedded_rnn import modeling_embedded_rnn
from .models.embedded_rnn import feature_extraction_embedded_rnn

from .models.pretrained_embedded_rnn import configuration_pretrained_embedded_rnn
from .models.pretrained_embedded_rnn import modeling_pretrained_embedded_rnn

from .models.faster_rcnn import configuration_faster_rcnn
from .models.faster_rcnn import modeling_faster_rcnn
from .models.faster_rcnn import image_processing_faster_rcnn

from .models.rnn import configuration_rnn
from .models.rnn import modeling_rnn
from .models.rnn import feature_extraction_rnn

from .pipelines import tabular_regression
from .pipelines import tabular_classification
from .pipelines import custom_image_classification
from .pipelines import fixed_length_translation

def register():
    configuration_ann.register()
    modeling_ann.register()
    feature_extraction_ann.register()

    configuration_cnn.register()
    modeling_cnn.register()
    image_processing_cnn.register()

    configuration_custom_bert.register()
    modeling_custom_bert.register()

    configuration_embedded_1dcnn.register()
    modeling_embedded_1dcnn.register()

    configuration_embedded_rnn.register()
    modeling_embedded_rnn.register()
    feature_extraction_embedded_rnn.register()

    configuration_pretrained_embedded_rnn.register()
    modeling_pretrained_embedded_rnn.register()

    configuration_faster_rcnn.register()
    modeling_faster_rcnn.register()
    image_processing_faster_rcnn.register()

    configuration_rnn.register()
    modeling_rnn.register()
    feature_extraction_rnn.register()
    
    tabular_regression.register()
    tabular_classification.register()
    custom_image_classification.register()
    fixed_length_translation.register()
