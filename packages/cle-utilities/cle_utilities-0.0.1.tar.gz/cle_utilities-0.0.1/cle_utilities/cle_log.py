import requests
from datetime import datetime, tzinfo, timedelta


class SimpleUtc(tzinfo):
    def tzname(self, **kwargs):
        return "UTC"

    def utcoffset(self, dt):
        return timedelta(0)


class CleLogging:
    def get_current_timestamp(self):
        timestamp = datetime.utcnow().replace(tzinfo=SimpleUtc()).isoformat()
        return timestamp

    def cle_send_request(self, cle_url, cle_log_request, okta_token, certificate, logger=None):
        try:
            print("CLE Payload: \n", cle_log_request)
            response = requests.post(cle_url, json=cle_log_request,
                                     headers={"Authorization": okta_token, "Content-Type": "application/json"},
                                     verify=certificate)
            logger.info("Status Code: " + str(response.status_code))
            logger.info("CLE Response: " + response.text)
        except Exception as err:
            logger.debug("CLE Exception: " + str(err))
