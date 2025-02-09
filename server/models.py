from pydantic import BaseModel
from typing import List

class HarmfulContent(BaseModel):
    is_present: bool
    confidence: float
    category: str
    reasons: List[str]
    where_in_content: List[str]

class AIGenerated(BaseModel):
    is_present: bool
    confidence: float
    reasons: List[str]
    characteristics: List[str]  
    where_in_content: List[str]

class ScamLikelihood(BaseModel):
    is_scam: bool
    confidence: float
    reasons: List[str]
    signs: List[str]
    where_in_content: List[str]

class WebsiteAnalysis(BaseModel):
    harmful_content: HarmfulContent
    ai_generated: AIGenerated
    scam_likelihood: ScamLikelihood
