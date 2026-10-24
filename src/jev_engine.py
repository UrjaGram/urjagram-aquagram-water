"""
TypeSafe Jev System-One Decision Classifier & Deterministic Safety Guardrails.
Implements the UrjaGram architecture pattern:
"A language model writes, Jev decides, code acts."
"""

from enum import Enum
from typing import Dict, Any, Tuple
from .config import (
    SAFE_WATER_TABLE_MAX_MBGL,
    ADVISORY_WATER_TABLE_MBGL,
    WARNING_WATER_TABLE_MBGL,
    CRITICAL_EMERGENCY_MBGL
)

class AlertLevel(str, Enum):
    NORMAL = "LEVEL_0_NORMAL"
    ADVISORY = "LEVEL_1_ADVISORY"
    WARNING = "LEVEL_2_WARNING"
    EMERGENCY = "LEVEL_3_EMERGENCY"

class ActionDirective(str, Enum):
    OPTIMAL_IRRIGATION = "PERMIT_FULL_SCHEDULED_IRRIGATION"
    SCHEDULE_ALTERATION = "PROMOTE_NIGHT_IRRIGATION_AND_ALTERNATE_FURROWS"
    MANDATORY_MICRO_IRRIGATION = "RESTRICT_TO_DRIP_SPRINKLER_ONLY_CAP_PUMPING_4_HRS"
    CRITICAL_OVERDRAFT_HALT = "PROHIBIT_FLOOD_IRRIGATION_RESERVE_AQUIFER_FOR_DRINKING"

class JevDecisionEngine:
    """
    Jev System-One deterministic classification engine.
    Maps continuous multi-dimensional hydro-soil feature vectors to discrete operational choices.
    """
    
    @staticmethod
    def classify_status(
        water_table_mbgl: float,
        days_of_water_left: float,
        consecutive_dry_days: int
    ) -> AlertLevel:
        """
        Fast deterministic classifier simulating Jev System-One scoring:
        Evaluates risk score across three dimensions:
        1. Depth to water table
        2. Projected runout days
        3. Prolonged dry spells
        """
        risk_score = 0
        
        # Dimension 1: Water table depth
        if water_table_mbgl >= CRITICAL_EMERGENCY_MBGL:
            risk_score += 4
        elif water_table_mbgl >= WARNING_WATER_TABLE_MBGL:
            risk_score += 3
        elif water_table_mbgl >= ADVISORY_WATER_TABLE_MBGL:
            risk_score += 2
        elif water_table_mbgl > SAFE_WATER_TABLE_MAX_MBGL:
            risk_score += 1

        # Dimension 2: Days of water remaining
        if days_of_water_left < 15.0:
            risk_score += 4
        elif days_of_water_left < 30.0:
            risk_score += 3
        elif days_of_water_left < 60.0:
            risk_score += 1

        # Dimension 3: Dry spell intensity
        if consecutive_dry_days >= 21:
            risk_score += 2
        elif consecutive_dry_days >= 14:
            risk_score += 1

        # Classify based on consolidated score
        if risk_score >= 7:
            return AlertLevel.EMERGENCY
        elif risk_score >= 4:
            return AlertLevel.WARNING
        elif risk_score >= 2:
            return AlertLevel.ADVISORY
        else:
            return AlertLevel.NORMAL

    @staticmethod
    def enforce_hard_safety_guardrails(
        jev_decision: AlertLevel,
        current_water_table_mbgl: float
    ) -> Tuple[AlertLevel, ActionDirective, str]:
        """
        MANDATORY URJAGRAM RULE:
        Always pair Jev with a hard rule. A safety threshold set in code
        can only be raised by Jev, never lowered.
        """
        guardrail_triggered = False
        final_level = jev_decision

        # Hard Rule 1: Water table at or deeper than 16.5 mbgl (~54 ft)
        # Cannot be lower than WARNING under any condition.
        if current_water_table_mbgl >= WARNING_WATER_TABLE_MBGL:
            if final_level in [AlertLevel.NORMAL, AlertLevel.ADVISORY]:
                final_level = AlertLevel.WARNING
                guardrail_triggered = True

        # Hard Rule 2: Water table at or deeper than 18.0 mbgl (~59 ft)
        # MUST BE EMERGENCY regardless of any other input.
        if current_water_table_mbgl >= CRITICAL_EMERGENCY_MBGL:
            final_level = AlertLevel.EMERGENCY
            guardrail_triggered = True

        # Map to specific Action Directive
        if final_level == AlertLevel.EMERGENCY:
            directive = ActionDirective.CRITICAL_OVERDRAFT_HALT
            rationale = "Aquifer extraction has reached critical threshold. Groundwater reserved for human/animal survival."
        elif final_level == AlertLevel.WARNING:
            directive = ActionDirective.MANDATORY_MICRO_IRRIGATION
            rationale = "Water table depleted below safe limit. Flood irrigation banned; max 4 hrs pump run."
        elif final_level == AlertLevel.ADVISORY:
            directive = ActionDirective.SCHEDULE_ALTERATION
            rationale = "Water reserves declining. Night pumping and soil mulching recommended."
        else:
            directive = ActionDirective.OPTIMAL_IRRIGATION
            rationale = "Groundwater levels within safe operating capacity."

        guardrail_note = "Hard safety rule enforced override" if guardrail_triggered else "Compliant with safety threshold"
        return final_level, directive, guardrail_note
