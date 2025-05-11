#!/bin/bash
exec 3<>./samples/get_bid_req.proto
python3 sample_udf.py 3
exec 3>&-