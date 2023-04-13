#!/bin/bash
set -x
packet_count=1000
run_test() {
    docker-compose down
    docker-compose up -d
    sleep 10
    bash net_setup.sh
    echo "rate is $1"
    SERVICE_NAME=secondary
    for id in $(docker-compose ps -q $SERVICE_NAME); do
        docker exec -d "$id" python -u secondary_test.py
    done;

    # PKTS_NEED_TO_PROCESS=$(grep PKTS_NEED_TO_PROCESS .env | cut -d '=' -f2)
    # duration=$((PKTS_NEED_TO_PROCESS/$1+10))
    # echo "Duration: $duration"

    for ((i=0;i<$2;i++))
    do
        # b_rate=$(( $1 * 1400 ))
        # dd if="packet_sender_data.txt" bs=1400 count="$packet_count" | pv --rate-limit "$b_rate" --bytes | nc -u 127.0.0.1 8080
        iperf -c 127.0.0.1 -p 8080 -u -b "$1"pps -F packet_sender_data.txt -l 100 -t 60 -x CDMSV &
        # packetsender --udp --rate "$1" --num "$packet_count" 127.0.0.1 8080 --file packet_sender_data.txt &
    done
    python kill_iperf.py
    
}

# clear the previous results 
rm -rf results/*
mkdir -p results

batches=(80)
buffers=(100)
pkt_rates=(200)
flow_counts=(10)
stamper_counts=(3)
# stamper_counts=(1)

docker-compose build


for stamper_count in "${stamper_counts[@]}"; do
    for flow_count in "${flow_counts[@]}"; do
        for bs in "${batches[@]}"; do
            for (( bfs=10 ; bfs<=10 ; bfs++ )); do
                for (( pr=2000 ; pr<=2000 ; pr+=500 )); do
                    echo "Batch size = $batch_size, Buffer size = $buffer_size, Packet rate = $packet_rate, Flow Count = $flow_count"
                    
                    # replace env values in .env file
                    nf_cnt=$stamper_count
                    flow_cnt_per_nf=$((flow_count/$nf_cnt))
                    sed -i~ "/^BATCH_SIZE=/s/=.*/=$bs/" .env
                    sed -i~ "/^BUFFER_SIZE=/s/=.*/=$bfs/" .env
                    sed -i~ "/^PACKET_RATE=/s/=.*/=$pr/" .env
                    sed -i~ "/^STAMPER_CNT=/s/=.*/=$stamper_count/" .env
                    sed -i~ "/^FLOW_CNT_PER_NF=/s/=.*/=$flow_cnt_per_nf/" .env
                    sed -i~ "/^HZ_CLIENT_CNT=/s/=.*/=$nf_cnt/" .env
                     
                    filename=results/batch_"${bs}"-buf_"${bfs}"-pktrate_"${pr}"-flow_cnt_"${flow_cnt_per_nf}"-stamper_cnt_"${stamper_count}".csv
                    echo "Flow, Latency(ms), Throughput(byte/s), Throughput(pps), Packets Dropped" >> "$filename"

                    for trial in {10..10}; do
                        echo "Trial number $trial"
                        sed -i~ "/^TRIAL=/s/=.*/=$trial/" .env
                        run_test "$pr" "$flow_count" 
                    done
                    echo
                done
            done
        done
    done
done

