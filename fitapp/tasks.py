import logging
import sys

from celery import shared_task
from celery.exceptions import Ignore, Reject
from dateutil import parser
from django.core.cache import cache
from fitbit.exceptions import HTTPTooManyRequests

from . import utils
from .models import UserFitbit, TimeSeriesData, TimeSeriesDataType


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
hdlr = logging.FileHandler('./tracktivitypets_celerylog.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

LOCK_EXPIRE = 60 * 5 # Lock expires in 5 minutes

## Broker settings.
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

@shared_task
def subscribe(fitbit_user, subscriber_id):
    """ Subscribe to the user's fitbit data """

    logging.debug("Attemping to subscribe fitbit user: %s" % str(fitbit_user))

    fbusers = UserFitbit.objects.filter(fitbit_user=fitbit_user)
    for fbuser in fbusers:
        fb = utils.create_fitbit(**fbuser.get_user_data())
        try:
            fb.subscription(fbuser.user.id, subscriber_id)
            logger.debug("New subscriber: UserId: %s SubscriberId: %s" % (fbuser.user.id, subscriber_id))
        except:
            exc = sys.exc_info()[1]
            logger.error("Error subscribing user: %s" % exc)
            raise Reject(exc, requeue=False)

    logging.debug("Successfully subscribed fitbit user: %s" % str(fitbit_user))


@shared_task
def unsubscribe(*args, **kwargs):
    """ Unsubscribe from a user's fitbit data """

    logging.debug("Attemping to unsubscribe fitbit user")

    fb = utils.create_fitbit(**kwargs)
    try:
        for sub in fb.list_subscriptions()['apiSubscriptions']:
            if sub['ownerId'] == kwargs['user_id']:
                fb.subscription(sub['subscriptionId'], sub['subscriberId'],
                                method="DELETE")
                logger.debug("User subscribed: UserId: %s SubscriberId:%s" % (kwargs['user_id'], sub['subscriberId']))
    except:
        exc = sys.exc_info()[1]
        logger.error("Error unsubscribing user: %s" % exc)
        raise Reject(exc, requeue=False)

    logging.debug("Successfully unsubscribed fitbit user")



@shared_task
def get_time_series_data(fitbit_user, cat, resource, date=None):
    """ Get the user's time series data """

    logger.debug("Get time series data for %s" % str(fitbit_user))

    try:
        _type = TimeSeriesDataType.objects.get(category=cat, resource=resource)
    except TimeSeriesDataType.DoesNotExist:
        logger.error("The resource %s in category %s doesn't exist" % (
            resource, cat))
        raise Reject(sys.exc_info()[1], requeue=False)

    # Create a lock so we don't try to run the same task multiple times
    sdat = date.strftime('%Y-%m-%d') if date else 'ALL'
    lock_id = '{0}-lock-{1}-{2}-{3}'.format(__name__, fitbit_user, _type, sdat)
    if not cache.add(lock_id, 'true', LOCK_EXPIRE):
        logger.debug('Already retrieving %s data for date %s, user %s' % (
            _type, fitbit_user, sdat))
        raise Ignore()

    fbusers = UserFitbit.objects.filter(fitbit_user=fitbit_user)
    dates = {'base_date': 'today', 'period': 'max'}
    if date:
        dates = {'base_date': date, 'end_date': date}
    try:
        for fbuser in fbusers:
            logger.debug("Updating user: %s", str(fbuser))
            data = utils.get_fitbit_data(fbuser, _type, **dates)
            for datum in data:
                # Create new record or update existing record
                date = parser.parse(datum['dateTime'])
                tsd, created = TimeSeriesData.objects.get_or_create(
                    user=fbuser.user, resource_type=_type, date=date)
                tsd.value = datum['value']
                tsd.save()
        # Release the lock
        cache.delete(lock_id)
    except HTTPTooManyRequests:
        # We have hit the rate limit for the user, retry when it's reset,
        # according to the reply from the failing API call
        e = sys.exc_info()[1]
        logger.debug('Rate limit reached, will try again in %s seconds' %
                     e.retry_after_secs)
        
        raise get_time_series_data.retry(e, countdown=e.retry_after_secs)
    except Exception:
        exc = sys.exc_info()[1]
        logger.error("Exception updating data: %s" % exc)
        raise Reject(exc, requeue=False)

    logging.debug("Successfully got time series data for user")
