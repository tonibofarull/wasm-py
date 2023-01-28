FROM ubuntu:22.04

WORKDIR /tools

RUN apt-get update && apt-get install -y \
    git wget build-essential cmake python3 python3-pip

RUN git clone --recursive https://github.com/WebAssembly/wabt.git

WORKDIR /tools/wabt/build

RUN cmake .. && make -j $(nproc)

ENV PATH=/tools/wabt/build:$PATH

ARG WASI_SDK_VER=19
RUN wget https://github.com/WebAssembly/wasi-sdk/releases/download/wasi-sdk-${WASI_SDK_VER}/wasi-sdk-${WASI_SDK_VER}.0-linux.tar.gz && \
    tar -xvf wasi-sdk-${WASI_SDK_VER}.0-linux.tar.gz && \
    mv wasi-sdk-${WASI_SDK_VER}.0 /opt/wasi-sdk-${WASI_SDK_VER} && \
    ln -s /opt/wasi-sdk-${WASI_SDK_VER} /opt/wasi-sdk && \
    rm -rf wasi-sdk-*

ENV PATH=/opt/wasi-sdk/bin:$PATH

RUN useradd -m user
USER user
