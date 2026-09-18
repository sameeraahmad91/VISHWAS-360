"""Lightweight multilingual intent model used by the chatbot and voice flow.

It is deliberately trained at import time on a small, transparent seed set so the
service works without downloading a large model. Replace the examples with labeled
production conversations when enough data is collected.
"""
from __future__ import annotations
from typing import Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

EXAMPLES = {
    "Electrician": ["light not working", "fan wiring", "बिजली का काम", "switch repair"],
    "Plumber": ["tap leaking", "pipe blockage", "नल में पानी लीक", "bathroom plumbing"],
    "AC Repair": ["ac not cooling", "air conditioner service", "एसी खराब", "gas refill"],
    "Carpenter": ["door repair", "wood furniture", "दरवाजा ठीक करना", "cupboard work"],
    "Painter": ["paint my wall", "घर की पेंटिंग", "putty and whitewash", "wall colour"],
    "Appliance Repair": ["fridge repair", "washing machine broken", "टीवी ठीक करना", "microwave service"],
    "Cleaning": ["deep clean home", "sofa cleaning", "घर की सफाई", "bathroom clean"],
    "Mechanic": ["bike puncture", "car engine problem", "गाड़ी खराब", "battery jumpstart"],
}
URGENT = ("urgent", "emergency", "immediately", "sparking", "flood", "smoke", "gas leak", "तुरंत", "आपात")
_labels, _texts = zip(*[(label, text) for label, values in EXAMPLES.items() for text in values])
_vectorizer = TfidfVectorizer(ngram_range=(1, 2), analyzer="char_wb", min_df=1)
_model = LogisticRegression(max_iter=500, random_state=42).fit(_vectorizer.fit_transform(_texts), _labels)

def classify(text: str) -> dict[str, Any]:
    value = (text or "").strip()
    probabilities = _model.predict_proba(_vectorizer.transform([value]))[0]
    index = int(probabilities.argmax())
    service = str(_model.classes_[index])
    confidence = float(probabilities[index])
    return {"service": service, "confidence": round(confidence, 4), "urgent": any(w in value.lower() for w in URGENT)}
