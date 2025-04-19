## Command to generate python binary ##
python -m pip install nuitka
sudo apt-get install python3-dev
apt install patchelf
python -m nuitka --standalone --onefile sample_udf.py 
##run commands specified in command.sh to generate protobuf headers##
#install protoc
sudo apt upgrade protobuf-compiler

