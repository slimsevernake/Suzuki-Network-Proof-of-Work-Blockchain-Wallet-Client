import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNReconnectionPolicy
 

pnconfig = PNConfiguration()
pnconfig.reconnect_policy = PNReconnectionPolicy.LINEAR

pnconfig.subscribe_key = ""
pnconfig.publish_key = ""
pubnub = PubNub(pnconfig)

TEST_CHANNEL = "TEST_CHANNEL"

pubnub.subscribe().channels([TEST_CHANNEL]).execute()

class Listener(SubscribeCallback):
    def message(self, pubnub, message_obj):
        print(f"\n--Incoming message object: {message_obj}")

pubnub.add_listener(Listener())

def main():
    time.sleep(1)
    pubnub.publish().channel([TEST_CHANNEL]).message({"test":"bar"}).sync()

if __name__ == "__main__":
    main()


