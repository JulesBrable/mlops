# Use Alpine Linux as the base image for a lightweight container
FROM alpine:latest

WORKDIR ${HOME}/mlops/cronjob

RUN apk add --no-cache curl jq bash python3 python3-pip

# Download and install the MinIO Client (mc)
ADD https://dl.min.io/client/mc/release/linux-amd64/mc /usr/bin/mc
RUN chmod +x /usr/bin/mc

COPY . .
RUN dir -s
RUN pip install -r requirements.txt

# Add permissions
RUN chmod +x /get_data.sh

CMD ["/get_data.sh"]
