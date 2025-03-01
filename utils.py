from typing import Dict
from database import Database

def calculate_weights(db: Database) -> Dict[str, float]:
    """Calculate current weights based on user votes"""
    votes = db._read_json(db.votes_file)
    
    # Default weights
    weights = {
        'social': 0.3,
        'environmental': 0.2,
        'political': 0.2,
        'philanthropy': 0.2,
        'cultural': 0.1
    }
    
    if not votes:
        return weights
    
    # Calculate average weights from votes
    vote_sums = {category: 0.0 for category in weights.keys()}
    vote_counts = {category: 0 for category in weights.keys()}
    
    for vote in votes:
        category = vote['category']
        if category in vote_sums:
            vote_sums[category] += vote['weight']
            vote_counts[category] += 1
    
    # Calculate normalized weights
    total_weight = 0
    for category in weights.keys():
        if vote_counts[category] > 0:
            weights[category] = vote_sums[category] / vote_counts[category]
            total_weight += weights[category]
    
    # Normalize weights to sum to 1
    if total_weight > 0:
        for category in weights.keys():
            weights[category] = weights[category] / total_weight
    
    return weights
