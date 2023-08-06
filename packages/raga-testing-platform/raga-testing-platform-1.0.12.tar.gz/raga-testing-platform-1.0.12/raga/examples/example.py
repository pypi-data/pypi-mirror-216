from raga import *
import pandas as pd
import json
import ast

ds_json_file = "MB.json"

test_df = []
with open(ds_json_file, 'r') as json_file:
    # Load JSON data
    json_data = json.load(json_file)
    
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
            'TimeOfCapture': TimeStampElement(item["capture_time"]),
            'SourceLink': StringElement(item["inputs"][0]),
            'AnnotationsV1': AnnotationsV1,
            'ROIVectorsM1': ROIVectorsM1,
            'ImageVectorsM1': ImageVectorsM1,
        }

        merged_dict = {**data_point, **attributes_dict}

        test_df.append(merged_dict)
        

pd_ds = pd.DataFrame(test_df)


# data_frame_extractor(pd_ds).to_csv("MB_new.csv", index=False)

schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement())
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement())
schema.add("SourceLink", FeatureSchemaElement())
schema.add("Resolution", AttributeSchemaElement())
schema.add("Scene", AttributeSchemaElement())
schema.add("AnnotationsV1", InferenceSchemaElement(model="57_improved"))
schema.add("ImageVectorsM1", ImageEmbeddingSchemaElement(model="57_improved", ref_col_name=""))
schema.add("ROIVectorsM1", RoiEmbeddingSchemaElement(model="57_improved", ref_col_name=""))

test_session = TestSession("testingProject", "test_exp_serve_test_37")

# Create an instance of the Dataset class
test_ds = Dataset(test_session, "ServeDataset_6")

test_ds.load(pd_ds, schema)
test_ds.head()


testName = StringElement("testABTes2")
testName1 = StringElement("testABTest3")
modelA = StringElement("modelA")
modelB = StringElement("modelB")
gt = StringElement("GT")
labelled_type = ModelABTestTypeElement("labelled")
unlabelled_type = ModelABTestTypeElement("unlabelled")
aggregation_level = AggregationLevelElement()
aggregation_level.add(StringElement("weather"))
aggregation_level.add(StringElement("scene"))
aggregation_level.add(StringElement("time_of_day"))
rules = ModelABTestRules()
rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

model_comparison_check = model_ab_test(test_ds, testName=testName, modelA = modelA , modelB = modelB , gt = gt,  type = labelled_type, aggregation_level = aggregation_level, rules = rules)

model_comparison_check = model_ab_test(test_ds, testName=testName1, modelA = modelA , modelB = modelB , type = unlabelled_type, aggregation_level = aggregation_level, rules = rules)