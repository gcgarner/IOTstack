# supported build argument
ARG DEBIAN_VARIANT=bullseye-slim

# Download base image
FROM debian:${DEBIAN_VARIANT}

# re-reference supported argument and copy to environment var
ARG DEBIAN_VARIANT
ENV DEBIAN_VARIANT=${DEBIAN_VARIANT}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Refer https://github.com/jacksonliam/mjpg-streamer/issues/386
# This assumes a Debian build and references:
#     libjpeg62-turbo-dev
# For Ubuntu, replace with:
#     libjpeg8-dev

# acknowledgement: mostly borrowed from https://github.com/Cossey/docker
RUN apt-get -q -y update \
 && apt-get -q -y -o "DPkg::Options::=--force-confold" -o "DPkg::Options::=--force-confdef" install apt-utils \
 && rm -rf /etc/dpkg/dpkg.cfg.d/excludes \
 && apt-get -q -y -o "DPkg::Options::=--force-confold" -o "DPkg::Options::=--force-confdef" install \
       cmake \
       git \
       gcc \
       g++ \
       libjpeg62-turbo-dev \
       tzdata \
       uuid-runtime \
 && apt-get -q -y autoremove \
 && apt-get -q -y clean \
 && rm -rf /var/lib/apt/lists/* \
 && git clone https://github.com/jacksonliam/mjpg-streamer.git /usr/src/mjpg-streamer \
 && make -C /usr/src/mjpg-streamer/mjpg-streamer-experimental \
 && make -C /usr/src/mjpg-streamer/mjpg-streamer-experimental install \
 && rm -rf /usr/src/mjpg-streamer \
 && apt-get -q -y -o "DPkg::Options::=--force-confold" -o "DPkg::Options::=--force-confdef" purge \
       cmake \
       git \
       gcc \
       g++

# set up the container start point
ENV ENTRYPOINT_SCRIPT="docker-entrypoint.sh"
COPY docker-entrypoint.sh /usr/local/bin
RUN chmod 755 /usr/local/bin/docker-entrypoint.sh

# starting point - self-repair (if ever needed) and launch
ENTRYPOINT ["docker-entrypoint.sh"]

# the streamer invocation
CMD mjpg_streamer \
    -i "/usr/local/lib/mjpg-streamer/input_uvc.so -d ${MJPG_STREAMER_INTERNAL_DEVICE} -n -f ${MJPG_STREAMER_FPS} -r ${MJPG_STREAMER_SIZE}" \
    -o "/usr/local/lib/mjpg-streamer/output_http.so -p 80 -w /usr/local/share/mjpg-streamer/www ${MJPG_STREAMER_CREDENTIALS}"

# set root's home directory as default (probably unnecessary)
WORKDIR /root

# port
EXPOSE "80"

# set container metadata
LABEL com.github.SensorsIot.IOTstack.Dockerfile.build-args="${DEBIAN_VARIANT}"
LABEL com.github.SensorsIot.IOTstack.Dockerfile.maintainer="Paraphraser <34226495+Paraphraser@users.noreply.github.com>"

# EOF
