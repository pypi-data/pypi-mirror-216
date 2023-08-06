from raga import *
import pandas as pd
import json
import datetime

def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def convert_json_to_data_frame(json_file_path):
    test_data_frame = []
    with open(json_file_path, 'r') as json_file:
        # Load JSON data
        json_data = json.load(json_file)
        hr = 1
        # Process the JSON data
        transformed_data = []
        for item in json_data:
            AnnotationsV1 = ImageDetectionObject()
            ROIVectorsM1 = ROIEmbedding()
            ImageVectorsM1 = ImageEmbedding()
            for detection in item["outputs"][0]["detections"]:
                AnnotationsV1.add(ObjectDetection(Id=0, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
                for roi_emb in detection['roi_embedding']:
                    ROIVectorsM1.add(Embedding(roi_emb))
            
            attributes_dict = {}
            attributes = item.get("attributes", {})
            for key, value in attributes.items():
                attributes_dict[key] = StringElement(value)

            image_embeddings = item.get("image_embedding", {})
            for value in image_embeddings:
                ImageVectorsM1.add(Embedding(value))

            data_point = {
                'ImageId': StringElement(item["inputs"][0]),
                'TimeOfCapture': TimeStampElement(get_timestamp_x_hours_ago(hr)),
                'SourceLink': StringElement(item["inputs"][0]),
                'AnnotationsV1': AnnotationsV1,
                'ROIVectorsM1': ROIVectorsM1,
                'ImageVectorsM1': ImageVectorsM1,
            }

            merged_dict = {**data_point, **attributes_dict}
            test_data_frame.append(merged_dict)
            hr+=1
    return test_data_frame

pd_modelA = pd.DataFrame(convert_json_to_data_frame("test-dataset-modelA.json"))
pd_modelB = pd.DataFrame(convert_json_to_data_frame("test-dataset-modelB.json"))


schema_model_a = RagaSchema()
schema_model_a.add("ImageId", PredictionSchemaElement(), pd_modelA)
schema_model_a.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_modelA)
schema_model_a.add("SourceLink", FeatureSchemaElement(), pd_modelA)
schema_model_a.add("Reflection", AttributeSchemaElement(), pd_modelA)
schema_model_a.add("Overlap", AttributeSchemaElement(), pd_modelA)
schema_model_a.add("CameraAngle", AttributeSchemaElement(), pd_modelA)
schema_model_a.add("AnnotationsV1", InferenceSchemaElement(model="modelA"), pd_modelA)
schema_model_a.add("ImageVectorsM1", ImageEmbeddingSchemaElement(model="modelA", ref_col_name=""), pd_modelA)
schema_model_a.add("ROIVectorsM1", RoiEmbeddingSchemaElement(model="modelA", ref_col_name=""), pd_modelA)

schema_model_b = RagaSchema()
schema_model_b.add("ImageId", PredictionSchemaElement(), pd_modelB)
schema_model_b.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_modelB)
schema_model_b.add("SourceLink", FeatureSchemaElement(), pd_modelB)
schema_model_b.add("Reflection", AttributeSchemaElement(), pd_modelB)
schema_model_b.add("Overlap", AttributeSchemaElement(), pd_modelB)
schema_model_b.add("CameraAngle", AttributeSchemaElement(), pd_modelB)
schema_model_b.add("AnnotationsV1", InferenceSchemaElement(model="ModelB"), pd_modelB)
schema_model_b.add("ImageVectorsM1", ImageEmbeddingSchemaElement(model="ModelB", ref_col_name=""), pd_modelB)
schema_model_b.add("ROIVectorsM1", RoiEmbeddingSchemaElement(model="ModelB", ref_col_name=""), pd_modelB)
