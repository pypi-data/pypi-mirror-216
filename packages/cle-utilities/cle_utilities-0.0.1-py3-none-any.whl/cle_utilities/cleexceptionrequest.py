class CleExceptionRequest:
    def __init__(self, header, Category, ExceptionType, Severity, Code, TransactionData, DumpAnalysis, Message = None, MessagesNVP = None, ReplyDestination = None, 
                 ReplayCount = None, DataEncoding = None, MessageHeader = None, SendExactMessage = None, IssueGroup = None):
        self.Header = header
        self.Category = Category
        self.Type = ExceptionType
        self.Severity = Severity
        self.Code = Code
        if Message:
            self.Message = Message
        if MessagesNVP:
            self.MessagesNVP = MessagesNVP
        if ReplyDestination:
            self.ReplyDestination = ReplyDestination
        if ReplayCount:
            self.ReplayCount = ReplayCount
        else:
            self.ReplayCount = "0"
        self.TransactionData = TransactionData
        self.DumpAnalysis = DumpAnalysis
        if DataEncoding:
            self.DataEncoding = DataEncoding
        if MessageHeader:
            self.MessageHeader = MessageHeader
        if SendExactMessage:
            self.SendExactMessage = SendExactMessage
        else:
            self.SendExactMessage = "N"
        if IssueGroup:
            self.IssueGroup = IssueGroup
