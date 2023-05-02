from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from .models import Video

class TestVideoList(TestCase):

    def test_all_videos_displayed_in_correct_order(self):

        v1 = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')
        v2 = Video.objects.create(name='ABC', notes='example', url='https://www.youtube.com/watch?v=456')
        v3 = Video.objects.create(name='lmn', notes='example', url='https://www.youtube.com/watch?v=789')
        v4 = Video.objects.create(name='def', notes='example', url='https://www.youtube.com/watch?v=101')

        expected_video_order = [v2, v4, v3, v1]
        response = self.client.get(reverse('video_list'))
        videos_in_template = list(response.context['videos'])
        self.assertEqual(expected_video_order, videos_in_template)

    def test_no_video_message(self):
        response = self.client.get(reverse('video_list'))
        videos_in_template = response.context['videos']
        self.assertContains(response, 'No videos')
        self.assertEquals(0, len(videos_in_template))


class TestVideoModel(TestCase):

    def test_create_id(self):
        video = Video.objects.create(name='example', url='https://www.youtube.com/watch?v=IODxDxX7oi4')
        self.assertEqual('IODxDxX7oi4', video.video_id)

    def test_create_id_valid_url_with_time_parameter(self):
        # a video that is playing and paused may have a timestamp in the query
        video = Video.objects.create(name='example', url='https://www.youtube.com/watch?v=IODxDxX7oi4&ts=14')
        self.assertEqual('IODxDxX7oi4', video.video_id)

    def test_invalid_urls_raise_validation_error(self):
        invalid_video_urls = [
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch/somethingelse',
            'https://www.youtube.com/watch/somethingelse?v=1234567',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch?abc=123',
            'https://www.youtube.com/watch?v=',
            'https://www.youtube.com/watch?v1234',
            'https://github.com',
            '12345678',
            'hhhhhhhhttps://www.youtube.com/watch',
            'http://www.youtube.com/watch/somethingelse?v=1234567',
            'https://minneapolis.edu',
            'https://minneapolis.edu?v=123456'
            ''
        ]

        for invalid_url in invalid_video_urls:
            with self.assertRaises(ValidationError):
                Video.objects.create(name='example', url=invalid_url, notes='example notes')

        video_count = Video.objects.count()
        self.assertEqual(0, video_count)

class TestVideoDetails(TestCase):

    def test_page_shows_video_information(self):
        video = Video.objects.create(name='XYZ', notes='example', url='https://www.youtube.com/watch?v=123')
        response = self.client.get(reverse('video_details', args=[video.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'XYZ')
        self.assertContains(response, 'example')
        self.assertContains(response, 'https://www.youtube.com/watch?v=123')
        self.assertContains(response, '123')
    
    def test_video_that_does_not_exist(self):
        response = self.client.get(reverse('video_details', args=[999999]))
        self.assertEqual(response.status_code, 404)