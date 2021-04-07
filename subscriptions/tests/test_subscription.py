from django.test import TestCase
from django.core.validators import ValidationError

from subscription.models import Subscription
from core.tests.sample_objects import get_sample_user, get_sample_community


class SubscriptionModelTests(TestCase):
    """Subscriptiom model tests"""

    def test_create_subscription_success(self):
        """Test creating a new subsctoption successfully"""

        subscriber = get_sample_user()
        community = get_sample_community()

        subscription = Subscription.objects.create(
            subscriber=subscriber, community=community
        )

        self.assertEqual(subscription.subscriber, subscriber)
        self.assertEqual(subscription.community, community)

    def test_create_subscription_invalid_field(self):
        subscriber = get_sample_user()
        community = None

        with self.assertRaises(ValidationError):
            Subscription.objects.create(subscriber=subscriber, community=community)
