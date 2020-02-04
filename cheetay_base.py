class CheetayBase(object):
    """
    Base class for Locust.
    """

    def __init__(self, hostname, client):
        """
        Initialize the client.
        :param hostname: The hostname of the test server, sent as the "Referer" HTTP header.
        :param client: The test client used by locust.
        """
        self.hostname = hostname
        self.client = client

        self.default_headers = {
            u'Accept': u'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            u'Authorization': u'Basic bWNraW5zZXk6YWNhZGVteQ==',
            u'Connection': u'keep-alive',
        }


    def _check_response(self, response):
        """
        Check whether a response was successful.
        """
        if response.status_code != 200:
            raise Exception(
                'API request failed with following error code: ' +
                str(response.status_code)
            )

    def _check_response_data(self, response):
        """
        Check whether a response was successful.
        """
        if response.status_code != 200:
            raise Exception(
                'API request failed with following error code: ' +
                str(response.status_code)
            )

        page_response = response.text
        try:
            assert '"status":true' in page_response
        except:
            raise Exception("Page response is not correct")