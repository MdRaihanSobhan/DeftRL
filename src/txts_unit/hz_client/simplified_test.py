import logging
import hazelcast
import threading
import queue
from queue import PriorityQueue
from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol, DatagramProtocol
import sys
import os
from dotenv import load_dotenv
import numpy as np
from stable_baselines3 import PPO
from rl_environment import DEFTEnvironment

load_dotenv()

sys.path.append('..')
from exp_package import Hazelcast, Helpers
from exp_package.Two_phase_commit.primary_2pc import Primary

import socket

per_flow_packet_counter = None
master: Primary = None
rl_model = None

class Buffers:
    input_buffer = queue.Queue(maxsize=100000)
    output_buffer = queue.Queue(maxsize=100000)

    @staticmethod
    def get_input_buffer_time():
        return np.mean([BufferTimeMaps.input_out[id] - BufferTimeMaps.input_in[id] for id in BufferTimeMaps.input_out])

    @staticmethod
    def get_output_buffer_time():
        return np.mean([BufferTimeMaps.output_out[id] - BufferTimeMaps.output_in[id] for id in BufferTimeMaps.output_out])

class BufferTimeMaps:
    input_in = {}
    input_out = {}
    output_in = {}
    output_out = {}

class Timestamps:
    start_time = None
    end_time = None

class Limit:
    BATCH_SIZE = int(os.getenv('BATCH_SIZE'))
    PKTS_NEED_TO_PROCESS = 1000
    GLOBAL_UPDATE_FREQUENCY = 1
    BUFFER_LIMIT = 1 * BATCH_SIZE

class Statistics:
    processed_pkts = 0
    received_packets = 0
    total_packet_size = 0
    total_delay_time = 0
    total_three_pc_time = 0
    packet_dropped = 0

    @classmethod
    def calculate_latency(cls):
        return cls.total_delay_time / max(1, cls.processed_pkts)

    @classmethod
    def calculate_throughput_bytes(cls):
        time_delta = Helpers.get_current_time_in_ms() - Timestamps.start_time
        return cls.total_packet_size / max(1, time_delta / 1000.0)

    @classmethod
    def calculate_throughput_pps(cls):
        time_delta = Helpers.get_current_time_in_ms() - Timestamps.start_time
        return cls.processed_pkts / max(1, time_delta / 1000.0)

    @classmethod
    def calculate_processing_time(cls):
        return cls.total_three_pc_time / max(1, cls.processed_pkts)

    @classmethod
    def calculate_path_latency(cls):
        return cls.total_delay_time / max(1, cls.processed_pkts)

class State:
    per_flow_cnt = {}

# def receive_a_pkt(pkt):
#     if Statistics.received_packets == 0:
#         Timestamps.start_time = Helpers.get_current_time_in_ms()

#     Statistics.received_packets += 1
#     print(f'received pkts: {Statistics.received_packets}')

#     if Buffers.input_buffer.qsize() < Limit.BUFFER_LIMIT:
#         Buffers.input_buffer.put((pkt, Statistics.received_packets))
#         BufferTimeMaps.input_in[Statistics.received_packets] = Helpers.get_current_time_in_ms()
#     else:
#         Statistics.packet_dropped += 1

def receive_a_pkt(pkt):
    if Statistics.received_packets == 0:
        Timestamps.start_time = Helpers.get_current_time_in_ms()

    Statistics.received_packets += 1
    print(f'received pkts: {Statistics.received_packets}')

    if Buffers.input_buffer.qsize() < Limit.BUFFER_LIMIT:
        Buffers.input_buffer.put((pkt, Statistics.received_packets))
        BufferTimeMaps.input_in[Statistics.received_packets] = Helpers.get_current_time_in_ms()
    else:
        Statistics.packet_dropped += 1

def process_a_packet(packet, packet_id):
    Statistics.processed_pkts += 1
    Statistics.total_packet_size += len(packet)
    print(f'Length of packet is {len(packet)}')
    print(f'Processed pkts: {Statistics.processed_pkts}')

    Statistics.total_delay_time += Helpers.get_current_time_in_ms() - BufferTimeMaps.input_in[packet_id]
    BufferTimeMaps.input_out[packet_id] = Helpers.get_current_time_in_ms()

    Buffers.output_buffer.put((packet, packet_id))
    BufferTimeMaps.output_in[packet_id] = Helpers.get_current_time_in_ms()

def process_packet_with_hazelcast():
    global rl_model
    env = DEFTEnvironment()

    pkt_num_of_cur_batch = 0
    uniform_global_distance = Limit.BATCH_SIZE // Limit.GLOBAL_UPDATE_FREQUENCY

    while True:
        pkt, pkt_id = Buffers.input_buffer.get()

        # Get current state
        current_state = env._get_next_state()

        # Use RL model to choose action
        action, _ = rl_model.predict(current_state)

        # Apply the action
        env._apply_action(action)

        process_a_packet(pkt, pkt_id)

        pkt_num_of_cur_batch += 1

        if Buffers.output_buffer.qsize() == Limit.BATCH_SIZE:
            pkt_num_of_cur_batch = 0
            empty_output_buffer()
            local_state_update()

        if pkt_num_of_cur_batch % uniform_global_distance == 0 or pkt_num_of_cur_batch == Limit.BATCH_SIZE:
            global_state_update(10)

        if Statistics.processed_pkts + Statistics.packet_dropped == Limit.PKTS_NEED_TO_PROCESS:
            Timestamps.end_time = Helpers.get_current_time_in_ms()
            generate_statistics()
            break

