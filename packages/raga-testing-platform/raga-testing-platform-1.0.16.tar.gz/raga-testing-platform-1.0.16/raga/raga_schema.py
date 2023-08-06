from abc import ABC
from typing import Optional
from datetime import datetime
import pandas as pd

class RagaSchemaElement(ABC):
    def __init__(self):
        super().__init__()
        self.type: str
        self.model: Optional[str]
        self.ref_col_name: Optional[str]

class PredictionSchemaElement(RagaSchemaElement):
    def __init__(self):
        super().__init__()
        self.type = "imageName"
        self.model = ""
        self.ref_col_name = ""

class TimeOfCaptureSchemaElement(RagaSchemaElement):
    def __init__(self):
        super().__init__()
        self.type = "timestamp"
        self.model = ""
        self.ref_col_name = ""

class FeatureSchemaElement(RagaSchemaElement):
    def __init__(self):
        super().__init__()
        self.type = "feature"
        self.model = ""
        self.ref_col_name = ""
class AttributeSchemaElement(RagaSchemaElement):
    def __init__(self):
        super().__init__()
        self.type = "attribute"
        self.model = ""
        self.ref_col_name = ""

class InferenceSchemaElement(RagaSchemaElement):
    def __init__(self, model:str):
        if not isinstance(model, str) or not model: 
            raise ValueError("model is required and must be a non-empty string.")
        self.type = "inference"
        self.model = model
        self.ref_col_name = ""

class ImageEmbeddingSchemaElement(RagaSchemaElement):
    def __init__(self, model:str, ref_col_name:str):
        if not isinstance(model, str) or not model: 
            raise ValueError("model is required and must be a non-empty string.")
        self.type = "imageEmbedding"
        self.model = model
        self.ref_col_name = ref_col_name


class RoiEmbeddingSchemaElement(RagaSchemaElement):
    def __init__(self, model:str, ref_col_name:str):
        if not isinstance(model, str) or not model: 
            raise ValueError("model is required and must be a non-empty string.")
        self.type = "roiEmbedding"
        self.model = model
        self.ref_col_name = ref_col_name



class RagaSchema():
    def __init__(self):
        self.columns = list()

    def validation(self, column_name: str, ragaSchemaElement:RagaSchemaElement, data_frame:pd.DataFrame):
        if not isinstance(column_name, str) or not column_name: 
            raise ValueError("column_name is required and must be a non-empty string.")
        if not isinstance(ragaSchemaElement, RagaSchemaElement): 
            raise ValueError("ragaSchemaElement must be an instance of the RagaSchemaElement.")
        if not isinstance(data_frame, pd.DataFrame): 
            raise ValueError("data_frame must be an instance of the pd.DataFrame.")
        return True
     
    def add(self, column_name: str, ragaSchemaElement, data_frame:pd.DataFrame):
        self.validation(column_name, ragaSchemaElement, data_frame)
        column_list = data_frame.columns.to_list()
        if column_name in column_list:
            self.columns.append({"customerColumnName":column_name, "type":ragaSchemaElement.type, "modelName":ragaSchemaElement.model, "ref_col_name":ragaSchemaElement.ref_col_name})
        else:
            raise ValueError(f"Raga Schema Error: Column name `{column_name}` not found in provided Data Frame. {column_list}")

class StringElement():
    def __init__(self, value:str):
        self.value = value

    def get(self):
        return self.value
    
class FloatElement():
    def __init__(self, value:float):
        self.value = value

    def get(self):
        return self.value
    
class TimeStampElement():
    def __init__(self, date_time:datetime):
        self.date_time = date_time

    def get(self):
        return self.date_time
    
class AggregationLevelElement():
    def __init__(self):
        self.levels = []

    def add(self, level:StringElement):
        self.levels.append(level.get())

    def get(self):
        return self.levels
    
class ModelABTestTypeElement():
    def __init__(self, type:str):
        self.type = type
        if self.type not in ["labelled", "unlabelled"]:
            raise ValueError("Invalid value for 'type'. Must be one of: ['labelled', 'unlabelled'].")

    def get(self):
        return self.type    

       
class ModelABTestRules():
    def __init__(self):
        self.rules = []

    def add(self, metric:StringElement, IoU:FloatElement, _class:StringElement, threshold:FloatElement):
        self.rules.append({ "metric" : metric.get(), "iou": IoU.get(),  "class": _class.get(), "threshold":threshold.get() })

    def get(self):
        return self.rules
class ObjectDetection:
    def __init__(self, Id:Optional[str], Format:Optional[str], Confidence:Optional[float], ClassId:Optional[str] = None, ClassName:Optional[str]=None, BBox=None):
        self.Id = Id
        self.ClassId = ClassId
        self.ClassName = ClassName
        self.BBox = BBox
        self.Format = Format
        self.Confidence = Confidence

class ImageDetectionObject():
    def __init__(self):
        self.detections = list()
    
    def add(self, object_detection:ObjectDetection):
        self.detections.append(object_detection.__dict__)
    
    def get(self):
        return self.__dict__

class Embedding:
    def __init__(self, embedding: float):
        self.embedding = embedding

class ImageEmbedding:
    def __init__(self):
         self.embeddings = []

    def add(self, embedding_values: Embedding):
        self.embeddings.append(embedding_values.embedding)

    def get(self):
        return self.__dict__

class ROIEmbedding:
    def __init__(self):
         self.embeddings = []

    def add(self, embedding_values: Embedding):
        self.embeddings.append(embedding_values.embedding)

    def get(self):
        return self.__dict__
