"""Advanced Machine Learning Platform Routes."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import uuid

from dario_app.database import get_db
from dario_app.modules.ml_platform import models
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

router = APIRouter(prefix="/api/ml-platform", tags=["ml_platform"])


# Pydantic Schemas
class MLModelCreate(BaseModel):
    model_name: str
    model_type: str
    algorithm: str
    description: Optional[str] = None


class TrainingPipelineCreate(BaseModel):
    model_id: int
    pipeline_name: str
    dataset_source: str
    train_val_test_split: str = "70/20/10"


class PredictionRequest(BaseModel):
    model_id: int
    input_features: Dict[str, Any]


class FeatureCreate(BaseModel):
    feature_name: str
    feature_type: str
    source_table: str
    source_column: str


class AutoMLExperimentCreate(BaseModel):
    experiment_name: str
    problem_type: str
    target_column: str
    objective: str


# ML Model Management Endpoints
@router.post("/models")
async def create_ml_model(
    model: MLModelCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Register a new ML model."""
    db_model = models.MLModel(
        organization_id=organization_id,
        model_name=model.model_name,
        model_type=model.model_type,
        algorithm=model.algorithm,
        description=model.description,
        version="1.0.0",
        status="training",
    )
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)
    return {"id": db_model.id, "model_name": db_model.model_name, "status": db_model.status}


