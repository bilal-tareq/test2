FROM python:3.10

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy files
COPY --chown=user . $HOME/app

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 7860

# Run the app with gunicorn
CMD ["gunicorn", "supercareer.wsgi:application", "--bind", "0.0.0.0:7860"]
