
## Install protobuf compiler & protoc

```
python -m pip install nuitka
sudo apt-get install python3-dev
apt install patchelf
```

## Instruction for latest protoc compiler

```
PB_REL="https://github.com/protocolbuffers/protobuf/releases"
curl -LO $PB_REL/download/v30.2/protoc-30.2-linux-x86_64.zip
unzip protoc-30.2-linux-x86_64.zip -d $HOME/.local
export PATH="$PATH:$HOME/.local/bin"

```

## Steps to generate Binary

- Run commands specified in command.sh to generate protobuf header files
- Run nuitka to generate standalone binary as below
```
python -m nuitka --standalone sample_udf.py 
```


## Generate protobuf message from JSON inputfile

```
python serialize_request.py samples/get_bid_request.pbtxt samples/get_bid_req.proto
```

