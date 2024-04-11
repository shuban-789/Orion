FROM python:3.9 
ADD src/server.py .
RUN pip install requests beautifulsoup4 python-dotenv
CMD [“python”, “src/server.py”] 
EXPOSE 8080