@router.get("/models")
async def list_ml_models(
    organization_id: int = Query(...),
    model_type: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List ML models."""
    query = db.query(models.MLModel).filter(
        models.MLModel.organization_id == organization_id
    )
    
    if model_type:
        query = query.filter(models.MLModel.model_type == model_type)
    if status:
        query = query.filter(models.MLModel.status == status)
    
    ml_models = await query.all()
    
    deployed_count = sum([1 for m in ml_models if m.status == "deployed"])
    avg_accuracy = sum([m.accuracy_score or 0 for m in ml_models if m.accuracy_score]) / len(ml_models) if ml_models else 0
    
    return {
        "models": ml_models,
        "total": len(ml_models),
        "deployed_count": deployed_count,
        "average_accuracy": avg_accuracy
    }


@router.get("/models/{model_id}")
async def get_ml_model(
    model_id: int,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Get ML model details."""
    model = await db.query(models.MLModel).filter(
        models.MLModel.id == model_id,
        models.MLModel.organization_id == organization_id
    ).first()
    
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return {"model": model}


@router.put("/models/{model_id}/deploy")
async def deploy_ml_model(
    model_id: int,
    environment: str,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Deploy an ML model to production."""
    model = await db.query(models.MLModel).filter(
        models.MLModel.id == model_id,
        models.MLModel.organization_id == organization_id
    ).first()
    
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    model.status = "deployed"
    model.deployed_at = datetime.utcnow()
    model.deployment_endpoint = f"/api/ml-platform/predict/{model_id}"
    
    # Create deployment record
    deployment = models.ModelDeployment(
        organization_id=organization_id,
        model_id=model_id,
        deployment_name=f"{model.model_name}_deployment",
        environment=environment,
        deployment_type="real-time",
        endpoint_url=model.deployment_endpoint,
        deployment_status="active",
        deployed_at=datetime.utcnow(),
        health_status="healthy",
    )
    db.add(deployment)
    
    await db.commit()
    return {"id": model.id, "status": "deployed", "endpoint": model.deployment_endpoint}


# Training Pipeline Endpoints
@router.post("/training-pipelines")
async def create_training_pipeline(
    pipeline: TrainingPipelineCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create and start a training pipeline."""
    db_pipeline = models.TrainingPipeline(
        organization_id=organization_id,
        model_id=pipeline.model_id,
        pipeline_name=pipeline.pipeline_name,
        training_status="running",
        dataset_source=pipeline.dataset_source,
        train_val_test_split=pipeline.train_val_test_split,
        start_time=datetime.utcnow(),
    )
    db.add(db_pipeline)
    await db.commit()
    await db.refresh(db_pipeline)
    return {"id": db_pipeline.id, "status": db_pipeline.training_status}


@router.get("/training-pipelines")
async def list_training_pipelines(
    organization_id: int = Query(...),
    model_id: Optional[int] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List training pipelines."""
    query = db.query(models.TrainingPipeline).filter(
        models.TrainingPipeline.organization_id == organization_id
    )
    
    if model_id:
        query = query.filter(models.TrainingPipeline.model_id == model_id)
    if status:
        query = query.filter(models.TrainingPipeline.training_status == status)
    
    pipelines = await query.all()
    return {"pipelines": pipelines, "total": len(pipelines)}


@router.put("/training-pipelines/{pipeline_id}/complete")
async def complete_training_pipeline(
    pipeline_id: int,
    accuracy: float,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Mark training pipeline as completed."""
    pipeline = await db.query(models.TrainingPipeline).filter(
        models.TrainingPipeline.id == pipeline_id,
        models.TrainingPipeline.organization_id == organization_id
    ).first()
    
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")
    
    pipeline.training_status = "completed"
    pipeline.end_time = datetime.utcnow()
    pipeline.training_metrics = {"accuracy": accuracy}
    
    # Update model with training results
    model = await db.query(models.MLModel).filter(
        models.MLModel.id == pipeline.model_id
    ).first()
    
    if model:
        model.accuracy_score = accuracy
        model.last_trained_at = datetime.utcnow()
        model.status = "trained"
    
    await db.commit()
    return {"id": pipeline.id, "status": "completed", "accuracy": accuracy}


# Prediction Endpoints
@router.post("/predictions")
async def create_prediction(
    request: PredictionRequest,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a prediction request."""
    prediction_id = str(uuid.uuid4())
    
    # Simulate prediction (in production, this would call the actual model)
    prediction_result = {
        "prediction": "positive",
        "probability": 0.85,
        "class_probabilities": {"positive": 0.85, "negative": 0.15}
    }
    
    db_prediction = models.MLPrediction(
        organization_id=organization_id,
        model_id=request.model_id,
        prediction_id=prediction_id,
        input_features=request.input_features,
        prediction_result=prediction_result,
        confidence_score=0.85,
        prediction_type="single",
        processing_time_ms=15.5,
        requested_at=datetime.utcnow(),
    )
    db.add(db_prediction)
    await db.commit()
    await db.refresh(db_prediction)
    
    return {
        "prediction_id": prediction_id,
        "result": prediction_result,
        "confidence": 0.85
    }


@router.get("/predictions")
async def list_predictions(
    organization_id: int = Query(...),
    model_id: Optional[int] = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List predictions."""
    query = db.query(models.MLPrediction).filter(
        models.MLPrediction.organization_id == organization_id
    )
    
    if model_id:
        query = query.filter(models.MLPrediction.model_id == model_id)
    
    predictions = await query.limit(limit).all()
    
    avg_confidence = sum([p.confidence_score or 0 for p in predictions]) / len(predictions) if predictions else 0
    
    return {
        "predictions": predictions,
        "total": len(predictions),
        "average_confidence": avg_confidence
    }


# Feature Store Endpoints
@router.post("/features")
async def create_feature(
    feature: FeatureCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a feature in the feature store."""
    db_feature = models.FeatureStore(
        organization_id=organization_id,
        feature_name=feature.feature_name,
        feature_type=feature.feature_type,
        source_table=feature.source_table,
        source_column=feature.source_column,
    )
    db.add(db_feature)
    await db.commit()
    await db.refresh(db_feature)
    return {"id": db_feature.id, "feature_name": db_feature.feature_name}


@router.get("/features")
async def list_features(
    organization_id: int = Query(...),
    feature_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List features in the feature store."""
    query = db.query(models.FeatureStore).filter(
        models.FeatureStore.organization_id == organization_id
    )
    
    if feature_type:
        query = query.filter(models.FeatureStore.feature_type == feature_type)
    
    features = await query.all()
    return {"features": features, "total": len(features)}


# Model Performance Monitoring Endpoints
@router.get("/performance-metrics")
async def get_performance_metrics(
    organization_id: int = Query(...),
    model_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get model performance metrics."""
    query = db.query(models.ModelPerformanceMetric).filter(
        models.ModelPerformanceMetric.organization_id == organization_id
    )
    
    if model_id:
        query = query.filter(models.ModelPerformanceMetric.model_id == model_id)
    
    metrics = await query.order_by(models.ModelPerformanceMetric.metric_date.desc()).limit(100).all()
    
    if metrics:
        avg_accuracy = sum([m.accuracy or 0 for m in metrics]) / len(metrics)
        drift_detected = sum([1 for m in metrics if m.concept_drift_detected])
        
        return {
            "metrics": metrics,
            "average_accuracy": avg_accuracy,
            "drift_alerts": drift_detected
        }
    
    return {"metrics": [], "average_accuracy": 0, "drift_alerts": 0}


# AutoML Endpoints
@router.post("/automl-experiments")
async def create_automl_experiment(
    experiment: AutoMLExperimentCreate,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create an AutoML experiment."""
    db_experiment = models.AutoMLExperiment(
        organization_id=organization_id,
        experiment_name=experiment.experiment_name,
        problem_type=experiment.problem_type,
        target_column=experiment.target_column,
        objective=experiment.objective,
        experiment_status="running",
        start_time=datetime.utcnow(),
    )
    db.add(db_experiment)
    await db.commit()
    await db.refresh(db_experiment)
    return {"id": db_experiment.id, "status": db_experiment.experiment_status}


@router.get("/automl-experiments")
async def list_automl_experiments(
    organization_id: int = Query(...),
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List AutoML experiments."""
    query = db.query(models.AutoMLExperiment).filter(
        models.AutoMLExperiment.organization_id == organization_id
    )
    
    if status:
        query = query.filter(models.AutoMLExperiment.experiment_status == status)
    
    experiments = await query.all()
    return {"experiments": experiments, "total": len(experiments)}


# Batch Prediction Endpoints
@router.post("/batch-predictions")
async def create_batch_prediction(
    model_id: int,
    batch_name: str,
    input_source: str,
    organization_id: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Create a batch prediction job."""
    db_batch = models.PredictionBatch(
        organization_id=organization_id,
        model_id=model_id,
        batch_name=batch_name,
        batch_status="queued",
        input_data_source=input_source,
    )
    db.add(db_batch)
    await db.commit()
    await db.refresh(db_batch)
    return {"id": db_batch.id, "status": db_batch.batch_status}


@router.get("/batch-predictions")
async def list_batch_predictions(
    organization_id: int = Query(...),
    model_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """List batch prediction jobs."""
    query = db.query(models.PredictionBatch).filter(
        models.PredictionBatch.organization_id == organization_id
    )
    
    if model_id:
        query = query.filter(models.PredictionBatch.model_id == model_id)
    
    batches = await query.all()
    return {"batches": batches, "total": len(batches)}


# Deployment Management Endpoints
@router.get("/deployments")
async def list_deployments(
    organization_id: int = Query(...),
    environment: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List model deployments."""
    query = db.query(models.ModelDeployment).filter(
        models.ModelDeployment.organization_id == organization_id
    )
    
    if environment:
        query = query.filter(models.ModelDeployment.environment == environment)
    
    deployments = await query.all()
    
    active_count = sum([1 for d in deployments if d.deployment_status == "active"])
    
    return {
        "deployments": deployments,
        "total": len(deployments),
        "active_count": active_count
    }


# Health Check
@router.get("/health")
async def health_check():
    """Check ML platform module health."""
    return {
        "status": "healthy",
        "module": "ml_platform",
        "version": "1.0.0",
        "features": [
            "ML Model Registry",
            "Training Pipeline Management",
            "Real-time Predictions",
            "Batch Predictions",
            "Feature Store",
            "AutoML Experiments",
            "Model Performance Monitoring",
            "Model Deployment Management",
            "A/B Testing Support",
            "Data Drift Detection"
        ]
    }
