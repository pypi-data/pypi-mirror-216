import io
import base64
import logging
import requests
from typing import Any, Dict, Optional, Union
from PIL import Image, UnidentifiedImageError
from mutagen.mp4 import MP4  # type: ignore
from drf_extra_fields import fields  # type: ignore
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ObjectDoesNotExist
from rest_flex_fields import FlexFieldsModelSerializer  # type: ignore
from rest_framework import serializers
from rest_framework.serializers import *  # Import everything so that this file is enough to access DRF stuffs
from ..misc import resolve_environment


class RelatedModelSerializer(FlexFieldsModelSerializer):
    """
    Base model serializer which can also be used as a relation field of another serializer. DRF
    separates relation fields from the regular fields of a serializer, but the main difference between
    both from the API'sperspective is that a relation field takes "queryset" parameter. They also differ
    implementation wise in that the to_internal_value method returns an instance of the model in relation
    field while it doesn't for non-relation field. So this class allows model serializer class to be passed
    a queryset parameter to imply that it is being used a relation field.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.queryset = kwargs.pop("queryset", None)
        self.primary_key = kwargs.pop("primary_key", None)
        super().__init__(*args, **kwargs)

    def run_validators(self, value: Any) -> None:
        """
        Serializer inherits from Field and override this method to transform *value* into an iterable
        obviouly because a Serializer contains an iterable of fields. However, if this model is being
        used as a relation field, we expect value to be a non-iterable. In that case, we should call
        the Field.run_validators method instead of Serializer.run_validators
        """

        if self.queryset is None:
            return super().run_validators(value)

        return super(serializers.Serializer, self).run_validators(value)  # type: ignore

    def to_internal_value(self, data: Dict[str, Any]) -> Any:
        if self.queryset is None:
            return super().to_internal_value(data)

        if not isinstance(data, dict):
            message = "Invalid data type. Expected a dict but found {}".format(
                type(data)
            )
            raise serializers.ValidationError(message)

        if self.primary_key not in data:
            return super().to_internal_value(data)

        try:
            return self.queryset.get(**{self.primary_key: data[self.primary_key]})
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                f"Invalid {self.primary_key}. Object does not exist"
            )


class Base64MediaField(fields.Base64FileField):
    ALLOWED_TYPES = ("jpeg", "jpg", "png", "gif", "webp", "svg", "mp4")

    def get_file_extension(self, filename: str, decoded_file: bytes) -> Optional[str]:
        # First see if this is an image
        try:
            image = Image.open(io.BytesIO(decoded_file))
            if image.format is not None:
                return image.format.lower()
        except (UnidentifiedImageError, TypeError):
            pass

        # See if this is a video instead
        try:
            MP4(io.BytesIO(decoded_file))
            return "mp4"
        except Exception as exc:
            logging.exception(str(exc))
            return None

    def to_internal_value(self, data: Any) -> Union[Any, None]:
        if isinstance(data, SimpleUploadedFile):
            return super(fields.Base64FieldMixin, self).to_internal_value(data)

        if isinstance(data, str) and data.startswith("http"):
            # Note that we are disabling ssl verification to avoid failures. We don't
            # have control to the host SSL certificate so skipping verification makes
            # sense as we only interested in downloading the relevant file. To avoid
            # urlib3 from complaining in tests, however, we are enabling ssl verification
            # only in testing mode.
            is_testing = resolve_environment() == "testing"
            downloaded_data = requests.get(data, verify=is_testing).content
            return super().to_internal_value(
                base64.b64encode(downloaded_data).decode("utf-8")
            )

        return super().to_internal_value(data)
