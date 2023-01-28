/opt/wasi-sdk/bin/clang \
    -O3 \
    -nostdlib \
    -Wl,--allow-undefined \
    -Wl,--no-entry \
    -o test.wasm tests/test.c \
