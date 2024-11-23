"""
Module to test the module
"""

from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse


class GetCookieTestCase(TestCase):
    """
    Test case for verifying the cookie retrieval view.

    This test checks whether the view correctly returns a response
    containing the expected cookie value.
    """

    def test_get_cookie_view(self) -> None:
        """
        Test the cookie retrieval view.

        Sends a GET request to the 'cookie-get' URL and asserts that
        the response contains the expected cookie value.

        Asserts:
            Contains the string "Cookie value" in the response.
        """
        response: HttpResponse = self.client.get(reverse("myauth:cookie-get"))
        self.assertContains(response, "Cookie value")


class FooBarViewTest(TestCase):
    """
    Test case for verifying the FooBar view.

    This test checks whether the view returns a successful response
    with the correct content type and JSON data.
    """

    def test_foo_bar_view(self) -> None:
        """
        Test the FooBar view.

        Sends a GET request to the 'foo-bar' URL and asserts that
        the response status code is 200, the content type is
        'application/json', and the JSON data matches expected values.

        Asserts:
            Response status code is 200.
            Response content type is 'application/json'.
            Response JSON data matches expected values.
        """
        response: HttpResponse = self.client.get(reverse("myauth:foo-bar"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("content-type"),
            "application/json",
        )

        expected_data: dict = {"foo": "bar", "spam": "eggs"}

        self.assertJSONEqual(response.content, expected_data)
