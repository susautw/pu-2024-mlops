BASE_DIR = $(shell pwd)
OUT_DIR = ./src/protos
PROTOS_DIR = ./protos

gen-proto:
	cd $(BASE_DIR) && \
	python -m grpc_tools.protoc \
	 -I $(PROTOS_DIR) \
	 --python_out=$(OUT_DIR) \
 	 --pyi_out=$(OUT_DIR) \
 	 --grpc_python_out=$(OUT_DIR) \
 	 $(PROTOS_DIR)/*