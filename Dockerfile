# RMLW - Recursive Meta-Learning Workbench
# For authorised lab use only.

FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src/ src/
COPY tests/ tests/

RUN pip install --no-cache-dir ".[dev]"

# TARGET_URL must be set at runtime. Example: docker run -e TARGET_URL=http://dvwa:80 rmlw
# If not set, prints a helpful message and exits.
CMD ["sh", "-c", "if [ -z \"$TARGET_URL\" ]; then echo 'Error: TARGET_URL environment variable is required. Example: docker run -e TARGET_URL=http://localhost:8080 rmlw'; exit 1; fi; rmlw scan --target \"$TARGET_URL\" --mode baseline"]
