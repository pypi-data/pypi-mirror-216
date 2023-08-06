#https://huggingface.co/docs/transformers/main_classes/pipelines#transformers.ImageClassificationPipeline
#https://github.com/huggingface/transformers/blob/v4.30.0/src/transformers/pipelines/image_classification.py#L32
from transformers import Pipeline
from transformers.pipelines import PIPELINE_REGISTRY
from torch.nn import functional as F

class CustomImageClassificationPipeline(Pipeline):
    def _sanitize_parameters(self, **kwargs):
        preprocess_kwargs = {}
        postprocess_kwargs = {}
        if "top_k" in kwargs:
            preprocess_kwargs["top_k"] = kwargs["top_k"]
        return preprocess_kwargs, {}, postprocess_kwargs

    def preprocess(self, inputs):
        return self.image_processor(inputs, return_tensors=self.framework)        

    def _forward(self, model_inputs):
        return self.model(**model_inputs)

    def postprocess(self, model_outputs, top_k=5):
        logits = model_outputs['logits']
        #print(logits.shape) #torch.Size([1, 3])
        scores = F.softmax(logits, dim=-1)
        #print(scores.shape) #torch.Size([1, 3])
        postprocessed = []
        for score in scores:
            line = []
            for i, float_score in enumerate(score):
                label = self.model.config.id2label[i]
                line.append({'label': label, 'score': float_score.item()})
            line.sort(key=lambda x: x['score'], reverse=True)
            if top_k != None:
                line = line[:top_k] 
            postprocessed.append(line)
        if len(postprocessed) == 1:
            return postprocessed[0]
        return postprocessed

def register():
    PIPELINE_REGISTRY.register_pipeline('custom-image-classification', 
                                    #pt_model=AutoModelForImageClassification,
                                    pipeline_class=CustomImageClassificationPipeline)
