# Reproducible local MLOps pipeline

The initial JSON scenario engine has now been supplemented with actual deterministic training and a portable JSON model artifact.

```bash
cd projects/end-to-end-mlops-pipeline
bash scripts/pipeline.sh
```

Stages: CSV ingestion -> fixed 80/20 split (every fifth observation held out) -> ordinary least squares training -> MAE evaluation -> model JSON export -> SHA256 provenance of training data -> inference from versioned model artifact.

The sample data follows `y=2x+1`, so a proper implementation should predict `25` for `x=12`. Four independent tests check coefficients, artifact validity, prediction and degenerate datasets.

## What is not yet present

MLflow/experiment server, model registry, feature store, retraining scheduler, model deployment pipeline, production feature monitoring and real-world dataset shift handling. Docker deployment of the project evaluation API is separate from the ML training pipeline. The training pipeline itself runs locally using Python only and has no cloud charges.
