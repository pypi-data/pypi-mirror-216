import os
import time
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

#allows local testingdf of functions
if __name__ == '__main__':
    import utilspkg.utils_init
else:
    from utilspkg import utils_init

utils_init.load_env_variables_from_yaml('/Users/croft/VScode/ptagit/env_vars.yaml')

logger = utils_init.setup_logger(__name__)

SLACK_API_KEY = os.environ["SLACK_ACCESS_TOKEN_TEAM"]
TESTING_DM = os.environ["TESTING_DM"]
TESTING_CHANNEL = os.environ["TESTING_CHANNEL"] # not currently used since all goes to the DM's "channel"
tester = 'hi'

class SlackConnect:
    """
    A utility class for sending messages and fetching conversation history from Slack.
    """

    def __init__(self, api_key=SLACK_API_KEY, testing_flag=False, logger=None):
        """
        Initialize the SlackSender with an API key, testing flag, and optional logger.
        """
        self.api_key = api_key
        self.slack_client = WebClient(token=self.api_key)
        self.logger = logger if logger else logging.getLogger(__name__)
        self.testing_flag = testing_flag
        self.testing_dm_or_channel = TESTING_DM

    def send_dm_or_channel_message(self, channel_or_slack_id, message, thread_ts=None, testing_flag=None):
        """
        Send a message to the given channel or user (by Slack ID) through Direct Message.
        Optionally, reply to a threaded message by providing a thread timestamp.
        """
        if testing_flag is None:
            testing_flag = self.testing_flag

        channel_or_slack_id = channel_or_slack_id if not testing_flag else self.testing_dm_or_channel

        if channel_or_slack_id.startswith("U"):  # check if it's a user ID
            dm = self.slack_client.conversations_open(users=channel_or_slack_id)
            channel_or_slack_id = dm['channel']['id']

        response = self.slack_client.chat_postMessage(
            channel=channel_or_slack_id,
            text=message,
            thread_ts=thread_ts,  # ok if None
            unfurl_links=False,
            unfurl_media=False)
        
        return response

    def get_list_of_channels(self, bool_public_channels=True, bool_private_channels=True, exclude_archived=True):
        '''https://api.slack.com/methods/conversations.list
            Returns the conversations_list() result of 'all channels
            The object can then be iterated over (for channel in all_channels). Some properties:
            channel_id = channel["id"]
            channel_name = channel["name"]
            status = "private" if channel["is_private"] else "public"
            description = channel["purpose"]["value"]
            topic = channel["topic"]["value"]
            is_archived = channel["is_archived"]
        '''
        # initialize variables
        public_channels = None
        private_channels = None
        # Get the public channels
        if bool_public_channels:
            public_channels = self.slack_client.conversations_list(types="public_channel", exclude_archived=exclude_archived)
            public_channels = public_channels["channels"]

        # Get the private channels
        if bool_private_channels:
            private_channels = self.slack_client.conversations_list(types="private_channel", exclude_archived=exclude_archived)
            private_channels = private_channels["channels"]

        return public_channels + private_channels

    def get_channel_members(self, channel_id):
        '''Takes a channel_id string (e.g. "C0921V92") and returns the results of slack_client.conversation_members()'''
        return self.slack_client.conversations_members(channel=channel_id)

    def make_slack_api_call(self, method, **kwargs):
        ''' Handles pagination and rate limit checking '''
        while True:
            try:
                response = self.slack_client.api_call(method, **kwargs)
                
                if response['ok']:
                    return response
                elif response['error'] == 'ratelimited':
                    rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', 1))

                    logger.info(f"Rate limited: {response['error']}")
                    logger.info(f"Waiting for {rate_limit_reset} seconds before retrying")
                    time.sleep(rate_limit_reset)
                else:
                    logger.error(f"Slack API error: {response['error']}")
                    return response
            except SlackApiError as e:
                logger.error(f"Slack API error: {e}")
                return None
            
    def get_users (self):
        '''return the result of slack_client.users_list()'''
        return self.make_slack_api_call("users.list")
        

    def get_channel_messages(self, channel_id, oldest_timestamp=None, newest_timestamp=None):
        """
        Fetch messages from the specified Slack channel.
        Optionally, filter the messages by providing the oldest and/or newest timestamp.
        Handles pagination and rate limits.
        """

        messages = []
        next_cursor = None

        while True:
            try:
                # Build kwargs dict based on parameters
                kwargs = {
                    "channel": channel_id,
                    "inclusive": False,
                    "limit": 100,  # Get maximum number of messages per API call
                    "cursor": next_cursor,
                }

                # Only add timestamp parameters if they are not None
                if oldest_timestamp:
                    kwargs["oldest"] = oldest_timestamp
                if newest_timestamp:
                    kwargs["latest"] = newest_timestamp

                # Request the conversation history
                response = self.slack_client.conversations_history(**kwargs)
                messages += response.data.get('messages')

                # Check if more messages are available
                next_cursor = response.data.get('response_metadata', {}).get('next_cursor')
                if not next_cursor:
                    break

                # Pause before next API call to avoid hitting rate limits
                time.sleep(1)

            except SlackApiError as e:
                # If rate limited, sleep for recommended duration and try again
                if e.response["error"] == "ratelimited":
                    delay = int(e.response.headers.get('Retry-After'))
                    time.sleep(delay)
                else:
                    self.logger.error(f"Error fetching conversation history: {e}")
                    break

        return messages
    

if __name__ == '__main__':
    slack = SlackConnect()
    channels = slack.get_list_of_channels()
    print (len(channels))