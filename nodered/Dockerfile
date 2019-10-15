FROM nodered/node-red:latest
#node red install script instpired from https://tech.scargill.net/the-script/
RUN for addonnodes in \
node-red-node-pi-gpiod \
node-red-dashboard \
; do \
npm install ${addonnodes} ;\
done;
