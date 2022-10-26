FROM python:3.10

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PROJECT_DIR /usr/local/bin/luxsoft

# Install pipenv
RUN pip install pipenv

# Create project directory
WORKDIR ${PROJECT_DIR}

# Copy project
COPY TestProject ${PROJECT_DIR}/

# Install dependencies
RUN pipenv install --system --deploy