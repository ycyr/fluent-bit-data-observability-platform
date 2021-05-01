FROM golang:1.15.3 as build_loki_plugin

ENV LOKI_MAJOR 2
ENV LOKI_MINOR 0
ENV LOKI_PATCH 0

ENV LOKI_VERSION v${LOKI_MAJOR}.${LOKI_MINOR}.${LOKI_PATCH}

# Completely self contained build
RUN mkdir -p /src && cd /src && \
    git clone --depth 1 --branch $LOKI_VERSION https://github.com/grafana/loki.git
WORKDIR /src/loki

RUN make clean && make BUILD_IN_CONTAINER=true fluent-bit-plugin

FROM golang:1.15.3 as build_prometheus_metrics_plugin

ENV GOOS=linux\
    GOARCH=amd64

RUN mkdir -p /root && cd /root && \
    git clone --depth 1 --branch master https://github.com/neiman-marcus/fluent-bit-out-prometheus-metrics.git

WORKDIR /root/fluent-bit-out-prometheus-metrics

RUN go mod edit -replace github.com/fluent/fluent-bit-go=github.com/fluent/fluent-bit-go@master
RUN go mod download
RUN make clean && make build-plugin

FROM debian:buster as builder_fluent_bit

# Fluent Bit version
ENV FLB_MAJOR 1
ENV FLB_MINOR 6
ENV FLB_PATCH 9
ENV FLB_VERSION 1.6.9

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    cmake \
    make \
    tar \
    libssl-dev \
    libsasl2-dev \
    pkg-config \
    libsystemd-dev \
    libzstd-dev \
    zlib1g-dev \
    libpq-dev \
    postgresql-server-dev-all \
    flex \
    bison \
    git

RUN mkdir -p /fluent-bit/bin /fluent-bit/etc /fluent-bit/log /tmp/src/
RUN cd /tmp/src && \
    echo "Branch: $FLB_MAJOR.$FLB_MINOR" && \
    git clone --depth 1 --branch $FLB_MAJOR.$FLB_MINOR https://github.com/fluent/fluent-bit.git .
RUN rm -rf /tmp/src/build/*

WORKDIR /tmp/src/build/
# If you want to use native Loki plugin, change FLB_OUT_LOKI=Off to On
RUN cmake -DFLB_DEBUG=Off \
          -DFLB_TRACE=Off \
          -DFLB_JEMALLOC=On \
          -DFLB_TLS=On \
          -DFLB_SHARED_LIB=Off \
          -DFLB_EXAMPLES=Off \
          -DFLB_HTTP_SERVER=On \
          -DFLB_IN_SYSTEMD=On \
          -DFLB_OUT_KAFKA=On \
          -DFLB_OUT_LOKI=Off \
          -DFLB_OUT_PGSQL=On ../

RUN make -j $(getconf _NPROCESSORS_ONLN)
RUN install bin/fluent-bit /fluent-bit/bin/

# Configuration files
ENV WD=..
RUN cp -a \
    $WD/conf/fluent-bit.conf \
    $WD/conf/parsers.conf \
    $WD/conf/parsers_ambassador.conf \
    $WD/conf/parsers_java.conf \
    $WD/conf/parsers_extra.conf \
    $WD/conf/parsers_openstack.conf \
    $WD/conf/parsers_cinder.conf \
    $WD/conf/plugins.conf \
    /fluent-bit/etc/

FROM gcr.io/distroless/cc-debian10
LABEL maintainer="Eduardo Silva <eduardo@treasure-data.com>"
LABEL Description="Fluent Bit docker image" Vendor="Fluent Organization" Version="1.1"

COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/*sasl* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libz* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /lib/x86_64-linux-gnu/libz* /lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libssl.so* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libcrypto.so* /usr/lib/x86_64-linux-gnu/

# These below are all needed for systemd
COPY --from=builder_fluent_bit /lib/x86_64-linux-gnu/libsystemd* /lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /lib/x86_64-linux-gnu/libselinux.so* /lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /lib/x86_64-linux-gnu/liblzma.so* /lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/liblz4.so* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /lib/x86_64-linux-gnu/libgcrypt.so* /lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /lib/x86_64-linux-gnu/libpcre.so* /lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /lib/x86_64-linux-gnu/libgpg-error.so* /lib/x86_64-linux-gnu/

# PostgreSQL output plugin
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libpq.so* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libgssapi* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libldap* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libkrb* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libk5crypto* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/liblber* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libgnutls* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libp11-kit* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libidn2* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libunistring* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libtasn1* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libnettle* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libhogweed* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libgmp* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /usr/lib/x86_64-linux-gnu/libffi* /usr/lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /lib/x86_64-linux-gnu/libcom_err* /lib/x86_64-linux-gnu/
COPY --from=builder_fluent_bit /lib/x86_64-linux-gnu/libkeyutils* /lib/x86_64-linux-gnu/

COPY --from=builder_fluent_bit /fluent-bit /fluent-bit

COPY --from=build_loki_plugin /src/loki/cmd/fluent-bit/out_loki.so /fluent-bit/bin
COPY --from=build_prometheus_metrics_plugin /root/fluent-bit-out-prometheus-metrics/out_prometheus_metrics.so /fluent-bit/bin
ADD conf/fluent-bit.conf /fluent-bit/etc/fluent-bit.conf
ADD conf/plugins.conf /fluent-bit/etc/plugins.conf
ADD conf/parsers.conf /fluent-bit/etc/parsers.conf
EXPOSE 2020
EXPOSE 1514
CMD ["/fluent-bit/bin/fluent-bit", "-c", "/fluent-bit/etc/fluent-bit.conf"]
