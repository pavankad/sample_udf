#!/bin/bash
exec 3<>./proto.pb
python3 sample_udf.py 3
exec 3>&-