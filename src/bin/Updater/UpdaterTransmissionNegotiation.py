import json
import os


class NegotiationResultInterface:
    def set_passed_negotiation(self, boolean):
        raise NotImplemented()

    def results(self, *args, **kwargs):
        raise NotImplemented()

    def __bool__(self):
        raise NotImplemented()


class TransmissionNegotiationInterface:
    """
    TransmissionNegotiationInterface is a class that gives interfaces for file transfer
    negotiation terms.
    """

    def negotiate(self, transmission_condition):
        raise NotImplemented()

    def create_msg_to_host(self, text):
        raise NotImplemented()


class NegotiationResult(NegotiationResultInterface):
    def __init__(self, dict_results, boolean=False):
        assert isinstance(dict_results, dict)
        self._results = dict_results
        self._passed = boolean

    def set_passed_negotiation(self, boolean):
        self._passed = boolean

    def results(self, *args, **kwargs):
        self._assert_keys(*args)
        return self._get_dict_obj_recursively(self._results, *args)

    def __bool__(self):
        return self._passed

    def _assert_keys(self, *args):
        if args:
            assert len([argument for argument in args
                        if isinstance(argument, str)]) == len(args)

    def _get_dict_obj_recursively(self, current_dict_value, *args):
        if args:
            argument, args = args[0], args[1:]
            return self._get_dict_obj_recursively(current_dict_value[argument], *args)
        else:
            return current_dict_value


class TransmissionNegotiation(TransmissionNegotiationInterface):
    """
    TransmissionNegotiation class establishes a protocol the files are exchanged
    between the computers.
    The protocol is as follows:
    * A client sends a synchronization message, which goes as follows:
        {"SYN": {"filename": _, "filesize": _, "MD5": _}}
        and optionally info parameter may be appended, however it is not required
        {"SYN": {"filename": _, "filesize": _, "MD5": _}, "info": _}
    * A server responds to the synchronization message in the following way:
        {"ACK": {"filename": _, "filesize": _, "MD5": _}}
        The values of filename, filesize and md5 are the same as in SYN request.

        A respond of the server depends on free disk space available. If a disk
        lacks in space the following responds is sent to the client
        {"ACK": -1, "info": error_info}

        error_info describes a possible origin of an error, whose are:
        * 'Could not parse negotiation'
        * 'Not all conditions given'
        * 'Not enough space'

    If the respond of the server is positive, file transmission may begin.
    Data handling is done by other classes.
    """

    SYN = "SYN"
    FILE_NAME = "filename"
    FILE_SIZE = "filesize"
    MD5 = "MD5"
    ACK = "ACK"
    INFO = "info"

    def __init__(self):
        self.trans_cond = {}

    def create_msg_to_host(self, text):
        assert isinstance(text, str)
        msg = {self.INFO: text}
        msg_json = json.dumps(msg)
        return msg_json

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
            return NegotiationResult({self.ACK: self.trans_cond}, True)
        else:
            return self._create_failure_ack_msg("Not enough space")

    def _create_failure_ack_msg(self, error_info):
        return NegotiationResult({self.ACK: -1, self.INFO: error_info}, False)

    def _get_disk_free_space(self):
        statvfs = os.statvfs(os.getcwd())
        # http://pubs.opengroup.org/onlinepubs/009695399/basedefs/sys/statvfs.h.html
        return statvfs.f_bavail * statvfs.f_frsize
