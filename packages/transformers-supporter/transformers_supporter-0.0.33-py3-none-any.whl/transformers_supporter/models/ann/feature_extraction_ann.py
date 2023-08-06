from transformers import FeatureExtractionMixin
from transformers import AutoFeatureExtractor
from transformers import BatchFeature
import numpy as np
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import LabelBinarizer
import pickle
from transformers.utils import cached_file
from pathlib import Path

class TabularFeatureExtractor(FeatureExtractionMixin):
    pretrained_model_name_or_path = None
    transformer = None
    le = None

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, **kwargs):
        feature_extractor_dict, kwargs = cls.get_feature_extractor_dict(pretrained_model_name_or_path, **kwargs)
        cls.pretrained_model_name_or_path = pretrained_model_name_or_path #
        return cls.from_dict(feature_extractor_dict, **kwargs)
    
    #labels_shape: list, one, onehot
    #labels_type: float, long
    def __init__(
        self,  
        continuous_columns=['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 'Credit_History'],
        categorical_columns=['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area'],
        labels_column='Target',
        labels_shape='list',
        labels_type='float',
        **kwargs
    ):
        super().__init__(**kwargs)
        self.continuous_columns = continuous_columns
        self.categorical_columns = categorical_columns
        self.labels_column = labels_column
        self.labels_shape = labels_shape
        self.labels_type = labels_type
        self.labels = []

        if TabularFeatureExtractor.pretrained_model_name_or_path:
            if Path(TabularFeatureExtractor.pretrained_model_name_or_path).exists():
                transformer_file = f'{TabularFeatureExtractor.pretrained_model_name_or_path}/transformer.pkl'
            else:
                #transformer_file = cached_file(path_or_repo_id='automatethem/imdb-text-classification', filename='transformer.pkl')
                transformer_file = cached_file(path_or_repo_id=TabularFeatureExtractor.pretrained_model_name_or_path, filename='transformer.pkl')
                #print(transformer_file) #/root/.cache/huggingface/hub/models--automatethem--iris-tabular-classification/snapshots/c588c4558da42a7c63fdb05bef68ecc35dc19710/transformer.pkl
            with open(transformer_file, 'rb') as f:
                TabularFeatureExtractor.transformer = pickle.load(f)
    
    def __call__(self, df, return_tensors=None, **kwargs):
        x = df[self.continuous_columns + self.categorical_columns]
        x = TabularFeatureExtractor.transformer.transform(x)
        x = np.array(x, dtype=np.float32)
        #print(x.shape) #

        #학습
        if self.labels_column in df.columns:
            labels = df[self.labels_column]
            labels = labels.to_numpy()

            if df[self.labels_column].dtype == 'object':
                if self.labels_shape == 'list':
                    labels = TabularFeatureExtractor.le.transform(labels)
                elif self.labels_shape == 'one':
                    labels = TabularFeatureExtractor.le.transform(labels)
                    labels = labels.reshape(-1, 1)
                elif self.labels_shape == 'onehot':
                    labels = TabularFeatureExtractor.le.transform(labels)

            if self.labels_type == 'long':
                labels = np.array(labels, dtype=np.longlong)
            elif self.labels_type == 'float':
                labels = np.array(labels, dtype=np.float32)

            '''
            if return_tensors == 'pt':
                x = torch.from_numpy(x)
                labels = torch.from_numpy(labels)
            return {'x': x, 'labels': labels}
            '''
            #'''
            return BatchFeature(data={'x': x, 'labels': labels}, tensor_type=return_tensors)
            #'''
        #예측
        else:
            '''
            if return_tensors == 'pt':
                x = torch.from_numpy(x)
            return {'x': x}
            '''
            #'''
            return BatchFeature(data={'x': x}, tensor_type=return_tensors)
            #'''

    def train(self, df):
        x = df[self.continuous_columns + self.categorical_columns]
        TabularFeatureExtractor.transformer = make_column_transformer(
            (OneHotEncoder(), self.categorical_columns),
            remainder='passthrough')
        if len(self.continuous_columns) >= 2:
            TabularFeatureExtractor.transformer = make_pipeline(TabularFeatureExtractor.transformer, MinMaxScaler())
        TabularFeatureExtractor.transformer.fit(x)

        if df[self.labels_column].dtype == 'object':
            labels = df[self.labels_column]
            if self.labels_shape == 'list':
                TabularFeatureExtractor.le = LabelEncoder()
                TabularFeatureExtractor.le.fit(labels)
                #print(TabularFeatureExtractor.le.classes_) #['N' 'Y']
                self.labels = TabularFeatureExtractor.le.classes_ 
            elif self.labels_shape == 'one':
                TabularFeatureExtractor.le = LabelEncoder()
                TabularFeatureExtractor.le.fit(labels)
                #print(TabularFeatureExtractor.le.classes_) #['N' 'Y']
                self.labels = TabularFeatureExtractor.le.classes_ 
            elif self.labels_shape == 'onehot':
                TabularFeatureExtractor.le = LabelBinarizer()
                labels = df[self.labels_column]
                TabularFeatureExtractor.le.fit(labels)
                #print(TabularFeatureExtractor.le.classes_) #['N' 'Y']
                self.labels = TabularFeatureExtractor.le.classes_ 

    #https://github.com/huggingface/transformers/blob/c8f35a9ce37bd03f37fcf8336172bdcbe7ffc86a/src/transformers/feature_extraction_utils.py#L333
    def save_pretrained(self, save_directory, push_to_hub=False, **kwargs):
        #print(save_directory) #/content/drive/MyDrive/models/pytorch/models/bank-loan-model-for-tabular-classification
        transformer_file = f'{save_directory}/transformer.pkl'
        with open(transformer_file, 'wb') as f:
            pickle.dump(TabularFeatureExtractor.transformer, f)
        return super().save_pretrained(save_directory, push_to_hub, **kwargs)

def register():
    AutoFeatureExtractor.register(TabularFeatureExtractor, TabularFeatureExtractor)
