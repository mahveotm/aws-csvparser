import os
import boto3
import pytest

from moto import mock_s3, mock_lambda, mock_efs

@pytest.fixture
def aws_credentials():
    """Test credentilas for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"