FROM python:3.11

# Set the home directory to /root
ENV HOME /root
# cd into the home directory 
WORKDIR /root

# Copying files into image
COPY . .

# Installing Dependecies 
RUN pip install -r requirements.txt

# Exposing port 8080
EXPOSE 8080

# Run the app
CMD python -u server.py