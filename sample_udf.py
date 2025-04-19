import generate_bid_pb2
import sys
import os

def ReadRequestFromFd(fd):
	size = os.stat(fd).st_size
	req = generate_bid_pb2.GenerateProtectedAudienceBidRequest().FromString(os.read(fd, size))
	return req
   
def WriteResponseToFd(fd, response):
	bytesAsString = response.SerializeToString()
	os.write(fd, bytesAsString)

def main():
	if len(sys.argv) != 2:
		print("Expecting exactly one argument", file=sys.stderr)
		sys.exit(-1)

	fd = int(sys.argv[1])
	print(fd)
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
	#fd2 = os.open("sample_write.bin", os.O_RDWR)
	WriteResponseToFd(fd, response);

	print(response)

if __name__ == "__main__":
    main()



