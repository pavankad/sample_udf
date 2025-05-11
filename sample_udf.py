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

#import pdb

def read_request_from_fd(fd):    
    # Create a buffer to store all parts of the message
    message_buffer = bytearray()
    
    # Read first byte and discard it
    b = os.read(fd, 1)
    print(f"First byte: {b}")
    # Read the first byte(s) of the length prefix (varint-encoded)
    def read_varint():
        shift = 0
        result = 0
        varint_buffer = bytearray()
        

        while True:
            b = os.read(fd, 1)
            if not b:
                raise EOFError("Unexpected EOF while reading varint")
            
            # Add to our buffer
            varint_buffer.extend(b)
            message_buffer.extend(b)
            
            byte = b[0]
            result |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7
        
        return int(result), varint_buffer
    
    # Read tag byte
    tag_byte = os.read(fd, 1)
    if not tag_byte:
        raise EOFError("Unexpected EOF while reading tag byte")

    # Add tag byte to our buffer
    message_buffer.extend(tag_byte)
    
    # Parse tag byte
    tag_value = tag_byte[0]
    #pdb.set_trace()
    field_number = tag_value >> 3
    wire_type = tag_value & 0x7

    print(f"Parsed tag byte: 0x{tag_value:02x}")
    print(f"Field number: {field_number}, Wire type: {wire_type}")
    
    # Check if this is a length-delimited field (wire type 2)
    if wire_type != 2:
        raise ValueError(f"Expected wire type 2 (length-delimited), got {wire_type}")
    
    # Read the length as a varint
    msg_len, length_buffer = read_varint()
    #message_buffer.extend(length_buffer)
    print(f"Message length: {msg_len} bytes (encoded in {len(length_buffer)} bytes)")
    print("Length buffer:", length_buffer)
    print("Message buffer:", message_buffer)
    # Read the message data (payload)
    msg_data = os.read(fd, msg_len)
    if len(msg_data) < msg_len:
        raise EOFError(f"Truncated message: expected {msg_len} bytes, got {len(msg_data)} bytes")
    
    # Add message data to our buffer
    message_buffer.extend(msg_data)
    print(message_buffer)
    """
    # Print buffer analysis
    tag_end = 1  # Tag is 1 byte
    length_end = tag_end + len(length_buffer)
    payload_end = length_end + len(msg_data)
    
    print("\nProtobuf Message Structure:")
    print(f"  Tag:    bytes 0-{tag_end-1} ({tag_end} bytes)")
    print(f"  Length: bytes {tag_end}-{length_end-1} ({len(length_buffer)} bytes)")
    print(f"  Payload: bytes {length_end}-{payload_end-1} ({len(msg_data)} bytes)")
    print(f"  Total message size: {len(message_buffer)} bytes")
    
    # For debugging: show hex representation of the full message
    print("\nHex representation of the protobuf message:")
    for i in range(0, len(message_buffer), 16):
        chunk = message_buffer[i:i+16]
        hex_values = ' '.join(f'{b:02x}' for b in chunk)
        print(f"  {i:04x}: {hex_values}")

    """
    # Parse the message data
    request = generate_bid_pb2.GenerateProtectedAudienceBidRequest()
    request.ParseFromString(message_buffer)
    return request

def write_response_to_fd(fd, response):
    """Write a response to a file descriptor."""
    data = bytearray()
    data.extend(response.SerializeToString())
    print(data)
    os.write(fd, data)

def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Not enough arguments!\n")
        return -1
    
    fd = int(sys.argv[1])
    #with io.FileIO(fd, "rb+", closefd=False) as file:    
    # Read the request
    request = read_request_from_fd(fd)
    print(request)

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
    print(response, "\n")
    #write_response_to_fd(file, response)
    write_response_to_fd(fd, response)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())