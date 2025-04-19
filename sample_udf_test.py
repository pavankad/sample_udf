import generate_bid_pb2
import sys
import pdb
import os

"""
sample_message = generate_bid_pb2.GenerateProtectedAudienceBidRequest()

sample_message.interest_group.name = "Maya Kausalya"
sample_message.interest_group.user_bidding_signals = "{\"age\":29, \"avg_amount_spent\":10000}"
sample_message.server_metadata.logging_enabled=True
sample_message.server_metadata.debug_reporting_enabled=True

print(sample_message)


with open("sample.bin", "wb") as f:
    print("write as binary")
    bytesAsString = sample_message.SerializeToString()
    f.write(bytesAsString)


with open("sample.bin", "rb") as f:
    print("read values")
    sample_message_read = generate_bid_pb2.GenerateProtectedAudienceBidRequest().FromString(f.read())

print(sample_message_read)

response = generate_bid_pb2.GenerateProtectedAudienceBidResponse()

pdb.set_trace()
"""


def ReadRequestFromFd(fd):
	size = os.stat(fd).st_size
	req = generate_bid_pb2.GenerateProtectedAudienceBidRequest().FromString(os.read(fd, size))
	return req
   
def WriteResponseToFd(fd2, response):
	bytesAsString = response.SerializeToString()
	os.write(fd2, bytesAsString)

def main():
	if len(sys.argv) != 2:
		print("Expecting exactly one argument", file=sys.stderr)
		sys.exit(-1)

	fd = os.open(sys.argv[1], os.O_RDWR)

	req = ReadRequestFromFd(fd)

	print(req)

	response = generate_bid_pb2.GenerateProtectedAudienceBidResponse()

	bid = generate_bid_pb2.ProtectedAudienceBid()
	bid.ad='ad'
	bid.bid = 1.0
	bid.render = "https://my-render-url"
	bid.ad_cost=2.0
	bid.bid_currency='USD'

	response.bids.append(bid)
	fd2 = os.open("sample_write.bin", os.O_RDWR)
	WriteResponseToFd(fd2, response);

	print(response)

if __name__ == "__main__":
    main()