def generate_statistics():
    time_delta = Timestamps.end_time - Timestamps.start_time
    total_process_time = time_delta / 1000.0
    throughput = Statistics.total_packet_size / total_process_time
    latency = Statistics.total_delay_time / Statistics.processed_pkts

    batch_size = Limit.BATCH_SIZE
    buffer_size = Limit.BUFFER_LIMIT
    packet_rate = Statistics.calculate_throughput_pps()
    
    filename = f'results/batch_{batch_size}-buf_{buffer_size}-pktrate_{packet_rate:.0f}.csv'

    with open(filename, 'a') as f:
        f.write(f'{latency},{throughput},{Statistics.packet_dropped}\n')

def empty_output_buffer():
    while not Buffers.output_buffer.empty():
        _, pkt_id = Buffers.output_buffer.get()
        BufferTimeMaps.output_out[pkt_id] = Helpers.get_current_time_in_ms()
        Statistics.total_delay_time += BufferTimeMaps.output_out[pkt_id] - BufferTimeMaps.output_in[pkt_id]

def local_state_update():
    print(f'replicating on backup as per batch.\n cur_batch: {State.per_flow_cnt}')
    cur_time = Helpers.get_current_time_in_ms()
    global_state = per_flow_packet_counter.get("global")
    master.replicate(global_state)
    Statistics.total_three_pc_time += Helpers.get_current_time_in_ms() - cur_time

def global_state_update(batches_processed: int):
    print(f'Global state update')
    map_key = "global"
    per_flow_packet_counter.lock(map_key)
    value = per_flow_packet_counter.get(map_key)
    per_flow_packet_counter.set(map_key, batches_processed if value is None else value + batches_processed)
    per_flow_packet_counter.unlock(map_key)
    print(per_flow_packet_counter.get(map_key))

# class EchoUDP(DatagramProtocol):
#     def datagramReceived(self, datagram, address):
#         receive_a_pkt(datagram)

from twisted.internet import reactor

class EchoUDP(DatagramProtocol):
    def __init__(self):
        self.iperf_packets = 0
        self.iperf_client = None

    def startProtocol(self):
        self.iperf_client = reactor.listenUDP(0, self)

    def datagramReceived(self, datagram, address):
        if len(datagram) >= 4 and datagram[:4] == b'\x00\x80\x00\x00':  # iperf2 UDP packet header
            self.iperf_packets += 1
            if self.iperf_packets % 100 == 0:  # Log every 100 iperf packets
                print(f"Received {self.iperf_packets} iperf packets")
            # Forward iperf packet to the iperf server
            self.iperf_client.transport.write(datagram, ('127.0.0.1', 5001))
        else:
            receive_a_pkt(datagram)

    def connectionRefused(self):
        print("No one listening")

def train_rl_model():
    env = DEFTEnvironment()
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)
    model.save("ppo_deft_model")
    return model

CLUSTER_NAME = "deft-cluster"
LISTENING_PORT = 8000

# def main():
#     global per_flow_packet_counter, rl_model

#     print(f"Trying to connect to cluster {CLUSTER_NAME}....")

#     hazelcast_client = hazelcast.HazelcastClient(cluster_members=["hazelcast:5701"],
#                                                  cluster_name=CLUSTER_NAME)
#     print("Connected!")

#     per_flow_packet_counter = Hazelcast.create_per_flow_packet_counter(hazelcast_client)

#     # Train RL model
#     rl_model = train_rl_model()

#     hazelcast_thread = threading.Thread(target=process_packet_with_hazelcast)
#     hazelcast_thread.start()

#     print(f"Listening for packets on port {LISTENING_PORT}")
#     reactor.listenUDP(LISTENING_PORT, EchoUDP())
#     reactor.run()

DEFT_LISTENING_PORT = 8000  # or whatever port your DEFT system should listen on

def main():
    global per_flow_packet_counter, rl_model

    print(f"Trying to connect to cluster {CLUSTER_NAME}....")

    hazelcast_client = hazelcast.HazelcastClient(cluster_members=["hazelcast:5701"],
                                                 cluster_name=CLUSTER_NAME)
    print("Connected!")

    per_flow_packet_counter = Hazelcast.create_per_flow_packet_counter(hazelcast_client)

    # Train RL model
    rl_model = train_rl_model()

    hazelcast_thread = threading.Thread(target=process_packet_with_hazelcast)
    hazelcast_thread.start()

    print(f"Listening for packets on port {DEFT_LISTENING_PORT}")
    reactor.listenUDP(DEFT_LISTENING_PORT, EchoUDP())
    reactor.run()

if __name__ == '__main__':
    main()