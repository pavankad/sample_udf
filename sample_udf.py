#!/usr/bin/env python3
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os
from google.protobuf.internal import decoder
from google.protobuf.internal import encoder
import generate_bid_pb2
import io

def read_request_from_fd(file):
    request = generate_bid_pb2.GenerateProtectedAudienceBidRequest()
    request.ParseFromString(file.read())
    return request

def write_response_to_fd(file, response):
    """Write a response to a file descriptor."""
    data = response.SerializeToString()
    file.write(data)

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Not enough arguments!\n")
        return -1
    
    fd = int(sys.argv[1])
    with io.FileIO(fd, "rb+", closefd=False) as file:    
        # Read the request
        request = read_request_from_fd(file)
        
        # Create the response
        response = generate_bid_pb2.GenerateProtectedAudienceBidResponse()
        bid = generate_bid_pb2.ProtectedAudienceBid()
        bid.ad= request.interest_group.name
        bid.bid = 1.0
        bid.render = "https://my-render-url"
        bid.ad_cost= 2.0
        bid.bid_currency='USD'
        
        # Write the response
        response.bids.append(bid)
        write_response_to_fd(file, response)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())