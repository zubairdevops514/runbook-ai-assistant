FROM python:3.13-slim
WORKDIR /app
RUN useradd --create-home worker
COPY --chown=worker:worker runbook.py evaluate.py ./
COPY --chown=worker:worker runbooks ./runbooks
USER worker
ENTRYPOINT ["python", "runbook.py"]
CMD ["Why is my pod in CrashLoopBackOff?"]
