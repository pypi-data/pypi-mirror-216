from typing import Optional
from raga import Dataset, StringElement, AggregationLevelElement, ModelABTestRules, ModelABTestTypeElement

def model_ab_test(test_ds: Dataset, testName: StringElement, modelA: StringElement, modelB: StringElement,
                  type: ModelABTestTypeElement, aggregation_level: AggregationLevelElement, rules: ModelABTestRules,
                  gt: Optional[StringElement] = StringElement(""), filter: Optional[StringElement] = StringElement("")):
    ab_test_validation(test_ds, testName, modelA, modelB, type, aggregation_level, rules, gt)      
    return {
            "datasetId": test_ds.dataset_id,
            "experimentId": test_ds.test_session.experiment_id,
            "name": testName.get(),
            "filter": filter.get(),
            "modelA": modelA.get(),
            "modelB": modelB.get(),
            "gt": gt.get(),
            "type": type.get(),
            "aggregationLevels": aggregation_level.get(),
            "rules": rules.get()
        }


def ab_test_validation(test_ds: Dataset, testName: StringElement, modelA: StringElement, modelB: StringElement,
               type: ModelABTestTypeElement, aggregation_level: AggregationLevelElement, rules: ModelABTestRules,
               gt: Optional[StringElement] = StringElement("")):
    assert isinstance(test_ds, Dataset), "test_ds must be an instance of the Dataset class."
    assert isinstance(testName, StringElement) and testName.get(), "testName is required and must be an instance of the StringElement class."
    assert isinstance(modelA, StringElement) and modelA.get(), "modelA is required and must be an instance of the StringElement class."
    assert isinstance(modelB, StringElement) and modelB.get(), "modelB is required and must be an instance of the StringElement class."
    assert isinstance(type, ModelABTestTypeElement), "type must be an instance of the ModelABTestTypeElement class."
    assert isinstance(aggregation_level, AggregationLevelElement) and aggregation_level.get(), "aggregation_level is required and must be an instance of the AggregationLevelElement class."
    assert isinstance(rules, ModelABTestRules) and rules.get(), "rules is required and must be an instance of the ModelABTestRules class."

    if type.get() == "labelled":
        assert isinstance(gt, StringElement) and gt.get(), "gt is required on labelled type and must be an instance of the StringElement class."

    if type.get() == "unlabelled":
        if isinstance(gt, StringElement) and gt.get():
            raise ValueError("gt is not required on unlabelled type.")
    return True
