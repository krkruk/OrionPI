from bin.Updater.UpdaterTransmissionNegotiation import *
import unittest
import json


class TestUpdaterTransmissionNegotiation(unittest.TestCase):
    def setUp(self):
        self.positive_sync_dict = {
            "SYN": {
                "filename": "update.zip",
                "filesize": 2000,
                "MD5": "5d41402abc4b2a76b9719d911017c592"
            }
        }
        self.positive_ack_dict = {
            "ACK": {
                "filename": "update.zip",
                "filesize": 2000,
                "MD5": "5d41402abc4b2a76b9719d911017c592"
            }
        }
        self.erroneous_sync_dict = {
            "SYNC": {
                "filename": "update.zip",
                "filesize": 2000,
                "MD5": "5d41402abc4b2a76b9719d911017c592"
            }
        }
        self.positive_sync_json = json.dumps(self.positive_sync_dict)
        self.positive_ack_json = json.dumps(self.positive_ack_dict)
        self.erroneous_sync_json = json.dumps(self.erroneous_sync_dict)
        self.erroneous_sync_json = self.erroneous_sync_json[2:]
        self.sync_not_all_values_passed_dict = self.positive_sync_dict.copy()

    def test_negotiate_positive_syn_ack_dict(self):
        negotiator = TransmissionNegotiation()
        ack = negotiator.negotiate(self.positive_sync_dict)
        self.assertDictEqual(self.positive_ack_dict, ack)

    def test_negotiate_erroneous_syn_ack_dict(self):
        negotiator = TransmissionNegotiation()
        ack = negotiator.negotiate(self.erroneous_sync_dict)
        self.assertEqual(-1, ack["ACK"])

    def test_negotiatie_erroneous_syn_ack_not_all_values_passed(self):
        negotiator = TransmissionNegotiation()
        del self.sync_not_all_values_passed_dict["SYN"]["filesize"]
        ack = negotiator.negotiate(self.sync_not_all_values_passed_dict)
        self.assertEqual(-1, ack["ACK"])

    def test_get_bare_transmission_condition_given_correct_data(self):
        negotiator = TransmissionNegotiation()
        negotiator.trans_cond = self.positive_sync_dict
        expected_bare = self.positive_sync_dict["SYN"]
        negotiator._get_bare_transmission_condition()
        self.assertDictEqual(expected_bare, negotiator.trans_cond)

    def test_get_bare_transmission_cond_given_erroneous_sync_data(self):
        negotiator = TransmissionNegotiation()
        negotiator.trans_cond = self.erroneous_sync_dict
        self.assertRaises(KeyError, negotiator._get_bare_transmission_condition)

    def test_has_all_transmission_parameters_expect_true(self):
        negotiator = TransmissionNegotiation()
        negotiator.trans_cond = self.positive_sync_dict
        negotiator._get_bare_transmission_condition()
        self.assertTrue(negotiator._has_all_transmission_parameters())

    def test_has_all_transmission_parameters_not_all_values_passed_expect_false(self):
        negotiator = TransmissionNegotiation()
        negotiator.trans_cond = self.positive_sync_dict
        negotiator._get_bare_transmission_condition()
        del negotiator.trans_cond[TransmissionNegotiation.FILE_NAME]
        self.assertFalse(negotiator._has_all_transmission_parameters())

    def test_convert_transmission_cond_to_dict_on_erroneous_json(self):
        negotiator = TransmissionNegotiation()
        negotiator.trans_cond = self.erroneous_sync_json
        self.assertRaises(TypeError, negotiator._convert_transmission_cond_to_dict)


if __name__ == "__main__":
    unittest.main()
