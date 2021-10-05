import random

from ad import Ad

def create_random_ctr():
    return round(random.uniform(0.15, 0.2), 2)
    
def create_random_context_multipliers(ads) -> dict[Ad, float]:
    multiplier_map = {}
    for ad in ads:
        multiplier_map[ad] = round(random.uniform(0.8, 1.2), 2)

    return multiplier_map
    
