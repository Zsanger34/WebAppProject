FROM python:3.8 

# Set the home directory to /root
ENV HOME /root
# cd into the home directory 
WORKDIR /root

# Copying files into image
COPY . .

# Installing Dependecies 
RUN pip install --no-cache-dir -r requirements.txt

# Exposing port 8080
EXPOSE 8080

# Run the app
CMD python3 -u server.py