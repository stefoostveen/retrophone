import pjsua2 as pj
import call as cl
import logging
import callmanager_events as cme
import event


class Account(pj.Account):
    def __init__(self):
        pj.Account.__init__(self)
        self.call = None
        self.callbacks = {
                cme.CM_CALL_INCOMING: [],
                cme.CM_CALL_ENDED: [],
                cme.CM_CALL_ACCEPTED: [],
                cme.CM_ACCOUNT_REG_START: [],
                cme.CM_ACCOUNT_REG_COMPLETE: []
        }

    def onRegState(self, prm):
        print("[ACCOUNT] onRegState")

    def onRegStarted(self, prm):
        print("[ACCOUNT] regstarted")

    def onIncomingCall(self, prm):
        print("[CALL] incoming")
        self.call = cl.Call(self, prm.callId)
        op = pj.CallOpParam()
        op.statusCode = pj.PJSIP_SC_RINGING
        self.call.answer(op)
        self.notify(cme.CM_CALL_INCOMING, prm=prm)

    def startCall(self, uri):
        self.call = cl.Call(self)
        op = pj.CallOpParam(True)
        try:
            self.call.makeCall(uri, op)
        except Exception as e:
            logging.exception(e)

    def subscribe(self, callback, event_t):
        self.callbacks[event_t].append(callback)

    def notify(self, event_t, **attrs):
        e = event.Event()
        e.source = self
        for k, v in attrs.items():
            setattr(e, k, v)
        for fn in self.callbacks[event_t]:
            fn(e)
