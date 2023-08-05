import random

def categorical_draw(probs):
    """
    Given an array if probabilities, returns  
    """
    probs = [0.2, 0.4, 0.1, 0.3]
    z = random.random()
    cum_prob = 0.0
    for i in range(len(probs)):
        prob = probs[i]
        cum_prob += prob
        if cum_prob > z:
            return i
    return len(probs) - 1
    cum_prob

class Softmax():
    """
    Softmax will have a variable exploration rate based on the value specified
    for tau or a "temperature" parameter. Based on the analogy from physics in
    which a system will behave differently at higher temperatures.

    Parameters
    ----------
    tau : float
        Scaling factor that determines how often the Softmax algorithm explores.
        tau = 0 results in choosing the arm with the highest estimated value 
        every time. tau = Inf would result in purely random exploration, similar
        to the Epsilon Greedy algorithm.
    
    counts: int

    values: float

    Attributes
    ----------

    
    """
    def __init__(self, tau, counts, values):
        self.tau = tau
        self.counts = counts
        self.values = values
        return
    
    def initialize(self, n_arms):
        self.counts = [0 for col in range(n_arms)]
        self.values = [0.0 for col in range(n_arms)]
        return
    
    def select_arm(self):
        z = sum([math.exp(v / self.tau) for v in self.values])
        probs = [math.exp(v / self.tau) / z for v in self.values]
        return categorical_draw(probs)

    def update(self, chosen_arm, reward):
        self.counts[chosen_arm] = self.counts[chosen_arm] + 1
        n = self.counts[chosen_arm]
        
        value = self.values[chosen_arm]
        new_value = ((n - 1) / float(n)) * value + (1 / float(n)) * reward
        self.values[chosen_arm] = new_value
        return