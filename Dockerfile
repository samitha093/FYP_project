# Use the Ubuntu 22 base image
FROM ubuntu:22.04

# Copy the .bin file into the container
COPY C_main.bin /app/C_main.bin

# Set the working directory
WORKDIR /app

# Set execute permission for the .bin file
RUN chmod +x C_main.bin

# Define the entry point to run the .bin file
ENTRYPOINT ["./C_main.bin"]