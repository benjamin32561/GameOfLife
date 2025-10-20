"""
Alert system for the Nature Ecosystem Simulation.
Provides various alert types to monitor simulation state.
"""
from alerts.alert_manager import AlertManager
from alerts.base_alert import BaseAlert
from alerts.entity_above_threshold_alert import EntityAboveThreshold
from alerts.predator_eats_herbivore_alert import PredatorEatsHerbivoreAlert
from alerts.zero_stats_alert import ZeroStatsAlert

__all__ = [
    'BaseAlert',
    'ZeroStatsAlert',
    'PredatorEatsHerbivoreAlert',
    'EntityAboveThreshold',
    'AlertManager',
]

