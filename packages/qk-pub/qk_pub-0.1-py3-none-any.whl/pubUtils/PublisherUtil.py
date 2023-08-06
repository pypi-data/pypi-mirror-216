from eventpy.eventdispatcher import EventDispatcher

pub = EventDispatcher()


def pub_event(topic=None, event=None, call_back_func=None):
    pub.appendListener(topic, call_back_func)
    pub.dispatch(topic, event)
