from transformers import Pipeline
from transformers.pipelines import PIPELINE_REGISTRY
from torch.nn import functional as F

class FixedLengthTranslationPipeline(Pipeline):
    def _sanitize_parameters(self, **kwargs):
        preprocess_kwargs = {}
        if 'vocab_path' in kwargs:
            preprocess_kwargs['vocab_path'] = kwargs['vocab_path']
        postprocess_kwargs = {}
        return preprocess_kwargs, {}, postprocess_kwargs

    def preprocess(self, inputs, vocab_path=None):
        return self.tokenizer(inputs, vocab_path=vocab_path, return_tensors=self.framework)        

    def _forward(self, model_inputs):
        return self.model(**model_inputs)

    def postprocess(self, model_outputs):
        logits = model_outputs['logits']
        #print(logits.shape) #torch.Size([1, 3, 9])
        scores = F.softmax(logits, dim=-1)
        indexes = scores.argmax(axis=-1)
        #print(indexes.shape) #torch.Size([1, 3])
        postprocessed = []
        for index in indexes:
            #print(index) #tensor([2, 4, 6], device='mps:0')
            tokens = self.tokenizer.convert_ids_to_tokens(index)
            translation_text = ' '.join(tokens)
            postprocessed.append({'translation_text': translation_text}) 
        return postprocessed
        
def register():
    PIPELINE_REGISTRY.register_pipeline('fixed-length-translation', 
                                    #pt_model=AutoModelForFixedLengthTranslation,
                                    pipeline_class=FixedLengthTranslationPipeline)
