class CleLogRequest:
    def __init__(self, header, LogLevel, TimeDuration=None, Category=None, Messages=None, Status=None,
                 TransactionBefore=None, TransactionAfter=None, DataEncoding=None):
        self.Header = header
        if TimeDuration:
            self.TimeDuration = TimeDuration
        if Category:
            self.Category = Category
        if Messages:
            self.Messages = Messages
        if Status:
            self.Status = Status
        if TransactionBefore:
            self.TransactionBefore = TransactionBefore
        if TransactionAfter:
            self.TransactionAfter = TransactionAfter
        self.LogLevel = LogLevel
        if DataEncoding:
            self.DataEncoding = DataEncoding
