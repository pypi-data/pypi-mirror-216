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

def convert_json_to_data_frame(json_file_path_model_1, json_file_path_model_2):
    test_data_frame = []
    with open(json_file_path_model_1, 'r') as json_file:
        # Load JSON data
        model_1 = json.load(json_file)
    with open(json_file_path_model_2, 'r') as json_file:
        # Load JSON data
        model_2 = json.load(json_file)

    # Create a dictionary to store the inputs and corresponding data points
    inputs_dict = {}
    hr = 1
    # Process model_1 data
    for item in model_1:
        inputs = item["inputs"]
        inputs_dict[tuple(inputs)] = item
    
    # Process model_2 data
    for item in model_2:
        inputs = item["inputs"]
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

        merged_item = inputs_dict.get(tuple(inputs), {})
        AnnotationsV2 = ImageDetectionObject()
        ROIVectorsM2 = ROIEmbedding()
        ImageVectorsM2 = ImageEmbedding()
        for detection in merged_item["outputs"][0]["detections"]:
            AnnotationsV2.add(ObjectDetection(Id=0, ClassId=0, ClassName=detection['class'], Confidence=detection['confidence'], BBox= detection['bbox'], Format="xywh_normalized"))
            for roi_emb in detection['roi_embedding']:
                ROIVectorsM2.add(Embedding(roi_emb))
        
        image_embeddings = merged_item.get("image_embedding", {})
        for value in image_embeddings:
            ImageVectorsM2.add(Embedding(value))

        data_point = {
            'ImageId': StringElement(item["inputs"][0]),
            'TimeOfCapture': TimeStampElement(get_timestamp_x_hours_ago(hr)),
            'SourceLink': StringElement(item["inputs"][0]),
            'AnnotationsV1': AnnotationsV1,
            'ROIVectorsM1': ROIVectorsM1,
            'ImageVectorsM1': ImageVectorsM1,
            'AnnotationsV2': AnnotationsV2,
            'ROIVectorsM2': ROIVectorsM2,
            'ImageVectorsM2': ImageVectorsM2,
        }

        merged_dict = {**data_point, **attributes_dict}
        test_data_frame.append(merged_dict)
        hr+=1

    return test_data_frame

pd_data_frame = pd.DataFrame(convert_json_to_data_frame("test-dataset-modelA.json", "test-dataset-modelB.json"))

schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement(), pd_data_frame)
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_data_frame)
schema.add("SourceLink", FeatureSchemaElement(), pd_data_frame)
schema.add("Reflection", AttributeSchemaElement(), pd_data_frame)
schema.add("Overlap", AttributeSchemaElement(), pd_data_frame)
schema.add("CameraAngle", AttributeSchemaElement(), pd_data_frame)
schema.add("AnnotationsV1", InferenceSchemaElement(model="modelA-column-name-test-1"), pd_data_frame)
schema.add("ImageVectorsM1", ImageEmbeddingSchemaElement(model="modelA-column-name-test-1", ref_col_name=""), pd_data_frame)
schema.add("ROIVectorsM1", RoiEmbeddingSchemaElement(model="modelA-column-name-test-1", ref_col_name=""), pd_data_frame)
schema.add("AnnotationsV2", InferenceSchemaElement(model="modelB-column-name-test-1"), pd_data_frame)
schema.add("ImageVectorsM2", ImageEmbeddingSchemaElement(model="modelB-column-name-test-1", ref_col_name=""), pd_data_frame)
schema.add("ROIVectorsM2", RoiEmbeddingSchemaElement(model="modelB-column-name-test-1", ref_col_name=""), pd_data_frame)


test_session = TestSession(project_name="testingProject",run_name= "test_iteration-test-maan-column-name-test-13")

test_ds = Dataset(test_session=test_session, name="test-dataset-column-name-issue-test-1")

test_ds.load(pd_data_frame, schema)


testName = StringElement("testABNewTest-A-column-name-test-13")
modelA = StringElement("modelA-column-name-test-1")
modelB = StringElement("modelB-column-name-test-1")
type = ModelABTestTypeElement("unlabelled")
aggregation_level = AggregationLevelElement()
aggregation_level.add(StringElement("Reflection"))
aggregation_level.add(StringElement("Overlap"))
aggregation_level.add(StringElement("CameraAngle"))
rules = ModelABTestRules()
rules.add(metric = StringElement("difference_percentage"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.2))
rules.add(metric = StringElement("difference_count"), IoU = FloatElement(0.5), _class = StringElement("vehicle"), threshold = FloatElement(0.5))


model_comparison_check = model_ab_test(test_ds, testName=testName, modelA = modelA , modelB = modelB , type = type, aggregation_level = aggregation_level, rules = rules)

test_session.add(model_comparison_check)

test_session.run()