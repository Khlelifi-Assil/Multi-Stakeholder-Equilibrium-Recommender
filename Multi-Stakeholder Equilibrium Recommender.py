import numpy as np
from typing import Dict, List

class StakeholderUtility:
    """
    Defines a stakeholder and their specific utility function weights.
    """
    def __init__(self, name: str, weights: Dict[str, float], color: str = 'gray'):
        self.name = name
        self.weights = weights
        self.color = color

    def calculate(self, outcome_metrics: Dict[str, float]) -> float:
        """
        Calculates utility for a specific slate outcome based on weights.
        U = sum(weight_i * metric_i)
        """
        return sum(self.weights.get(k, 0) * v for k, v in outcome_metrics.items())

class MultiStakeholderRecommender:
    """
    Optimizes recommendation slates to maximize Social Welfare 
    across User, Creator, Platform, and Society.
    """
    def __init__(self, stakeholders: List[StakeholderUtility]):
        self.stakeholders = stakeholders

    def _calculate_diversity(self, rec_set: List[Dict]) -> float:
        """
        Calculates 1 - Jaccard Similarity averaged over all pairs in the slate.
        Higher is better.
        """
        n = len(rec_set)
        if n < 2: return 0
        
        total_sim = 0
        pairs = 0
        for i in range(n):
            for j in range(i + 1, n):
                # Assuming items have a 'category' field
                g1 = set(str(rec_set[i].get('category', '')).split('|'))
                g2 = set(str(rec_set[j].get('category', '')).split('|'))
                
                if not g1 and not g2:
                    sim = 1
                else:
                    intersection = len(g1.intersection(g2))
                    union = len(g1.union(g2))
                    sim = intersection / union if union > 0 else 0
                
                total_sim += sim
                pairs += 1
        
        return 1 - (total_sim / pairs) if pairs > 0 else 0

    def evaluate_slate_outcome(self, rec_set: List[Dict]) -> Dict[str, float]:
        """
        Aggregates raw item attributes into slate-level system metrics.
        """
        return {
            'relevance': np.mean([r.get('relevance', 0) for r in rec_set]),
            'diversity': self._calculate_diversity(rec_set),
            'exposure': np.mean([r.get('creator_score', 0) for r in rec_set]),
            'engagement': np.mean([r.get('engagement', 0) for r in rec_set]),
            'misinformation': np.mean([r.get('misinfo', 0) for r in rec_set]),
            'polarization': np.mean([r.get('polarization', 0) for r in rec_set])
        }

    def select_optimal_slate(self, candidate_sets: List[List[Dict]]) -> Dict:
        """
        Iterates through candidate slates to find the Nash Equilibrium / Social Welfare optimum.
        
        Objective: Maximize Sum(Utilities)
        Constraint: Rawlsian Penalty (prevent utility collapse for any single stakeholder).
        """
        best_set = None
        best_welfare = -np.inf
        best_metrics = None
        best_utilities = None

        for rec_set in candidate_sets:
            # 1. Evaluate System Metrics for this slate
            outcomes = self.evaluate_slate_outcome(rec_set)
            
            # 2. Calculate Utility for every stakeholder
            utilities = [s.calculate(outcomes) for s in self.stakeholders]
            welfare = sum(utilities)

            # 3. Apply Rawlsian Penalty
            # If the minimum utility is significantly lower than the average, 
            # punish the score to avoid crushing a stakeholder.
            avg_util = np.mean(utilities)
            min_util = min(utilities)
            
            # Threshold: Min utility cannot be less than 40% of the average
            if min_util < avg_util * 0.4: 
                welfare *= 0.5  # Heavy penalty

            # 4. Update Best
            if welfare > best_welfare:
                best_welfare = welfare
                best_set = rec_set
                best_metrics = outcomes
                best_utilities = utilities

        return {
            "slate": best_set,
            "welfare": best_welfare,
            "metrics": best_metrics,
            "utilities": best_utilities
        }