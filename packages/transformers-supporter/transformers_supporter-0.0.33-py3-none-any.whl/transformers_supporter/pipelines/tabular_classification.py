from transformers import Pipeline
from transformers.pipelines import PIPELINE_REGISTRY
from torch.nn import functional as F

class TabularClassificationPipeline(Pipeline):
    def _sanitize_parameters(self, **kwargs):
        preprocess_kwargs = {}
        if "transformer_path" in kwargs:
            preprocess_kwargs["transformer_path"] = kwargs["transformer_path"]
        postprocess_kwargs = {}
        if "top_k" in kwargs:
            preprocess_kwargs["top_k"] = kwargs["top_k"]
        return preprocess_kwargs, {}, postprocess_kwargs

    def preprocess(self, inputs, transformer_path=None):
        return self.feature_extractor(inputs, transformer_path=transformer_path, return_tensors=self.framework)        
        
    def _forward(self, model_inputs):
        return self.model(**model_inputs)

    def postprocess(self, model_outputs, top_k=None):
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
    PIPELINE_REGISTRY.register_pipeline('tabular-classification', 
                                    #pt_model=AutoModelForTabularClassification
                                    pipeline_class=TabularClassificationPipeline)

'''
#참고

from transformers import Pipeline
from transformers.pipelines import PIPELINE_REGISTRY
from torch.nn import functional as F

class TabularBinaryClassificationPipeline(Pipeline):
    def _sanitize_parameters(self, **kwargs):
        preprocess_kwargs = {}
        if "transformer_path" in kwargs:
            preprocess_kwargs["transformer_path"] = kwargs["transformer_path"]
        postprocess_kwargs = {}
        if "top_k" in kwargs:
            preprocess_kwargs["top_k"] = kwargs["top_k"]
        return preprocess_kwargs, {}, postprocess_kwargs

    def preprocess(self, inputs, transformer_path=None):
        return self.feature_extractor(inputs, transformer_path=transformer_path, return_tensors=self.framework)        

    def _forward(self, model_inputs):
        return self.model(**model_inputs)

    def postprocess(self, model_outputs, top_k=None):
        logits = model_outputs['logits']
        probabilities = F.sigmoid(logits)
        results = []
        for probability in probabilities:
            label = self.model.config.id2label[1 if probability > 0.5 else 0]
            probability = probability if probability > 0.5 else 1 - probability
            results.append({'label': label, 'score': probability.item()})   
        results.sort(key=lambda x: x['score'], reverse=True)
        if top_k != None:
            results = results[:top_k]            
        return results

def register_pipeline():
    PIPELINE_REGISTRY.register_pipeline('tabular-binary-classification', 
                                    #pt_model=AutoModelForTabularClassification
                                    pipeline_class=TabularBinaryClassificationPipeline)
'''
