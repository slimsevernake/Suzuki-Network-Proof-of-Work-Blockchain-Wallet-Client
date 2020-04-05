import time
import backend.env_config as config
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNReconnectionPolicy
 
pnconfig = PNConfiguration()
pnconfig.reconnect_policy = PNReconnectionPolicy.LINEAR
pnconfig.subscribe_key = config.pubsub["subscribe_key"]
pnconfig.publish_key = config.pubsub["publish_key"]
TEST_CHANNEL = "TEST_CHANNEL"

class Listener(SubscribeCallback):
    def message(self, pubnub, message_obj):
        print(f"\n-- Channel: {message_obj.channel} | Message: {message_obj.message}")

class PubSub():
    """
    Manages the publish/subscribe layer of the application, affording
    scalable communications infrastructure across nodes.
    """
    def __init__(self):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels([TEST_CHANNEL]).execute()
        self.pubnub.add_listener(Listener())

    def publish(self, channel_str, message_obj):
        """
        Publish given message obj to given channel.
        """
        self.pubnub.publish().channel(channel_str).message(message_obj).sync()

def main():
    pubsub = PubSub()

    time.sleep(1)

    pubsub.publish(TEST_CHANNEL, { "foo": "bar" })

if __name__ == "__main__":
    main()


