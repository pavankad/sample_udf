text-proto:
	rm -rf proto.pb
	python3 text_to_protobuf.py ./samples/get_bid_request.pbtxt

run-udf: text-proto
	./run_udf.sh

gen-udf:
	python -m nuitka --standalone sample_udf.py	

gen-archive:
	cd sample_udf.dist && \
	cp sample_udf.bin bin.exe && \
	zip -r ../sample_udf.bin.zip . && \
	cd ..
