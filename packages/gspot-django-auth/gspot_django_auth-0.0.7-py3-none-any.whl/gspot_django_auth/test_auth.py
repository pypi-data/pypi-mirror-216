from rest_framework.test import APIClient
from unittest import mock
from .authentication import CustomJWTAuthentication
from .models import DeveloperUser, CustomerUser, AdminUser
from .factory import AdminUserFactory, DeveloperUserFactory, CustomerUserFactory
from unittest import TestCase


class AuthTestCase(TestCase):

    def setUp(self) -> None:
        self.url = '/'
        self.client = APIClient()

    def test_010_get_without_token(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)

    @mock.patch('redis.asyncio.Redis.get')
    def test_020_get_from_headers(self, redis_mock):
        token_config.storage = 'headers'
        admin_data = AdminUserFactory().to_dict()
        admin_data['role'] = 'administrator'
        redis_mock.return_value = json.dumps(admin_data)
        response = self.client.get(self.url, headers={'HTTP_AUTHORIZATION': '12345'})
        self.assertEqual(response.status_code, 200)

    @mock.patch('redis.asyncio.Redis.get')
    def test_020_get_from_cookies(self, redis_mock):
        token_config.storage = 'cookies'
        self.client.cookies.set('Authentication', '123')
        admin_data = AdminUserFactory().to_dict()
        admin_data['role'] = 'administrator'
        redis_mock.return_value = json.dumps(admin_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    # def test_030_get_data_from_redis(self):
    #     customer_data = CustomerUserFactory().to_dict()
    #     customer_data['role'] = 'customer'
    #     token_config.storage = 'cookies'
    #     self.client.cookies.set('Authentication', 'access_token')
    #     redis_client = RedisClient(
    #         token_config.host,
    #         token_config.port,
    #         token_config.db,
    #         token_config.password
    #     )
    #     redis_client = BaseRedis(redis_client.session)
    #     redis_client._put('access_token', customer_data)
    #     response = self.client.get('/')
    #     self.assertEqual(response.status_code, 200)

    # @mock.patch('redis.asyncio.Redis.get')
    def test_040_get_from_cookies(self, redis_mock):
        token_config.storage = 'cookies'
        self.client.cookies.set('Authentication', '123')
        customer_data = CustomerUserFactory().to_dict()
        customer_data['role'] = 'customer'
        redis_mock.return_value = json.dumps(customer_data)
        response = self.client.get(self.customer_url)
        self.assertEqual(response.status_code, 200)

    @mock.patch('redis.asyncio.Redis.get')
    def test_050_test_permissions(self, redis_mock):
        token_config.storage = 'cookies'
        self.client.cookies.set('Authentication', '123')
        admin_data = AdminUserFactory().to_dict()
        admin_data['role'] = 'administrator'
        redis_mock.return_value = json.dumps(admin_data)
        response = self.client.get(self.customer_url)
        self.assertEqual(response.status_code, 403)

    @mock.patch('redis.asyncio.Redis.get')
    def test_060_test_developer(self, redis_mock):
        token_config.storage = 'cookies'
        self.client.cookies.set('Authentication', '123')
        developer_data = DeveloperUserFactory().to_dict()
        developer_data['role'] = 'developer'
        redis_mock.return_value = json.dumps(developer_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)