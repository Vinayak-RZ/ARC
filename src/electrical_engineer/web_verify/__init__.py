"""External-context verification before checked labels."""

from electrical_engineer.web_verify.config import WebVerifyConfig, load_web_verify_config
from electrical_engineer.web_verify.engine import run_web_verify

__all__ = ["WebVerifyConfig", "load_web_verify_config", "run_web_verify"]
