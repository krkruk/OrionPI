import json
import os


class TransmissionNegotiationAbstract:
    SYN = "SYN"
    FILE_NAME = "filename"
    FILE_SIZE = "filesize"
    MD5 = "MD5"
    ACK = "ACK"
    ERROR_INFO = "error_info"

    def negotiate(self, transmission_condition):
        raise NotImplemented()


class TransmissionNegotiation(TransmissionNegotiationAbstract):
    def __init__(self):
        self.trans_cond = {}
        self.ack_msg = {}

    def negotiate(self, transmission_condition):
        self.trans_cond = transmission_condition
        try:
            self.trans_cond = self._convert_transmission_cond_to_dict()
            self._get_bare_transmission_condition()
        except (TypeError, KeyError):
            return self._create_failure_ack_msg("Could not parse negotiation")

        return self._create_ack_msg() \
            if self._has_all_transmission_parameters() \
            else self._create_failure_ack_msg("Not all conditions given")

    def _convert_transmission_cond_to_dict(self):
        if isinstance(self.trans_cond, dict):
            return self.trans_cond
        elif isinstance(self.trans_cond, str):
            try:
                return json.loads(self.trans_cond)
            except json.JSONDecodeError:
                raise TypeError()
        else:
            raise TypeError()

    def _get_bare_transmission_condition(self):
        bare = self.trans_cond.get(self.SYN)
        if not bare:
            raise KeyError("No SYN command in TransmissionNegotiation")
        self.trans_cond = bare

    def _has_all_transmission_parameters(self):
        trans_cond_keys = set(self.trans_cond.keys())
        all_keys = set([self.FILE_NAME, self.FILE_SIZE, self.MD5])
        return trans_cond_keys == all_keys

    def _create_ack_msg(self):
        free_space = self._get_disk_free_space()
        if free_space > self.trans_cond[self.FILE_SIZE]:
            return {self.ACK: self.trans_cond}
        else:
            return self._create_failure_ack_msg("Not enough space")

    def _create_failure_ack_msg(self, error_info):
        return {self.ACK: -1, self.ERROR_INFO: error_info}

    def _get_disk_free_space(self):
        statvfs = os.statvfs(os.getcwd())
        # http://pubs.opengroup.org/onlinepubs/009695399/basedefs/sys/statvfs.h.html
        return statvfs.f_bavail * statvfs.f_frsize
