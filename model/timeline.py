
from dataclasses import dataclass
from typing import List


@dataclass
class TimelineDate: 
    
    date: str
    events: List[str]
    
    def __init__(self, date: str, events: List[str]): 
        self.date = date
        self.events = events
        
    def to_bson(self, topic_code: str): 
        return {
            'topicCode': topic_code, 
            'date': self.date, 
            'events': self.events
        }
    
@dataclass
class Timeline: 
    
    dates: List[TimelineDate] 
    
    def __init__(self, dates: List[TimelineDate]): 
        self.dates = dates
    
    def to_bson(self, topic_code: str): 
        return [ date.to_bson(topic_code) for date in self.dates ]