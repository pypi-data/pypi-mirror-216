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

ds_json_file = "improved_rtl.json"

test_df = []
with open(ds_json_file, 'r') as json_file:
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
        test_df.append(merged_dict)
        hr+=1
        

pd_ds = pd.DataFrame(test_df)


# data_frame_extractor(pd_ds).to_csv("improved_rtl.csv", index=False)

schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement(), pd_ds)
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_ds)
schema.add("SourceLink", FeatureSchemaElement(), pd_ds)
schema.add("Reflection", AttributeSchemaElement(), pd_ds)
schema.add("Overlap", AttributeSchemaElement(), pd_ds)
schema.add("CameraAngle", AttributeSchemaElement(), pd_ds)
schema.add("AnnotationsV1", InferenceSchemaElement(model="57_improved"), pd_ds)
schema.add("ImageVectorsM1", ImageEmbeddingSchemaElement(model="57_improved", ref_col_name=""), pd_ds)
schema.add("ROIVectorsM1", RoiEmbeddingSchemaElement(model="57_improved", ref_col_name=""), pd_ds)

test_session = TestSession(project_name="testingProject",run_name= "test_iteration-test-90")

# Create an instance of the Dataset class
test_ds = Dataset(test_session=test_session, name="self_serve-Image-Editing")

test_ds.load(pd_ds, schema)




# testName = StringElement("testABNewTest-B-11")
# modelA = StringElement("57_improved")
# modelB = StringElement("57_improved")
# gt = StringElement("GT")
# type = ModelABTestTypeElement("labelled")
# aggregation_level = AggregationLevelElement()
# aggregation_level.add(StringElement("Reflection"))
# aggregation_level.add(StringElement("Overlap"))
# aggregation_level.add(StringElement("CameraAngle"))
# rules = ModelABTestRules()
# rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))

# model_comparison_check = model_ab_test(test_ds, testName=testName, modelA = modelA , modelB = modelB , gt = gt,  type = type, aggregation_level = aggregation_level, rules = rules)

# test_session.add(model_comparison_check)


testName = StringElement("testABNewTest-100")
modelA = StringElement("modelA")
modelB = StringElement("modelB")
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