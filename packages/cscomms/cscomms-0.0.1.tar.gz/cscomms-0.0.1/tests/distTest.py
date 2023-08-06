from cscomms import cscomms as messaging
from time import sleep

@messaging.listen(1, 1.0)
def message_listener(message):
  print(message)

sleep(5)

messaging.send(1, {"test": "Test"})