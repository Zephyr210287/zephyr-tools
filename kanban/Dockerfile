FROM python:3.11-slim

WORKDIR /app

# Copy application files
COPY server.py .
COPY index.html .

# Create data directory
RUN mkdir -p data

# Set environment variables
ENV KANBAN_DATA_FILE=/app/data/cards.json
ENV KANBAN_PORT=8744

# Expose port
EXPOSE 8744

# Run server
CMD ["python3", "server.py"]
