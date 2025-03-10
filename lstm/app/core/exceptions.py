class LSTMError(Exception):
    """Base exception for LSTM API."""
    pass

class ModelNotFoundError(LSTMError):
    """Raised when a model is not found."""
    pass

class TrainingError(LSTMError):
    """Raised when there's an error during training."""
    pass

class EvaluationError(LSTMError):
    """Raised when there's an error during evaluation."""
    pass

class DataProcessingError(LSTMError):
    """Raised when there's an error processing data."""
    pass 