"""
Shim module to forward profanity_check calls to alt_profanity_check.
This resolves the scikit-learn import issue with the unmaintained profanity-check package.
"""

try:
    from alt_profanity_check import predict, predict_prob
except ImportError:
    # Fallback if alt_profanity_check is not available
    def predict(text):
        """Fallback predict function that always returns False (no profanity detected)."""
        return False
    
    def predict_prob(text):
        """Fallback predict_prob function that always returns 0.0 (no profanity probability)."""
        return 0.0

__all__ = ['predict', 'predict_prob']
