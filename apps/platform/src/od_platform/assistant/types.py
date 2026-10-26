# apps/platform/src/od_platform/assistant/types.py
from pydantic import BaseModel
from typing import Dict, List

class HighRiskEvent(BaseModel):
    time_sec: int
    object: str
    confidence: float

class Statistics(BaseModel):
    analyzed_frames: int
    object_counts: Dict[str, int]
    high_risk_events: List[HighRiskEvent]

class AssistantReport(BaseModel):
    """智能助手返回的标准化报告对象"""
    video_name: str
    statistics: Statistics
    llm_interpretation: str