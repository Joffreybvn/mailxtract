import email
from email.message import Message
from ..exceptions import Boto3Missing

# Optionally import boto3
try:
    import boto3
except ImportError:
    boto3 = None


class MessageReader:
    """Base MessageReader class.
    Implement a 'message' method used by the extractor to get a Message object.
    """

    def __init__(self, message: Message):
        self._message: Message = message

    @classmethod
    def from_bytes(cls, bytes_object: bytes) -> 'MessageReader':
        """Create a MessageReader object from a bytes object"""
        message = email.message_from_bytes(bytes_object)
        return cls(message)

    @classmethod
    def from_file(cls, file_path: str) -> 'MessageReader':
        """Create a MessageReader object from a local file."""
        with open(file_path, mode='rb') as file:
            return cls.from_bytes(file.read())

    @property
    def message(self) -> Message:
        return self._message


class SESMessage(MessageReader):
    """
    SES Message reader. Extract message object created by SES.
    """

    # S3 client
    s3 = boto3.client('s3')

    def __new__(cls, *args, **kwargs) -> 'SESMessage':
        # Raise an error if boto3 is not installed
        if boto3 is None:
            raise Boto3Missing(
                "boto3 library is missing. Please install boto3, or use"
                "another message reader."
            )
        return super().__new__(cls)

    def __init__(self, message: Message):
        super().__init__(message)

    @classmethod
    def from_s3(cls, bucket: str, key: str) -> 'SESMessage':
        """Create a SESMessage object from a S3 bucket and key name."""
        response: dict = cls.s3.get_object(Bucket=bucket, Key=key)
        bytes_object: bytes = response['Body'].read()

        return cls.from_bytes(bytes_object)
