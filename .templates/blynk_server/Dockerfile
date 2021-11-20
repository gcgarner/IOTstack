# Acknowledgements:
#   Based on:
#    https://github.com/SensorsIot/IOTstack/blob/master/.templates/blynk_server/Dockerfile
#      (as at commit ID 4dff89c1bb6a5b1c01d3c087dcb662256a0c050f)
#   Borrows from:
#    https://github.com/Peterkn2001/blynk-server/blob/master/server/Docker/Dockerfile
#      (as at commit ID 889c7e55161832e21264d993d9fa5abd1c015e1c)

FROM ubuntu

# declare the version to be built, defaulting to 0.41.16 (which is
# current as of 2021-10-22)
ARG BLYNK_SERVER_VERSION=0.41.16

# form the download URL
ENV BLYNK_SERVER_URL=https://github.com/Peterkn2001/blynk-server/releases/download/v${BLYNK_SERVER_VERSION}/server-${BLYNK_SERVER_VERSION}.jar

# Add support packages to the base image
RUN apt-get update \
 && apt-get install -y \
      apt-utils \
      libreadline8 \
      libreadline-dev \
 && apt-get install -y \
      curl \
      libxrender1 \
      maven \
      openjdk-11-jdk \
      rsync

# Add IOTstack-specific support
ENV IOTSTACK_DEFAULTS_DIR="iotstack_defaults"
ENV IOTSTACK_ENTRY_POINT="docker-entrypoint.sh"
COPY ${IOTSTACK_DEFAULTS_DIR} /${IOTSTACK_DEFAULTS_DIR}
COPY ${IOTSTACK_ENTRY_POINT} /${IOTSTACK_ENTRY_POINT}
RUN chmod 755 /${IOTSTACK_ENTRY_POINT}

# define well-known paths
ENV IOTSTACK_DATA_DIR="/data"
ENV IOTSTACK_CONF_DIR="/config"
ENV IOTSTACK_JAVA_DIR="/blynk"

# Create and populate expected folders
RUN mkdir -p ${IOTSTACK_DATA_DIR} ${IOTSTACK_JAVA_DIR} \
 && curl -L ${BLYNK_SERVER_URL} >"${IOTSTACK_JAVA_DIR}/server.jar"

# declare expected mapped volumes
VOLUME ["${IOTSTACK_CONF_DIR}", "${IOTSTACK_DATA_DIR}"]

# Expose assumed internal ports:
#   8080 http.port
#   8440 hardware.mqtt.port
#   9443 https.port
EXPOSE 8080 8440 9443

# set the working directory
WORKDIR ${IOTSTACK_DATA_DIR}

# define launch procedure
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["java", "-jar", "/blynk/server.jar", "-dataFolder", "/data", "-serverConfig", "/config/server.properties", "-mailConfig", "/config/mail.properties"]

# supplement image metadata
LABEL blynk-server.version=${BLYNK_SERVER_VERSION}
LABEL blynk-server.url=${BLYNK_SERVER_URL}
LABEL com.github.SensorsIot.IOTstack.Dockerfile.maintainer="877dev <877dev@gmail.com>"
LABEL com.github.Peterkn2001.blynk-server.Dockerfile.maintainer="Florian Mauduit <f@lf.je>"

# unset variables that are not needed by docker-entrypoint.sh
ENV IOTSTACK_ENTRY_POINT=
ENV IOTSTACK_DATA_DIR=
ENV IOTSTACK_JAVA_DIR=
ENV BLYNK_SERVER_URL=

# EOF
