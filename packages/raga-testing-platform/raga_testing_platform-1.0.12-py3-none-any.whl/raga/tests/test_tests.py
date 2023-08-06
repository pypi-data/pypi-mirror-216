import os
import unittest
from unittest import mock
import pandas as pd
from raga import TestSession,Dataset,  initialize, model_ab_test, MAX_RETRIES, create_ab_test
from raga.utils.dataset_util import FileUploadError
from raga import Dataset, StringElement, AggregationLevelElement, ModelABTestRules, ModelABTestTypeElement, FloatElement
from unittest.mock import MagicMock, patch, Mock, call
from requests.exceptions import RequestException
import requests

class TestABTestTestCase(unittest.TestCase):

    def setUp(self):
        self.test_session = TestSession("project_name", "run_name", u_test=True)
        self.test_session.project_id = "project_id"
        self.test_session.token = "test_token"
        self.test_session.api_host = "base_url"
        self.dataset_name = "my_dataset"
        self.test_session.experiment_id = "experiment_id"
        self.dataset_creds = None
        self.dataset = Dataset(self.test_session, self.dataset_name, self.dataset_creds, u_test=True)
        self.dataset.dataset_id = "12345"


        self.testName = StringElement("TestName")
        self.modelA = StringElement("modelA")
        self.modelB = StringElement("modelB")
        self.gt = StringElement("GT")
        self.type = ModelABTestTypeElement("unlabelled")
        self.aggregation_level = AggregationLevelElement()
        self.aggregation_level.add(StringElement("weather"))
        self.aggregation_level.add(StringElement("scene"))
        self.aggregation_level.add(StringElement("time_of_day"))
        self.rules = ModelABTestRules()
        self.rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
        self.rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))
        
    def test_initialize_test_case(self):
         # Mock the create_ab_test function
        dataset = MagicMock(spec=Dataset)
        expected_response = {"success": True,
            "message": "Test created successfully",
            "data": {
            "id": "test_is",
            "name": "test_name"
            }
        }

        test_session = MagicMock(spec=TestSession)
        test_session.http_client = MagicMock()
        # Set the return value for http_client.post()
        test_session.http_client.post.return_value = expected_response
        dataset.test_session = test_session
        # Mock the necessary methods and attributes for test_ds and test_session
        dataset.dataset_id = "test_dataset_id"
        dataset.test_session.experiment_id = "test_experiment_id"
        dataset.test_session.token = "test_token"
        
        # Mock the necessary arguments
        testName = MagicMock(spec=StringElement)
        modelA = MagicMock(spec=StringElement)
        modelB = MagicMock(spec=StringElement)
        gt = MagicMock(spec=StringElement)
        filter = MagicMock(spec=StringElement)
        type = MagicMock(spec=ModelABTestTypeElement)
        aggregation_level = MagicMock(spec=AggregationLevelElement)
        rules = MagicMock(spec=ModelABTestRules)
        
        # Patch the create_ab_test functions
        with patch('raga._tests.create_ab_test') as create_ab_test:
            result = initialize(dataset, testName=testName, modelA=modelA, modelB=modelB, gt=gt, type=type, aggregation_level=aggregation_level, rules=rules, filter=filter)
     
            create_ab_test.assert_called_once_with(dataset, testName, modelA, modelB, type, aggregation_level, rules, gt, filter)
        assert result is True

    
    def test_valid_create_ab_test(self):
         # Mock the create_ab_test function
        dataset = MagicMock(spec=Dataset)
        expected_response = {"success": True,
            "message": "Test created successfully",
            "data": {
            "id": "test_is",
            "name": "test_name"
            }
        }

        test_session = MagicMock(spec=TestSession)
        test_session.http_client = MagicMock()
        # Set the return value for http_client.post()
        test_session.http_client.post.return_value = expected_response
        dataset.test_session = test_session
        # Mock the necessary methods and attributes for test_ds and test_session
        dataset.dataset_id = "test_dataset_id"
        dataset.test_session.experiment_id = "test_experiment_id"
        dataset.test_session.token = "test_token"
        
        # Mock the necessary arguments
        testName = MagicMock(spec=StringElement)
        modelA = MagicMock(spec=StringElement)
        modelB = MagicMock(spec=StringElement)
        gt = MagicMock(spec=StringElement)
        filter = MagicMock(spec=StringElement)
        type = MagicMock(spec=ModelABTestTypeElement)
        aggregation_level = MagicMock(spec=AggregationLevelElement)
        rules = MagicMock(spec=ModelABTestRules)

        # Call the method
        create_ab_test_res = create_ab_test(dataset, testName, modelA, modelB, type, aggregation_level, rules, gt, filter)
        
        # Assert the expected experiment ID is returned
        self.assertEqual(create_ab_test_res, expected_response.get('data'))


        
    def test_invalid_create_ab_test(self):
        expected_response = "invalid"
        # Mock the create_ab_test function
        dataset = MagicMock(spec=Dataset)
        test_session = MagicMock(spec=TestSession)
        test_session.http_client = MagicMock()
        # Set the return value for http_client.post()
        test_session.http_client.post.return_value = expected_response
        dataset.test_session = test_session
        # Mock the necessary methods and attributes for test_ds and test_session
        dataset.dataset_id = "test_dataset_id"
        dataset.test_session.experiment_id = "test_experiment_id"
        dataset.test_session.token = "test_token"
        
        # Mock the necessary arguments
        testName = MagicMock(spec=StringElement)
        modelA = MagicMock(spec=StringElement)
        modelB = MagicMock(spec=StringElement)
        gt = MagicMock(spec=StringElement)
        filter = MagicMock(spec=StringElement)
        type = MagicMock(spec=ModelABTestTypeElement)
        aggregation_level = MagicMock(spec=AggregationLevelElement)
        rules = MagicMock(spec=ModelABTestRules)


        # Call the method and assert it raises a KeyError
        with self.assertRaises(ValueError) as context:
            create_ab_test(dataset, testName, modelA, modelB, type, aggregation_level, rules, gt, filter)
            self.assertEqual(context.exception, "Invalid response data. Expected a dictionary.")
                

    def test_invalid_test_ds_parameter(self):
        testName = StringElement("TestName")
        modelA = StringElement("modelA")
        modelB = StringElement("modelB")
        gt = StringElement("GT")
        type = ModelABTestTypeElement("unlabelled")
        aggregation_level = AggregationLevelElement()
        aggregation_level.add(StringElement("weather"))
        aggregation_level.add(StringElement("scene"))
        aggregation_level.add(StringElement("time_of_day"))
        rules = ModelABTestRules()
        rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
        rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

        with self.assertRaises(AssertionError) as context:
            initialize("invalid_test_ds", testName, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), "test_ds must be an instance of the Dataset class.") 

    def test_missing_test_name_parameter(self):
        
        testName = StringElement("")
        modelA = StringElement("ModelA")
        modelB = StringElement("modelB")
        gt = StringElement("GT")
        type = ModelABTestTypeElement("unlabelled")
        aggregation_level = AggregationLevelElement()
        aggregation_level.add(StringElement("weather"))
        aggregation_level.add(StringElement("scene"))
        aggregation_level.add(StringElement("time_of_day"))
        rules = ModelABTestRules()
        rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
        rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

        with self.assertRaises(AssertionError) as context:
            initialize(self.dataset, testName, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), 'testName is required and must be an instance of the StringElement class.')

    def test_missing_model_a_parameter(self):
        testName = StringElement("TestName")
        modelA = StringElement("")
        modelB = StringElement("modelB")
        gt = StringElement("GT")
        type = ModelABTestTypeElement("unlabelled")
        aggregation_level = AggregationLevelElement()
        aggregation_level.add(StringElement("weather"))
        aggregation_level.add(StringElement("scene"))
        aggregation_level.add(StringElement("time_of_day"))
        rules = ModelABTestRules()
        rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
        rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

        with self.assertRaises(AssertionError) as context:
            initialize(self.dataset, testName, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), 'modelA is required and must be an instance of the StringElement class.')

    def test_missing_model_b_parameter(self):
        testName = StringElement("TestName")
        modelA = StringElement("modelA")
        modelB = StringElement("")
        gt = StringElement("GT")
        type = ModelABTestTypeElement("unlabelled")
        aggregation_level = AggregationLevelElement()
        aggregation_level.add(StringElement("weather"))
        aggregation_level.add(StringElement("scene"))
        aggregation_level.add(StringElement("time_of_day"))
        rules = ModelABTestRules()
        rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
        rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

        with self.assertRaises(AssertionError) as context:
            initialize(self.dataset, testName, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), 'modelB is required and must be an instance of the StringElement class.')



    def test_missing_aggregation_level_parameter(self):
        testName = StringElement("TestName")
        modelA = StringElement("modelA")
        modelB = StringElement("modelB")
        gt = StringElement("GT")
        type = ModelABTestTypeElement("unlabelled")
        aggregation_level = AggregationLevelElement()
        rules = ModelABTestRules()
        rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
        rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

        with self.assertRaises(AssertionError) as context:
            initialize(self.dataset, testName, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), "aggregation_level is required and must be an instance of the AggregationLevelElement class.")

    def test_invalid_aggregation_level_data_type(self):
        testName = StringElement("TestName")
        modelA = StringElement("modelA")
        modelB = StringElement("modelB")
        gt = StringElement("GT")
        type = ModelABTestTypeElement("unlabelled")
        aggregation_level = "invalid"
        rules = ModelABTestRules()
        rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
        rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

        with self.assertRaises(AssertionError) as context:
            initialize(self.dataset, testName, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), "aggregation_level is required and must be an instance of the AggregationLevelElement class.")

    def test_missing_rules_parameter(self):
        testName = StringElement("TestName")
        modelA = StringElement("modelA")
        modelB = StringElement("modelB")
        gt = StringElement("GT")
        type = ModelABTestTypeElement("unlabelled")
        aggregation_level = AggregationLevelElement()
        aggregation_level.add(StringElement("weather"))
        aggregation_level.add(StringElement("scene"))
        aggregation_level.add(StringElement("time_of_day"))
        rules = ModelABTestRules()

        with self.assertRaises(AssertionError) as context:
            initialize(self.dataset, testName, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), "rules is required and must be an instance of the ModelABTestRules class.")

    def test_invalid_rules_data_type(self):
        testName = StringElement("TestName")
        modelA = StringElement("modelA")
        modelB = StringElement("modelB")
        gt = StringElement("GT")
        type = ModelABTestTypeElement("unlabelled")
        aggregation_level = AggregationLevelElement()
        aggregation_level.add(StringElement("weather"))
        aggregation_level.add(StringElement("scene"))
        aggregation_level.add(StringElement("time_of_day"))
        rules = "invalid"

        with self.assertRaises(AssertionError) as context:
            initialize(self.dataset, testName, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), "rules is required and must be an instance of the ModelABTestRules class.")

    def test_missing_gt_on_labelled_type(self):
        testName = StringElement("TestName")
        modelA = StringElement("modelA")
        modelB = StringElement("modelB")
        gt = StringElement("")
        type = ModelABTestTypeElement("labelled")
        aggregation_level = AggregationLevelElement()
        aggregation_level.add(StringElement("weather"))
        aggregation_level.add(StringElement("scene"))
        aggregation_level.add(StringElement("time_of_day"))
        rules = ModelABTestRules()
        rules.add(metric = StringElement("precision_diff"), IoU = FloatElement(0.5), _class = StringElement("all"), threshold = FloatElement(0.05))
        rules.add(metric = StringElement("‘difference_count’"), IoU = FloatElement(0.5), _class = StringElement("‘vehicle’"), threshold = FloatElement(0.05))

        with self.assertRaises(AssertionError) as context:
            initialize(self.dataset, testName, modelA, modelB, type, aggregation_level, rules, gt)
        self.assertEqual(str(context.exception), f"gt is required on labelled type and must be an instance of the StringElement class.")
        
    @mock.patch('sys.exit')
    def test_model_ab_test_network_error(self, mock_exit):
        mock_initialize = MagicMock(side_effect=requests.exceptions.RequestException("Network error"))
        mock_create_ab_test = MagicMock(side_effect=requests.exceptions.RequestException("Network error"))

        with mock.patch('raga._tests.initialize', side_effect=mock_initialize), \
                mock.patch('raga._tests.create_ab_test', side_effect=mock_create_ab_test), \
                mock.patch('builtins.print') as mock_print:
            # Set up test input parameters
            testName = StringElement("TestName")
            modelA = StringElement("modelA")
            modelB = StringElement("modelB")
            gt = StringElement("Ground Truth")
            test_type = ModelABTestTypeElement("labelled")
            aggregation_level = AggregationLevelElement()
            aggregation_level.add(StringElement("weather"))
            aggregation_level.add(StringElement("scene"))
            aggregation_level.add(StringElement("time_of_day"))
            rules = ModelABTestRules()
            rules.add(metric=StringElement("precision_diff"), IoU=FloatElement(0.5), _class=StringElement("all"), threshold=FloatElement(0.05))
            rules.add(metric=StringElement("difference_count"), IoU=FloatElement(0.5), _class=StringElement("vehicle"), threshold=FloatElement(0.05))

            # Set the MAX_RETRIES to 3 for testing
            MAX_RETRIES = 3

            # Call the method
            model_ab_test(
                self.dataset, testName=testName, modelA=modelA, modelB=modelB, gt=gt, 
                type=test_type, aggregation_level=aggregation_level, rules=rules
            )

            # Assert the expected prints and retries
            expected_calls = [
                mock.call('Network error occurred: Network error'),
                mock.call('Retrying in 1 second(s)...'),
                mock.call('Network error occurred: Network error'),
                mock.call('Retrying in 2 second(s)...'),
                mock.call('Network error occurred: Network error')
            ]
            mock_print.assert_has_calls(expected_calls)
            self.assertEqual(mock_print.call_count, len(expected_calls))
            self.assertEqual(mock_initialize.call_count, MAX_RETRIES)
            mock_exit.assert_not_called()

    def test_model_ab_test_key_error(self):
        mock_initialize = mock.MagicMock()
        mock_initialize.side_effect = KeyError("Key error")
        mock_create_ab_test = mock.MagicMock()

        with mock.patch('raga.initialize', side_effect=mock_initialize), \
                mock.patch('raga.create_ab_test', side_effect=mock_create_ab_test), \
                mock.patch('builtins.print') as mock_print, \
                self.assertRaises(SystemExit) as cm:
            # Set up test input parameters
            testName = StringElement("TestName")
            modelA = StringElement("modelA")
            modelB = StringElement("modelB")
            gt = StringElement("Ground Truth")
            test_type = ModelABTestTypeElement("labelled")
            aggregation_level = AggregationLevelElement()
            aggregation_level.add(StringElement("weather"))
            aggregation_level.add(StringElement("scene"))
            aggregation_level.add(StringElement("time_of_day"))
            rules = ModelABTestRules()
            rules.add(metric=StringElement("precision_diff"), IoU=FloatElement(0.5), _class=StringElement("all"), threshold=FloatElement(0.05))
            rules.add(metric=StringElement("difference_count"), IoU=FloatElement(0.5), _class=StringElement("vehicle"), threshold=FloatElement(0.05))

            # Call the method
            model_ab_test(
                self.dataset, testName=testName, modelA=modelA, modelB=modelB, gt=gt, 
                type=test_type, aggregation_level=aggregation_level, rules=rules
            )

            # Assert the expected prints and retries
            mock_initialize.assert_called_once()
            mock_create_ab_test.assert_not_called()
            mock_print.assert_called_with('Key error occurred: Key error')
            self.assertEqual(cm.exception.code, 1)

    def test_model_ab_test_value_error(self):
        mock_initialize = mock.MagicMock()
        mock_initialize.side_effect = ValueError("Value error")
        mock_create_ab_test = mock.MagicMock()

        with mock.patch('raga.initialize', side_effect=mock_initialize), \
                mock.patch('raga.create_ab_test', side_effect=mock_create_ab_test), \
                mock.patch('builtins.print') as mock_print, \
                self.assertRaises(SystemExit) as cm:
            # Set up test input parameters
            # ...

            # Call the method
            model_ab_test(
                self.dataset, testName=self.testName, modelA=self.modelA, modelB=self.modelB, gt=self.gt, 
                type=self.type, aggregation_level=self.aggregation_level, rules=self.rules
            )

            # Assert the expected prints and retries
            # ...

            mock_initialize.assert_called_once()
            mock_create_ab_test.assert_not_called()
            mock_print.assert_called_with('Value error occurred: Value error')
            self.assertEqual(cm.exception.code, 1)

    def test_model_ab_test_unexpected_error(self):
        mock_initialize = mock.MagicMock()
        mock_initialize.side_effect = Exception("Unexpected error")
        mock_create_ab_test = mock.MagicMock()

        with mock.patch('raga.initialize', side_effect=mock_initialize), \
                mock.patch('raga.create_ab_test', side_effect=mock_create_ab_test), \
                mock.patch('builtins.print') as mock_print, \
                self.assertRaises(SystemExit) as cm:
            # Set up test input parameters
            # ...

            # Call the method
            model_ab_test(
                self.dataset, testName=self.testName, modelA=self.modelA, modelB=self.modelB, gt=self.gt, 
                type=self.type, aggregation_level=self.aggregation_level, rules=self.rules
            )

            # Assert the expected prints and retries
            # ...

            mock_initialize.assert_called_once()
            mock_create_ab_test.assert_not_called()
            mock_print.assert_called_with('An unexpected error occurred: Unexpected error')
            self.assertEqual(cm.exception.code, 1)


    

if __name__ == "__main__":
    unittest.main()



