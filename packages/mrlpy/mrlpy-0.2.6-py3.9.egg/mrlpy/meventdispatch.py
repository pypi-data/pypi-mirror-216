import logging


class MEventDispatch(object):
    """
    Generic event dispatcher which listen and dispatch events
    """

    def __init__(self):
        self._ev_listeners = dict()

    # def __del__(self):
    #    """
    #    Remove all listener references at destruction time
    #    """
    #    self._ev_listeners = None

    def has_listener(self, event_name, listener):
        """
        Return true if listener is register to event_name
        """
        # Check for event name and for the listener
        if event_name in self._ev_listeners.keys():
            return listener in self._ev_listeners[event_name]
        else:
            return False

    def dispatch_event(self, event):
        """
        Dispatch an instance of MEvent class
        """

        logging.info(f"Dispatching event: {event}")

        topic = ""

        if event.name == "":
            topic = event.method
        else:
            topic = event.name

        # Dispatch the event to all the associated listeners
        if topic in self._ev_listeners.keys():
            listeners = self._ev_listeners[event.name]

            for listener in listeners:
                listener(event)

    def add_event_listener(self, event_name, listener):
        """
        Add an event listener for an event name
        """
        # Add listener to the event name
        if not self.has_listener(event_name, listener):
            listeners = self._ev_listeners.get(event_name, [])

            listeners.append(listener)

            self._ev_listeners[event_name] = listeners

    def remove_event_listener(self, event_name, listener):
        """
        Remove event listener.
        """
        # Remove the listener from the event name
        if self.has_listener(event_name, listener):
            listeners = self._ev_listeners[event_name]

            if len(listeners) == 1:
                # Only this listener remains so remove the key
                del self._ev_listeners[event_name]

            else:
                # Update listeners chain
                listeners.remove(listener)

                self._ev_listeners[event_name] = listeners
