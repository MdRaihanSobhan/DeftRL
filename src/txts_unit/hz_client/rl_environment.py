import gym
from gym import spaces
import numpy as np

class DEFTEnvironment(gym.Env):
    def __init__(self):
        super(DEFTEnvironment, self).__init__()
        
        # Define action and observation space
        self.action_space = spaces.Discrete(5)  # 5 actions: adjust batch size, buffer size, packet rate, flow count, stamper count
        self.observation_space = spaces.Box(low=0, high=np.inf, shape=(9,), dtype=np.float32)
        
        self.state = None
        self.previous_state = None

    def reset(self):
        self.state = np.zeros(9)
        self.previous_state = None
        return self.state

    def step(self, action):
        # Apply the action to the DEFT system
        self._apply_action(action)
        
        # Get the next state from the DEFT system
        next_state = self._get_next_state()
        
        reward = self._calculate_reward(next_state)
        
        done = False  # Episode doesn't end in this continuous system
        
        self.previous_state = self.state
        self.state = next_state
        
        return next_state, reward, done, {}

    def _apply_action(self, action):
        if action == 0:
            Limit.BATCH_SIZE = max(10, Limit.BATCH_SIZE - 10)
        elif action == 1:
            Limit.BATCH_SIZE = min(200, Limit.BATCH_SIZE + 10)
        elif action == 2:
            Limit.BUFFER_LIMIT = max(Limit.BATCH_SIZE, Limit.BUFFER_LIMIT - Limit.BATCH_SIZE)
        elif action == 3:
            Limit.BUFFER_LIMIT = min(10 * Limit.BATCH_SIZE, Limit.BUFFER_LIMIT + Limit.BATCH_SIZE)
        elif action == 4:
            Limit.GLOBAL_UPDATE_FREQUENCY = max(1, Limit.GLOBAL_UPDATE_FREQUENCY - 1)

    def _get_next_state(self):
        return np.array([
            Statistics.calculate_latency(),
            Statistics.calculate_throughput_bytes(),
            Statistics.calculate_throughput_pps(),
            Statistics.processed_pkts,
            Statistics.packet_dropped,
            Buffers.get_input_buffer_time(),
            Buffers.get_output_buffer_time(),
            Statistics.calculate_processing_time(),
            Statistics.calculate_path_latency()
        ], dtype=np.float32)

    def _calculate_reward(self, state):
        return calculate_reward(*state, previous_state=self.previous_state)

def calculate_reward(
    latency,
    throughput_bytes,
    throughput_pps,
    packets_processed,
    packets_dropped,
    time_in_input_buffer,
    time_in_output_buffer,
    time_in_pkt_processing,
    path_latency,
    previous_state=None
):
    w_latency = -1.0
    w_throughput_bytes = 0.5
    w_throughput_pps = 0.5
    w_packets_processed = 0.3
    w_packets_dropped = -2.0
    w_time_in_buffers = -0.5
    w_time_in_processing = -0.5
    w_path_latency = -0.8
    
    r_latency = w_latency * latency
    r_throughput = w_throughput_bytes * np.log1p(throughput_bytes) + w_throughput_pps * np.log1p(throughput_pps)
    r_packets = w_packets_processed * np.log1p(packets_processed) + w_packets_dropped * packets_dropped
    r_buffers = w_time_in_buffers * (time_in_input_buffer + time_in_output_buffer)
    r_processing = w_time_in_processing * time_in_pkt_processing
    r_path = w_path_latency * path_latency
    
    improvements = 0
    if previous_state is not None:
        improvements += max(0, previous_state[0] - latency)
        improvements += max(0, throughput_bytes - previous_state[1]) / 1e6
        improvements += max(0, throughput_pps - previous_state[2]) / 1e3
        improvements += max(0, packets_processed - previous_state[3]) / 1e3
        improvements += max(0, previous_state[4] - packets_dropped)
        improvements += max(0, previous_state[5] - time_in_input_buffer)
        improvements += max(0, previous_state[6] - time_in_output_buffer)
        improvements += max(0, previous_state[7] - time_in_pkt_processing)
        improvements += max(0, previous_state[8] - path_latency)
    
    reward = r_latency + r_throughput + r_packets + r_buffers + r_processing + r_path + improvements
    
    return reward