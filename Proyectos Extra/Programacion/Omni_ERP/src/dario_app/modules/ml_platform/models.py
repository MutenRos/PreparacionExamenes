"""Advanced Machine Learning Platform Models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship

from dario_app.database import Base


class MLModel(Base):
    """Machine learning model registry."""
    
    __tablename__ = "ml_model"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    model_name = Column(String(200), nullable=False)
    model_type = Column(String(50))  # classification, regression, clustering, forecasting, recommendation
    algorithm = Column(String(100))  # random_forest, xgboost, neural_network, linear_regression
    version = Column(String(50))
    description = Column(Text)
    use_case = Column(String(200))  # sales_forecast, churn_prediction, demand_planning
    status = Column(String(50))  # training, deployed, deprecated, archived
    accuracy_score = Column(Float)
    precision_score = Column(Float)
    recall_score = Column(Float)
    f1_score = Column(Float)
    rmse = Column(Float)  # For regression
    mae = Column(Float)  # Mean Absolute Error
    training_data_size = Column(Integer)
    feature_count = Column(Integer)
    hyperparameters = Column(JSON)
    model_artifacts_path = Column(String(500))
    deployment_endpoint = Column(String(500))
    created_by = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_trained_at = Column(DateTime)
    deployed_at = Column(DateTime)


class TrainingPipeline(Base):
    """ML training pipeline execution tracking."""
    
    __tablename__ = "training_pipeline"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    model_id = Column(Integer, ForeignKey("ml_model.id"))
    pipeline_name = Column(String(200))
    training_status = Column(String(50))  # queued, running, completed, failed
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration_seconds = Column(Integer)
    dataset_source = Column(String(500))
    training_samples = Column(Integer)
    validation_samples = Column(Integer)
    test_samples = Column(Integer)
    train_val_test_split = Column(String(50))  # 70/20/10
    cross_validation_folds = Column(Integer)
    feature_engineering_steps = Column(JSON)
    hyperparameter_tuning = Column(Boolean, default=False)
    tuning_method = Column(String(50))  # grid_search, random_search, bayesian
    best_parameters = Column(JSON)
    training_metrics = Column(JSON)
    error_log = Column(Text)
    resource_usage = Column(JSON)  # CPU, memory, GPU usage
    created_at = Column(DateTime, default=datetime.utcnow)


class MLPrediction(Base):
    """Prediction requests and results."""
    
    __tablename__ = "ml_predictions"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    model_id = Column(Integer, ForeignKey("ml_model.id"))
    prediction_id = Column(String(100), unique=True, index=True)
    input_features = Column(JSON)
    prediction_result = Column(JSON)
    confidence_score = Column(Float)
    prediction_type = Column(String(50))  # single, batch, real-time
    processing_time_ms = Column(Float)
    model_version_used = Column(String(50))
    requested_by = Column(String(200))
    requested_at = Column(DateTime, default=datetime.utcnow)
    feedback_provided = Column(Boolean, default=False)
    actual_outcome = Column(String(200))  # For monitoring accuracy
    prediction_correct = Column(Boolean)


class FeatureStore(Base):
    """Feature engineering and storage."""
    
    __tablename__ = "feature_store"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    feature_name = Column(String(200), nullable=False)
    feature_type = Column(String(50))  # numerical, categorical, text, datetime
    data_type = Column(String(50))  # int, float, string, boolean
    description = Column(Text)
    source_table = Column(String(200))
    source_column = Column(String(200))
    transformation_logic = Column(Text)
    aggregation_function = Column(String(50))  # sum, avg, count, max, min
    time_window = Column(String(50))  # last_7_days, last_30_days, lifetime
    is_target_variable = Column(Boolean, default=False)
    importance_score = Column(Float)  # Feature importance
    correlation_with_target = Column(Float)
    missing_value_strategy = Column(String(50))  # mean, median, mode, drop, fill
    outlier_handling = Column(String(50))  # clip, remove, winsorize
    encoding_method = Column(String(50))  # one_hot, label, target, ordinal
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ModelPerformanceMetric(Base):
    """Model performance monitoring over time."""
    
    __tablename__ = "model_performance_metric"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    model_id = Column(Integer, ForeignKey("ml_model.id"))
    metric_date = Column(DateTime, default=datetime.utcnow)
    predictions_count = Column(Integer)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    auc_roc = Column(Float)
    confusion_matrix = Column(JSON)
    data_drift_score = Column(Float)  # Measure of distribution drift
    concept_drift_detected = Column(Boolean, default=False)
    average_confidence = Column(Float)
    error_rate = Column(Float)
    latency_p50_ms = Column(Float)
    latency_p95_ms = Column(Float)
    latency_p99_ms = Column(Float)
    retraining_recommended = Column(Boolean, default=False)
    alert_triggered = Column(Boolean, default=False)
    notes = Column(Text)


class AutoMLExperiment(Base):
    """Automated machine learning experiments."""
    
    __tablename__ = "automl_experiment"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    experiment_name = Column(String(200))
    objective = Column(String(50))  # maximize_accuracy, minimize_rmse, maximize_f1
    problem_type = Column(String(50))  # classification, regression, clustering
    dataset_id = Column(String(200))
    target_column = Column(String(200))
    experiment_status = Column(String(50))  # running, completed, failed
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    total_trials = Column(Integer)
    best_trial_id = Column(Integer)
    best_model_type = Column(String(100))
    best_score = Column(Float)
    algorithms_tested = Column(JSON)  # List of algorithms tried
    best_hyperparameters = Column(JSON)
    feature_selection_method = Column(String(50))  # recursive, lasso, tree-based
    selected_features = Column(JSON)
    cross_validation_strategy = Column(String(50))
    optimization_time_limit_minutes = Column(Integer)
    resource_constraints = Column(JSON)
    experiment_config = Column(JSON)
    leaderboard = Column(JSON)  # Top N models with scores
    created_by = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)


class PredictionBatch(Base):
    """Batch prediction jobs."""
    
    __tablename__ = "prediction_batch"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    model_id = Column(Integer, ForeignKey("ml_model.id"))
    batch_name = Column(String(200))
    batch_status = Column(String(50))  # queued, processing, completed, failed
    input_data_source = Column(String(500))
    output_data_destination = Column(String(500))
    total_records = Column(Integer)
    processed_records = Column(Integer)
    failed_records = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    average_confidence = Column(Float)
    predictions_summary = Column(JSON)
    error_log = Column(Text)
    requested_by = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)


class ModelDeployment(Base):
    """Model deployment tracking."""
    
    __tablename__ = "model_deployment"

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, nullable=False, index=True)
    model_id = Column(Integer, ForeignKey("ml_model.id"))
    deployment_name = Column(String(200))
    environment = Column(String(50))  # development, staging, production
    deployment_type = Column(String(50))  # real-time, batch, edge
    endpoint_url = Column(String(500))
    deployment_status = Column(String(50))  # deploying, active, inactive, failed
    instance_type = Column(String(100))  # CPU, GPU configuration
    scaling_config = Column(JSON)  # min/max instances, auto-scaling rules
    traffic_percentage = Column(Float)  # For A/B testing
    requests_per_second = Column(Integer)
    average_latency_ms = Column(Float)
    error_rate = Column(Float)
    deployed_by = Column(String(200))
    deployed_at = Column(DateTime)
    last_health_check = Column(DateTime)
    health_status = Column(String(50))  # healthy, degraded, unhealthy
    monitoring_enabled = Column(Boolean, default=True)
    alerts_config = Column(JSON)
