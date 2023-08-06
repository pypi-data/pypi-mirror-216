from transformers import PretrainedConfig
from transformers import PreTrainedModel
from transformers import AutoModel
from transformers import AutoTokenizer
from transformers import AutoConfig
from transformers import AutoModelForSequenceClassification
import torch
from torch.nn import functional as F
import pytorch_supporter
import transformers
from .configuration_embedded_rnn import EmbeddedRnnConfig

class EmbeddedRnnForSequenceClassification(PreTrainedModel):
    config_class = EmbeddedRnnConfig

    def __init__(self, config):
        super().__init__(config)        
        self.layer = torch.nn.Sequential(
            torch.nn.Embedding(num_embeddings=config.vocab_size, embedding_dim=32),
            pytorch_supporter.layers.HiddenStateResetLSTM(input_size=32, hidden_size=32, batch_first=True),
            pytorch_supporter.layers.LSTMLastHiddenState(),
            torch.nn.Linear(in_features=32, out_features=config.num_labels)
        )

    def forward(self, input_ids, labels=None):
        logits = self.layer(input_ids)
        #print(logits.shape) #torch.Size([16, 3])
        if labels == None:
            return transformers.file_utils.ModelOutput({'logits': logits})
        else:
            loss = F.nll_loss(F.log_softmax(logits), labels) #원핫 벡터를 넣을 필요없이 바로 실제값을 인자로 사용 #nll은 Negative Log Likelihood의 약자
            return transformers.file_utils.ModelOutput({'loss': loss, 'logits': logits})

from transformers import PretrainedConfig
from transformers import PreTrainedModel
from transformers import AutoModel
from transformers import AutoTokenizer
from transformers import AutoConfig
import torch
from torch.nn import functional as F
import pytorch_supporter
import transformers
from .configuration_embedded_rnn import EmbeddedRnnConfig

class EmbeddedRnnForFixedLengthTranslation(PreTrainedModel):
    config_class = EmbeddedRnnConfig

    def __init__(self, config):
        super().__init__(config)        
        self.layer = torch.nn.Sequential(
            torch.nn.Embedding(num_embeddings=config.vocab_size, embedding_dim=32),
            pytorch_supporter.layers.HiddenStateResetLSTM(input_size=32, hidden_size=32, batch_first=True),
            pytorch_supporter.layers.SelectFromArray(index=0), #lstm output, 모든 타임 스텝(토큰: 숫자, 문자, 단어)의 숨은 상태, torch.Size([8, 380, 32]) 
            torch.nn.Linear(in_features=32, out_features=config.vocab_size)
        )

    def forward(self, input_ids, labels=None):
        logits = self.layer(input_ids)
        #print(logits.shape) #torch.Size([2, 3, 7])
        if labels == None:
            return transformers.file_utils.ModelOutput({'logits': logits})
        else:
            #print(labels.shape) #torch.Size([2, 3])
            logits_ = logits.view(-1, logits.size(-1))
            labels_ = labels.view(-1)
            #print(logits_.shape) #torch.Size([6, 7])
            #print(labels_.shape) #torch.Size([6])
            loss = F.nll_loss(F.log_softmax(logits_), labels_) #원핫 벡터를 넣을 필요없이 바로 실제값을 인자로 사용 #nll은 Negative Log Likelihood의 약자
            return transformers.file_utils.ModelOutput({'loss': loss, 'logits': logits})

def register():
    AutoModelForSequenceClassification.register(EmbeddedRnnConfig, EmbeddedRnnForSequenceClassification)
    #AutoModelForFixedLengthTranslation.register(EmbeddedRnnConfig, EmbeddedRnnForFixedLengthTranslation)
    
