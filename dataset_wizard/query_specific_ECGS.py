import re
from settings import load_initial_200_ECGs


class Query:
    """
    Checks either the example of ECG from dataset fits a condition on
    heart rate, diagnosis absence|presence, etc.
    """
    def __init__(self, binary_features_names={},
                 diagnosys_names={},
                 HR_from=None,
                 HR_to=None,
                 substrs=[],
                 unwanted_substrs=[]):
        """
        :param binary_features_names: posiible binary features are ["isSinusRythm", "isRegularRhythm", "isNormalElectricalAxis"]
        diagnosys_names examples are "regular_normosystole", "left_ventricular_hypertrophy",...
        :param diagnosys_names:  dict with pairs (name_of_diagnosis and true|false)
        :param HR_from: lowest possible heart rate
        :param HR_to: biggest possible heart rate
        :param substrs: list of strings to find in doctor's description of an ECG
        """
        self.binary_features_names = binary_features_names
        self.diagnosys_names = diagnosys_names
        self.heart_rate_from = HR_from
        self.heart_rate_to = HR_to
        self.substrs=substrs
        self.unwanted_substrs=unwanted_substrs

    def is_query_ok(self, ecg_node):
        res = self.is_binarys_ok(ecg_node) \
              and self.is_diagnosis_ok(ecg_node) \
              and self.is_heart_rate_ok(ecg_node) \
              and self.contains_all_substrs(ecg_node) \
              and self.unwanted_substrs_ok(ecg_node)
        return res

    def contains_all_substrs(self, ecg_node):
        for substr in self.substrs:
            if not re.search(pattern=substr,string=ecg_node["TextDiagnosisDoc"], flags=re.IGNORECASE):
                return False
        return True

    def unwanted_substrs_ok(self, ecg_node):
        for substr in self.unwanted_substrs:
            if re.search(pattern=substr,string=ecg_node["TextDiagnosisDoc"], flags=re.IGNORECASE):
                return False
        return True

    def is_heart_rate_ok(self, ecg_node):
        HR = int(ecg_node["HeartRate"])
        if self.heart_rate_from is not None:
            if HR < self.heart_rate_from:
                return False
        if self.heart_rate_to is not None:
            if HR > self.heart_rate_to:
                return False
        return True

    def is_binarys_ok(self, ecg_node):
        for binary_feature_name in self.binary_features_names.keys():
            wanted_flag = self.binary_features_names[binary_feature_name]
            real_flag = ecg_node[binary_feature_name]
            if real_flag != wanted_flag:
                return False
        return True

    def is_diagnosis_ok(self, ecg_node):
        for diag_name in self.diagnosys_names.keys():
            wanted_flag = self.diagnosys_names[diag_name]
            real_flag = ecg_node["StructuredDiagnosisDoc"][diag_name]
            if real_flag != wanted_flag:
                return False
        return True