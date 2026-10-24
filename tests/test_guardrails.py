"""
Unit tests for Jev System-One Decision Engine & Safety Guardrails.
"""

from src.jev_engine import JevDecisionEngine, AlertLevel, ActionDirective

def test_hard_safety_guardrail_enforcement():
    # Simulate a scenario where water table is at 17.0 mbgl (> 16.5 mbgl WARNING threshold)
    # Even if Jev thought it was NORMAL, the hard rule MUST force it to at least WARNING!
    prelim_decision = AlertLevel.NORMAL
    severe_water_table_mbgl = 17.0

    final_level, directive, note = JevDecisionEngine.enforce_hard_safety_guardrails(
        jev_decision=prelim_decision,
        current_water_table_mbgl=severe_water_table_mbgl
    )

    assert final_level == AlertLevel.WARNING
    assert directive == ActionDirective.MANDATORY_MICRO_IRRIGATION
    assert "Hard safety rule enforced override" in note

def test_critical_emergency_guardrail():
    # Water table beyond 18.0 mbgl must trigger EMERGENCY regardless of input
    final_level, directive, note = JevDecisionEngine.enforce_hard_safety_guardrails(
        jev_decision=AlertLevel.ADVISORY,
        current_water_table_mbgl=18.5
    )

    assert final_level == AlertLevel.EMERGENCY
    assert directive == ActionDirective.CRITICAL_OVERDRAFT_HALT
