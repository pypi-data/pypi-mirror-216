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
