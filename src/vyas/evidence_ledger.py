"""Evidence Ledger & Contradiction Scoring Engine (Phase D).

Operating Standard: Classical Jyotish Evidence-Based Synthesis.
Guards against:
1. Double-counting correlated planetary/house indicators.
2. Promoting C3 without Natal Promise, Varga confirmation, and Dasha lord dignity.
3. Ignoring severe afflictions, combustion, or dusthana placement.
4. Arbitrary fake probability percentages (e.g. 75-96%).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

@dataclass
class EvidenceItem:
    source_system: str       # 'Parashari', 'KP', 'Jaimini', 'Gochar', 'Ashtakavarga', 'Shodashvarga'
    subject: str             # Planet or House or Dasha
    raw_fact: str            # Calculated fact (e.g., '10th Lord Saturn Exalted in 7H')
    interpretation: str      # Meaning for domain
    polarity: str            # 'Support', 'Obstruction', 'Neutral'
    weight: float            # 0.5 to 2.0
    dependency_group: str    # Grouping to prevent double counting (e.g., 'Saturn_Exalted')
    rule_id: str             # e.g., 'BPHS_10H_LORD_EXALTED'
    citation: str = ""       # e.g., 'BPHS ch. 24'


@dataclass
class DomainJudgment:
    domain: str
    tier: str                # 'C3', 'C2', 'C1'
    badge: str               # Full display badge
    verdict: str             # Headline conclusion
    detailed_synthesis: str  # Comprehensive Jyotishi synthesis
    supporting_evidence: List[str]
    weakening_evidence: List[str]
    contradictions: List[str]
    timing_window: str
    evidence_score: float
    is_natal_promised: bool
    dasha_aligned: bool
    varga_confirmed: bool
    transit_triggered: bool
    disclaimer: str = (
        "ज्योतिषीय मार्गदर्शन वैदिक ग्रह-स्थिति एवं काल-चक्र पर आधारित सांकेतिक विश्लेषण है। "
        "यह किसी भी प्रकार की निश्चितता या गारंटी का दावा नहीं करता; मानव पुरुषार्थ, विवेक एवं सत्कर्म सर्वोपरि हैं।"
    )


class EvidenceLedger:
    """Manages an audit-trailed ledger of astrological evidence for a domain query."""

    def __init__(self, domain_name: str):
        self.domain_name = domain_name
        self.items: List[EvidenceItem] = []
        self._seen_groups: Set[str] = set()

    def add_evidence(
        self,
        source_system: str,
        subject: str,
        raw_fact: str,
        interpretation: str,
        polarity: str,
        weight: float,
        dependency_group: str,
        rule_id: str,
        citation: str = ""
    ) -> None:
        """Add an evidence item to the ledger with deduplication protection."""
        item = EvidenceItem(
            source_system=source_system,
            subject=subject,
            raw_fact=raw_fact,
            interpretation=interpretation,
            polarity=polarity,
            weight=weight,
            dependency_group=dependency_group,
            rule_id=rule_id,
            citation=citation
        )
        self.items.append(item)

    def evaluate_convergence(
        self,
        is_natal_promised: bool,
        dasha_aligned: bool,
        varga_confirmed: bool,
        transit_triggered: bool,
        birth_time_confidence: str = "High",
        boundary_warning: bool = False
    ) -> DomainJudgment:
        """Evaluates convergence grade (C1, C2, C3) strictly from evidence ledger."""
        supporting: List[str] = []
        weakening: List[str] = []
        contradictions: List[str] = []

        grouped_support: Dict[str, float] = {}
        grouped_obstruction: Dict[str, float] = {}

        for item in self.items:
            desc = f"[{item.source_system}] {item.raw_fact}: {item.interpretation}"
            if item.polarity == "Support":
                supporting.append(desc)
                # Cap contribution from same dependency group to prevent double-counting
                cur_w = grouped_support.get(item.dependency_group, 0.0)
                grouped_support[item.dependency_group] = max(cur_w, item.weight)
            elif item.polarity == "Obstruction":
                weakening.append(desc)
                cur_w = grouped_obstruction.get(item.dependency_group, 0.0)
                grouped_obstruction[item.dependency_group] = max(cur_w, item.weight)
            elif item.polarity == "Contradiction":
                contradictions.append(desc)

        total_pos = sum(grouped_support.values())
        total_neg = sum(grouped_obstruction.values())
        net_score = round(total_pos - total_neg, 2)

        # Contradiction flag
        has_major_contradiction = (total_neg >= 1.5) or (len(contradictions) > 0)
        if not is_natal_promised and (dasha_aligned or transit_triggered):
            contradictions.append("दशा या गोचर सक्रिय है किन्तु जन्म कुण्डली में मूल शास्त्रीय प्रतिज्ञा (Natal Promise) दुर्बल अथवा अनुपस्थित है।")
            has_major_contradiction = True

        # Determine Tier
        # Rule for C3 (Triple Convergence):
        # 1. Natal Promise must be True
        # 2. Dasha must be Aligned
        # 3. Varga confirmation must be True
        # 4. Transit trigger must be True
        # 5. No major unresolved contradiction
        # 6. Birth time confidence must be High and not on boundary
        if (
            is_natal_promised
            and dasha_aligned
            and varga_confirmed
            and transit_triggered
            and not has_major_contradiction
            and birth_time_confidence == "High"
            and not boundary_warning
        ):
            tier = "C3"
            badge = "🔴 [C3] त्रि-संयोग सिद्ध (Triple Convergence)"
            verdict = "सशक्त अनुकूलता एवं कार्य सिद्धि का योग (Highly Favourable Window)"
            synthesis = (
                f"{self.domain_name} के संदर्भ में जन्म कुण्डली की मूल प्रतिज्ञा, सक्रिय विंशोत्तरी दशा, "
                f"संबंधित वर्ग चार्ट एवं गोचर चारों स्वतंत्र शास्त्रीय घटक एक साथ संरेखित हैं। "
                f"इस समयावधि में सतत कर्म संरेखण एवं विवेकपूर्ण निर्णयों से अभीष्ट सिद्धि की प्रबल संभावना बनती है।"
            )
        elif (is_natal_promised and (dasha_aligned or transit_triggered)) and not (total_neg > total_pos):
            tier = "C2"
            badge = "🟡 [C2] द्वि-संयोग प्रवृत्त (Double Convergence / Conditional)"
            verdict = "प्रयास एवं धैर्य सापेक्ष प्रगति (Progress Dependent on Focused Effort)"
            synthesis = (
                f"{self.domain_name} के क्षेत्र में कुछ प्रमुख शास्त्रीय कारक अनुकूल हैं, यद्यपि पूर्ण फलीभूत "
                f"होने हेतु कुछ अवरोधक घटकों या ग्रह स्थिति के अनुरूप संयम एवं सुनियोजित पुरुषार्थ अपेक्षित है।"
            )
        else:
            tier = "C1"
            badge = "🟠 [C1] एकल संकेत / आधार सुदृढ़ीकरण काल (Single Indicator / Caution)"
            verdict = "सतर्कता, धैर्य एवं आंतरिक संतुलन अपेक्षित (Consolidation & Caution)"
            synthesis = (
                f"वर्तमान कालखंड में {self.domain_name} हेतु तात्कालिक बड़े जोखिम से बचना श्रेयस्कर है। "
                f"यह समय नवीन योजनाओं की सुदृढ़ आधारशिला रखने एवं शास्त्रीय उपायों द्वारा ऊर्जा संतुलन का है।"
            )

        return DomainJudgment(
            domain=self.domain_name,
            tier=tier,
            badge=badge,
            verdict=verdict,
            detailed_synthesis=synthesis,
            supporting_evidence=supporting,
            weakening_evidence=weakening,
            contradictions=contradictions,
            timing_window="सक्रिय दशा एवं अनुकूल गोचर संचरण के मध्य",
            evidence_score=net_score,
            is_natal_promised=is_natal_promised,
            dasha_aligned=dasha_aligned,
            varga_confirmed=varga_confirmed,
            transit_triggered=transit_triggered
        )
