
class TotoMessage: 
    def __init__(self, timestamp: str, cid: str, id: str, type: str, msg: str, data: dict):
        self.timestamp = timestamp
        self.cid = cid
        self.id = id
        self.type = type
        self.msg = msg
        self.data = data
