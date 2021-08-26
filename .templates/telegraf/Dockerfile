# Download base image
FROM telegraf:latest

# Add support tool
RUN apt update && apt install -y rsync

# where IOTstack template files are stored
ENV IOTSTACK_DEFAULTS_DIR="iotstack_defaults"

# make a copy of the default config file
RUN mkdir -p /${IOTSTACK_DEFAULTS_DIR} && \
    cp /etc/telegraf/telegraf.conf /${IOTSTACK_DEFAULTS_DIR}/

# replace the docker entry-point script with a self-repairing version
ENV IOTSTACK_ENTRY_POINT="entrypoint.sh"
COPY ${IOTSTACK_ENTRY_POINT} /${IOTSTACK_ENTRY_POINT}
RUN chmod 755 /${IOTSTACK_ENTRY_POINT}
ENV IOTSTACK_ENTRY_POINT=

# IOTstack declares this path for persistent storage
VOLUME ["/etc/telegraf"]

# EOF
