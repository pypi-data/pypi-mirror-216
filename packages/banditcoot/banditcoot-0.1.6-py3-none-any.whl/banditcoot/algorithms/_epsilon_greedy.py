import random

def ind_max(x):
    """
    returns the index that corresponds to the maximum value in array x
    """
    m = max(x)
    return x.index(m)

def hello_world():
    """
    test function to see if package is installed in editable mode
    """
    print("hello universe")

class EpsilonGreedy():
    """

    Parameters
    ----------
    epsilon: float
        Percentage of time the bandit explores
    n_arms: int
        Number of arms
    rewards: array
        Average units of reward observed for each successful arm pull
    conv_rates: array
        Success rates for each arm
    counts: array
        number of times each arm has been pulled

    Attributes
    ----------
    values: array
        average number of successes observed for each arm (i.e. conversion rate)
    """
    def __init__(self, epsilon, n_arms, rewards, conv_rates=None, counts=None):
        self.epsilon    = epsilon
        self.rewards    = rewards
        self.conv_rates = [0 for i in range(n_arms)] if conv_rates is None else conv_rates
        self.counts     = [0 for i in range(n_arms)] if counts is None else counts
        self.values     = [i*j for i,j in zip(self.conv_rates,self.rewards)]
        # raise error if n_arms does not equal number of entries in counts or values
        if ((n_arms != len(self.counts)) or (n_arms != len(self.values)) or (n_arms != len(self.conv_rates))):
            raise ValueError("n_arms does not match the length of counts/values/conv_rates")
        return

    def select_arm(self):
        if random.random() > self.epsilon:
            chosen_arm = ind_max(self.values)
        else:
            chosen_arm = random.randrange(len(self.values))
        return chosen_arm

    def update(self, chosen_arm, success_flag):
        # increments counts for chosen arm
        self.counts[chosen_arm] = self.counts[chosen_arm] + 1
        # calculate new average reward for chosen arm
        n = self.counts[chosen_arm]
        prev_value = self.values[chosen_arm]
        new_value = ((n - 1) / float(n)) * prev_value + (1 / float(n)) * success_flag * self.rewards[chosen_arm]
        self.values[chosen_arm] = new_value
        return
    
    def batch_update(self, chosen_arm, num_times_chosen, num_successes, observed_reward=None):
        
        # save previous algo parameter values
        prev_counts     = self.counts.copy()
        prev_conv_rates = self.conv_rates.copy()
        prev_rewards    = self.rewards.copy()
        prev_values     = self.values.copy()

        # increments counts for chosen arm
        self.counts[chosen_arm] = prev_counts[chosen_arm] + num_times_chosen

        # update conversion rates
        self.conv_rates[chosen_arm] = ((prev_conv_rates[chosen_arm] * prev_counts[chosen_arm]) + num_successes) / self.counts[chosen_arm]

        # calculate new average reward for chosen arm
        observed_reward = self.rewards[chosen_arm] if observed_reward is None else observed_reward
        prev_total_rewards = (prev_rewards[chosen_arm] * prev_conv_rates[chosen_arm] * prev_counts[chosen_arm])
        new_total_rewards  = num_successes * observed_reward
        self.rewards[chosen_arm] = (prev_total_rewards + new_total_rewards) / self.counts[chosen_arm]
        
        # calculate new average value for chosen arm
        self.values[chosen_arm] = (self.conv_rates[chosen_arm] * self.counts[chosen_arm] * self.rewards[chosen_arm])/self.counts[chosen_arm]
        return

