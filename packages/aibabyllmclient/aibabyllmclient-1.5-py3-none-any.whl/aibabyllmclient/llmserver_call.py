from __future__ import print_function

import base64
import json
import logging
import time
import grpc
import numpy as np
from google.protobuf import any_pb2
from aibabyllmclient.core import (
    tongos_core_meta_pb2,
    tongos_service_pb2,
    tongos_service_pb2_grpc,
)

from aibabyllmclient.core import tongos_media_llm_req_pb2
from aibabyllmclient.core import tongos_media_llm_res_pb2


# from private_protocol.tongos_protocol.media.vision import tongos_media_cv_pb2


def got_packet(ts: int, prompt):
    # pg
    # with open("./client/test_data/ut/pg.json", "r") as f:
    #     # with open("./client/test_data/pg1107-2.txt", "r") as f:
    #     # with open("./client/test_data/pg1104-1.txt", "r") as f:
    #     pg = json.load(f)
    # items = json.dumps(pg)
    pg_data = tongos_media_llm_req_pb2.LLMREQMedia.ChunkData(prompt=prompt)
    # pg_data='{"CONT":"USA", "LOC":"柜台", "MONEY": "十万"}'
    data = any_pb2.Any()
    data.Pack(pg_data, "type.googleapis.com")
    data_chunk = tongos_core_meta_pb2.MediaChunk(
        create_ts=ts, bigai_media_url="bigai.tongos.media.nlp.NLGMedia", data=data
    )
    stream_chunk_pg = tongos_service_pb2.StreamPacket.StreamChunk(
        stream_tag="NLG_INPUT", stream_index=0, stream_name="pg", data_chunk=data_chunk
    )

    # merge
    # with open("./client/test_data/ut/merge_output.json", "r") as f:
    #     pg = json.load(f)
    # items = json.dumps(pg)
    # pg_data = tongos_media_cv_pb2.InformationMedia.ChunkData(info=items)
    # data = any_pb2.Any()
    # data.Pack(pg_data, "type.googleapis.com")
    # data_chunk = tongos_core_meta_pb2.MediaChunk(
    #     create_ts=ts, bigai_media_url="bigai.tongos.media.PGMedia", data=data
    # )
    # stream_chunk_mcmc = tongos_service_pb2.StreamPacket.StreamChunk(
    #     stream_tag="INFO_MCMC",
    #     stream_index=0,
    #     stream_name="mcmc",
    #     data_chunk=data_chunk,
    # )

    stream_chunks = []
    stream_chunks.append(stream_chunk_pg)
    # stream_chunks.append(stream_chunk_mcmc)
    packet = tongos_service_pb2.StreamPacket(chunks=stream_chunks)
    return packet


def call_llmserver(prompt,ip,port):
    with grpc.insecure_channel(ip+":"+port) as channel:
        stub = tongos_service_pb2_grpc.TongOSUnitStub(channel)
        # response = stub.SessionInitialization(
        #     tongos_service_pb2.SessionInitializationRequest()
        # )
        # print("respall:",response)
        # print("resp:" + response.session_id)
        packet = got_packet(0, prompt)
        req = tongos_service_pb2.MediaRequest(packet=packet)
        # call MediaProcess api
        resp = stub.MediaProcess(request=req)
        media_chunk=resp.packet.chunks[0].data_chunk
        info_data=tongos_media_llm_res_pb2.LLMRESMedia.ChunkData()
        media_chunk.data.Unpack(info_data)
        llm_result=str(info_data.output)
        print(f"llm_result*************{llm_result}")
        # for resp_item in resp:
        #     print("uuuuuuuuu")
        #     print(resp_item)
        #     print("ttttttttt")
        return llm_result

# # 两个线程跑
# import threading

# if __name__ == "__main__":
#     logging.basicConfig()

#     t1 = threading.Thread(target=run)
#     t1.start()
#     t2 = threading.Thread(target=run)
#     t2.start()
#     t1.join()
#     t2.join()

#     print("client send en!d")