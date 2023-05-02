from django.db import models
from urllib import parse
from django.core.exceptions import ValidationError

class Video(models.Model):
    # Fields for model
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True)
    video_id = models.CharField(max_length=40, unique=True)

    # Method to save video
    def save(self, *args, **kwargs):
        try:
            # Get url components
            url_components = parse.urlparse(self.url)
            # Raise error if url is invalid
            if url_components.scheme != 'https' or url_components.netloc != 'www.youtube.com' or url_components.path != '/watch':
                raise ValidationError(f'Invalid YouTube URL {self.url}')

            # Get query from url
            query_string = url_components.query
            # Raise error if query doesn't exist
            if not query_string:
                raise ValidationError(f'Invalid YouTube URL {self.url}')
            # Get parameters from query
            parameters = parse.parse_qs(query_string, strict_parsing=True)
            parameter_list = parameters.get('v')
            # Raise error if parameters don't exist
            if not parameter_list:
                raise ValidationError(f'Invalid YouTube URL parameters {self.url}')
            # Get video id
            self.video_id = parameter_list[0]
        except ValueError as e:
            raise ValidationError(f'Unable to parse URL {self.url}') from e
        
        super().save(*args, **kwargs)

    # String to print model
    def __str__(self):
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, \
            Video ID: {self.video_id}, Notes: {self.notes}'