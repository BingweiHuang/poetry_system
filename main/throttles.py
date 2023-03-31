from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class AnonWriteRateThrottle(AnonRateThrottle):
    THROTTLE_RATES = {"anon": "5/min"}

class AnonReadRateThrottle(AnonRateThrottle):
    THROTTLE_RATES = {"anon": "10/min"}

class UserWriteRateThrottle(UserRateThrottle):
    THROTTLE_RATES = {"user": "15/min"}

class UserReadRateThrottle(UserRateThrottle):
    THROTTLE_RATES = {"user": "30/min"}

class AnonEmailRateThrottle(AnonRateThrottle):
    THROTTLE_RATES = {"anon": "1/min"}

class UserEmailRateThrottle(UserRateThrottle):
    THROTTLE_RATES = {"user": "1/min"}