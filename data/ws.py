import asyncio
import websockets
from receive import create_inlets, process_data
import time
import json
import numpy as np

def parse_data(data):
    field_length = {
        "heartRate": 1,
        "respiration": 1,
        "leftEnergy": 1,
        "ECG": 6000,
        "RESP": 6000,
        "EDA": 6000,
        "PULSE": 6000,
        "mean": 1,
        "variance": 1,
        "value": 1,
        "corrdinates": 120,
        "cognitiveLoad": 1,
        "vigilance": 1,
        "emotion": 5,
        "emotionHistory": 150
    }

    json_data = {}
    offset = 0

    for field in field_length:
        length = field_length[field]

        if field == 'corrdinates':
            field_data = data[offset:offset + length]
            json_data[field] = np.array(field_data).reshape(-1, 2).tolist()

        elif field == 'emotion_history':
            field_data = data[offset:offset + length]
            json_data[field] = np.array(field_data).reshape(-1, 5).tolist()
        
        elif length == 1:
            json_data[field] = data[offset]
        
        else:
            json_data[field] = data[offset:offset + length]
        
        offset += length
        
    return json.dumps(json_data)

async def fetch_parse_send(socket):
    inlet = create_inlets()
    while True:
        # fetch
        sample, _ = inlet.pull_sample()
        print(f"Data received at: {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # parse
        json_data = parse_data(sample)

        # send
        await socket.send(json_data)
        await asyncio.sleep(3)

async def main():
    async with websockets.serve(fetch_parse_send, "localhost", 8080):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())