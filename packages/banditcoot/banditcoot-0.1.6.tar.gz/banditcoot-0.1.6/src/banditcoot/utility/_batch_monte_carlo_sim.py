def BatchMonteCarloTest(algo, arms, reward_amounts, n_iter, horizon):
    """
    Monte Carlo simulation used to test bandit algorithms with synthetic data

    algo: bandit algorithm of choice
    arms: array of arms to draw from
    n_iter: number of iterations
    horizon: horizon of time to simulate for each iteration
    """
    
    chosen_arms = [0.0 for i in range(n_iter * horizon)]
    rewards = [0.0 for i in range(n_iter * horizon)]
    cumulative_rewards = [0.0 for i in range(n_iter * horizon)]
    sim_nums = [0.0 for i in range(n_iter * horizon)]
    times = [0.0 for i in range(n_iter * horizon)]
    n_arms = len(arms)

    for sim in range(n_iter):
        sim += 1
        algo.initialize(n_arms)
    
        for t in range(horizon):
            t += 1
            index = (sim - 1) * horizon + t - 1
            sim_nums[index] = sim
            times[index] = t
            
            # choose an arm for time t
            chosen_arm = algo.select_arm()
            chosen_arms[index] = chosen_arm
            
            # record reward from chosen arm at time t
            reward = arms[chosen_arms[index]].draw() * reward_amounts[chosen_arm]
            rewards[index] = reward

            # record cumulative rewards
            cumulative_rewards[index] = cumulative_rewards[index - 1] + reward
            
            # update estimated reward from each arm
            algo.update(chosen_arm, reward)
  
    return [sim_nums, times, chosen_arms, rewards, cumulative_rewards]