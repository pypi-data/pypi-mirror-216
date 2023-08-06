import json
from typing import Optional
from raga import Dataset, StringElement, AggregationLevelElement, ModelABTestRules, ModelABTestTypeElement
import sys
import time
import requests
import random

MAX_RETRIES = 3


def model_ab_test(test_ds: Dataset, testName: StringElement, modelA: StringElement, modelB: StringElement,
                  type: ModelABTestTypeElement, aggregation_level: AggregationLevelElement, rules: ModelABTestRules,
                  gt: Optional[StringElement] = StringElement(""), filter: Optional[StringElement] = StringElement("")):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            initialize(test_ds, testName, modelA, modelB, type, aggregation_level, rules, gt, filter)
            break  # Exit the loop if initialization succeeds
        except requests.exceptions.RequestException as e:
            print(f"Network error occurred: {str(e)}")
            retries += 1
            if retries < MAX_RETRIES:
                print(f"Retrying in {retries} second(s)...")
                time.sleep(retries)
        except KeyError as e:
            print(f"Key error occurred: {str(e)}")
            sys.exit()  # No need to retry if a KeyError occurs
        except ValueError as e:
            print(f"Value error occurred: {str(e)}")
            sys.exit()  # No need to retry if a ValueError occurs
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            sys.exit()  # No need to retry if an unexpected error occurs


def initialize(test_ds: Dataset, testName: StringElement, modelA: StringElement, modelB: StringElement,
               type: ModelABTestTypeElement, aggregation_level: AggregationLevelElement, rules: ModelABTestRules,
               gt: Optional[StringElement] = StringElement(""), filter: Optional[StringElement] = StringElement("")):
    validation(test_ds, testName, modelA, modelB, type, aggregation_level, rules, gt)
    create_ab_test(test_ds, testName, modelA, modelB, type, aggregation_level, rules, gt, filter)
    return True


def create_ab_test(test_ds: Dataset, testName: StringElement, modelA: StringElement, modelB: StringElement,
                   type: ModelABTestTypeElement, aggregation_level: AggregationLevelElement, rules: ModelABTestRules,
                   gt: Optional[StringElement] = StringElement(""), filter: Optional[StringElement] = StringElement("")):
    payload = {
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

    res_data = test_ds.test_session.http_client.post("api/experiment/test", data=payload,headers={"Authorization": f'Bearer {test_ds.test_session.token}'})

    if not isinstance(res_data, dict):
        raise ValueError("Invalid response data. Expected a dictionary.")

    return res_data.get("data")


def validation(test_ds: Dataset, testName: StringElement, modelA: StringElement, modelB: StringElement,
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

    return True
