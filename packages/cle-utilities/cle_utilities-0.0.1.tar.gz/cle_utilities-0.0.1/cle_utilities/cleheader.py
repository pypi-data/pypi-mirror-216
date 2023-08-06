import json


class CleHeader:
    def __init__(self, ApplicationID, ServiceName, ComponentName, Timestamp, TransactionDomain, TransactionType,
                 TransactionID, Hostname, BusinessID, ApplicationDomain, BusinessID2=None):
        self.ApplicationID = ApplicationID
        self.ServiceName = ServiceName
        self.ComponentName = ComponentName
        self.Hostname = Hostname
        self.Timestamp = Timestamp
        self.TransactionDomain = TransactionDomain
        self.TransactionType = TransactionType
        self.TransactionID = TransactionID
        self.BusinessID = BusinessID
        self.ApplicationDomain = ApplicationDomain
        if BusinessID2:
            self.BusinessID2 = BusinessID2

    def __str__(self):
        return json.dumps(self.__dict__)
