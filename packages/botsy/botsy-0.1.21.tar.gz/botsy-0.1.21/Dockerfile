# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in pyproject.toml
RUN apt-get update && \
    apt-get install -y portaudio19-dev && \
    pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

ARG PYPI_USERNAME
ARG PYPI_PASSWORD
ENV PYPI_USERNAME=${PYPI_USERNAME}
ENV PYPI_PASSWORD=${PYPI_PASSWORD}

# NOTE This may not get used...
# RUN printf "[pypi]\nusername = %s\npassword = %s\n\n[testpypi]\nusername = %s\npassword = %s\n" \
#     "$PYPI_USERNAME" "$PYPI_PASSWORD" "$PYPI_USERNAME" "$PYPI_PASSWORD" > /root/.pypirc

# RUN chmod 600 /root/.pypirc

# Make port 80 available to the world outside this container
EXPOSE 80

# Run entrypoint.sh when the container launches
CMD ["/app/entrypoint.sh"]
