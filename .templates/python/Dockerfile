FROM python:3

# user+group ID defaults for IOTstack
ENV IOTSTACK_UID=1000
ENV IOTSTACK_GID=1000

# the template folder is named
ENV TEMPLATE="app"

# where IOTstack template files are stored
ENV PYTHON_DEFAULTS="/iotstack_defaults/${TEMPLATE}"

# ensure the defaults directory exists
RUN mkdir -p ${PYTHON_DEFAULTS}

# copy template files to defaults directory in image
COPY ${TEMPLATE} ${PYTHON_DEFAULTS}

# the requirements file (if it exists) is
ENV REQUIREMENTS="${PYTHON_DEFAULTS}/requirements.txt"

# set up requirements (if the file exists)
RUN if [ -e ${REQUIREMENTS} ] ; then pip3 install --no-cache-dir -r ${REQUIREMENTS} ; fi

# the python working directory is 
ENV PYTHON_WORKDIR="/usr/src/${TEMPLATE}"

# ensure the working directory exists
RUN mkdir -p ${PYTHON_WORKDIR}

# add an entry-point script
ENV ENTRY_POINT="docker-entrypoint.sh"
COPY ${ENTRY_POINT} /${ENTRY_POINT}
RUN chmod 755 /${ENTRY_POINT}

# unset variables that are not needed
ENV TEMPLATE=
ENV REQUIREMENTS=
ENV ENTRY_POINT=

# set the working directory
WORKDIR ${PYTHON_WORKDIR}

# away we go
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["/usr/local/bin/python", "./app.py"]

# EOF
