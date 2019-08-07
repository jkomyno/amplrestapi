FROM jkomyno/ampl-python

# Set the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy the sources in the working Directory
COPY . /app

# Expose the 9001 TCP port
EXPOSE 9001

# Run the amplrestapi Python module
CMD python -m amplrestapi
