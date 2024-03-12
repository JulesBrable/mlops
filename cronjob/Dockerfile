# Use Alpine Linux as the base image for a lightweight container
FROM alpine:latest

WORKDIR ${HOME}/mlops/cronjob

# Install curl, jq, and bash
RUN apk add --no-cache curl jq bash

# Download and install the MinIO Client (mc)
ADD https://dl.min.io/client/mc/release/linux-amd64/mc /usr/bin/mc
RUN chmod +x /usr/bin/mc

RUN pip install -r requirements.txt

# Add script to the container with permissions
COPY . .
RUN chmod +x /get_data.sh

CMD ["/get_data.sh"]
