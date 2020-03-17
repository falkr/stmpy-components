import paho.mqtt.client as mqtt
import logging
from threading import Thread
import json
from appJar import gui

# TODO: choose proper MQTT broker address
MQTT_BROKER = 'mqtt.item.ntnu.no'
MQTT_PORT = 1883

# TODO: choose proper topics for communication
MQTT_TOPIC_INPUT = 'ttm4115/team_x/command'
MQTT_TOPIC_OUTPUT = 'ttm4115/team_x/answer'


class TimerCommandSenderComponent:
    """
    The component to send voice commands.
    """

    def on_connect(self, client, userdata, flags, rc):
        # we just log that we are connected
        self._logger.debug('MQTT connected to {}'.format(client))

    def on_message(self, client, userdata, msg):
        pass

    def __init__(self):
        # get the logger object for the component
        self._logger = logging.getLogger(__name__)
        print('logging under name {}.'.format(__name__))
        self._logger.info('Starting Component')

        # create a new MQTT client
        self._logger.debug('Connecting to MQTT broker {} at port {}'.format(MQTT_BROKER, MQTT_PORT))
        self.mqtt_client = mqtt.Client()
        # callback methods
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        # Connect to the broker
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
        # start the internal loop to process MQTT messages
        self.mqtt_client.loop_start()

        self.create_gui()

    def create_gui(self):
        self.app = gui()

        def extract_timer_name(label):
            label = label.lower()
            if 'spaghetti' in label: return 'spaghetti'
            if 'green tea' in label: return 'green tea'
            if 'soft eggs' in label: return 'soft eggs'
            return None

        def extract_duration_seconds(label):
            label = label.lower()
            if 'spaghetti' in label: return 600
            if 'green tea' in label: return 120
            if 'soft eggs' in label: return 240
            return None

        def publish_command(command):
            payload = json.dumps(command)
            self._logger.info(command)
            self.mqtt_client.publish(MQTT_TOPIC_INPUT, payload=payload, qos=2)

        self.app.startLabelFrame('Starting timers:')
        def on_button_pressed_start(title):
            name = extract_timer_name(title)
            duration = extract_duration_seconds(title)
            command = {"command": "new_timer", "name": name, "duration": duration}
            publish_command(command)
        self.app.addButton('Start Spaghetti Timer', on_button_pressed_start)
        self.app.addButton('Start Green Tea Timer', on_button_pressed_start)
        self.app.addButton('Start Soft Eggs Timer', on_button_pressed_start)
        self.app.stopLabelFrame()

        self.app.startLabelFrame('Stopping timers:')
        def on_button_pressed_stop(title):
            name = extract_timer_name(title)
            command = {"command": "cancel_timer", "name": name}
            publish_command(command)
        self.app.addButton('Cancel Spaghetti Timer', on_button_pressed_stop)
        self.app.addButton('Cancel Green Tea Timer', on_button_pressed_stop)
        self.app.addButton('Cancel Soft Eggs Timer', on_button_pressed_stop)
        self.app.stopLabelFrame()

        self.app.startLabelFrame('Asking for status:')
        def on_button_pressed_status(title):
            name = extract_timer_name(title)
            if name is None:
                command = {"command": "status_all_timers"}
            else:
                command = {"command": "status_single_timer", "name": name}
            publish_command(command)
        self.app.addButton('Get All Timers Status', on_button_pressed_status)
        self.app.addButton('Get Spaghetti Timer Status', on_button_pressed_status)
        self.app.addButton('Get Green Tea Timer Status', on_button_pressed_status)
        self.app.addButton('Get Soft Eggs Timer Status', on_button_pressed_status)
        self.app.stopLabelFrame()

        self.app.go()


    def stop(self):
        """
        Stop the component.
        """
        # stop the MQTT client
        self.mqtt_client.loop_stop()


# logging.DEBUG: Most fine-grained logging, printing everything
# logging.INFO:  Only the most important informational log items
# logging.WARN:  Show only warnings and errors.
# logging.ERROR: Show only error messages.
debug_level = logging.DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(debug_level)
ch = logging.StreamHandler()
ch.setLevel(debug_level)
formatter = logging.Formatter('%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

t = TimerCommandSenderComponent()