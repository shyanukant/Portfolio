# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install virtualenv
RUN pip install --no-cache-dir virtualenv

# Create a virtual environment
RUN virtualenv venv

# Activate the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Install app dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app's code to the container
COPY . .

COPY sshd_config /etc/ssh/

# Start and enable SSH
RUN apt-get update \
    && apt-get install -y --no-install-recommends dialog \
    && apt-get install -y --no-install-recommends openssh-server \
    && echo "root:Docker!" | chpasswd \
    && chmod u+x /app/init_container.sh

EXPOSE 8000 2222

ENTRYPOINT [ "/app/container.sh" ] 