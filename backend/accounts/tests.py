from rest_framework.test import APITestCase


class SessionTokenTests(APITestCase):
    def test_creates_and_reuses_guest_session(self):
        created = self.client.post('/api/accounts/session/', {}, format='json')
        self.assertEqual(created.status_code, 201)
        token = created.data['session_token']

        reused = self.client.post(
            '/api/accounts/session/',
            {'session_token': token},
            format='json',
        )
        self.assertEqual(reused.status_code, 200)
        self.assertEqual(reused.data['session_token'], token)
