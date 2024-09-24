FROM python:3.10

# Set the home directory to /root
ENV HOME /root
# cd into the home directory 
WORKDIR /root

# Copying files into image
COPY . .

# Installing Dependecies 
RUN pip3 install -r requirements.txt

# Exposing port 8080
EXPOSE 8080

# Run the app
CMD /wait && python -u server.py