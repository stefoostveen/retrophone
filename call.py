import pjsua2 as pj
import callmanager_events as cme
import event

# PJSIP_INV_STATE_NULL 		    Before INVITE is sent or received
# PJSIP_INV_STATE_CALLING 	    After INVITE is sent
# PJSIP_INV_STATE_INCOMING 	    After INVITE is received.
# PJSIP_INV_STATE_EARLY 		After response with To tag.
# PJSIP_INV_STATE_CONNECTING 	After 2xx is sent/received.
# PJSIP_INV_STATE_CONFIRMED 	After ACK is sent/received.
# PJSIP_INV_STATE_DISCONNECTED 	Session is terminated.

class Call(pj.Call):
    def __init__(self, acc, call_id=pj.PJSUA_INVALID_ID, callbacks=None):
        pj.Call.__init__(self, acc, call_id=call_id)
        self.callbacks = callbacks

    def onCallState(self, prm):
        print("[CALL] call state changed")
        call_info = self.getInfo()
        if call_info.state == pj.PJSIP_INV_STATE_DISCONNECTED:
            print("[CALL] call ended")
            self.notify(cme.CM_CALL_ENDED)
            del_call_scheduled = True
        elif call_info.state == pj.PJSIP_INV_STATE_CONFIRMED:
            print("[CALL] call connected")
            self.notify(cme.CM_CALL_ACCEPTED)
        elif call_info.state == pj.PJSIP_INV_STATE_CALLING:
            print("[CALL] call ringing at other end")
            self.notify(cme.CM_CALL_RINGING_AOE)
        # elif call_info.state == pj.PJSIP_INV_STATE_INCOMING:
        #     print("[CALL] call incoming")
        #     self.notify(cme.CM_CALL_INCOMING)

    def onCallMediaState(self, prm):
        ci = self.getInfo()
        for mi in ci.media:
            if mi.type == pj.PJMEDIA_TYPE_AUDIO and (mi.status == pj.PJSUA_CALL_MEDIA_ACTIVE or mi.status == pj.PJSUA_CALL_MEDIA_REMOTE_HOLD):
                m = self.getMedia(mi.index)
                am = pj.AudioMedia.typecastFromMedia(m)
                # connect ports
                #todo: AttributeError: 'builtin_function_or_method' object has no attribute 'audDevManager' on the pi
                pj.Endpoint.instance.audDevManager().getCaptureDevMedia().startTransmit(am)
                am.startTransmit(pj.Endpoint.instance.audDevManager().getPlaybackDevMedia())

                # if mi.status == pj.PJSUA_CALL_MEDIA_REMOTE_HOLD and not self.onhold:
                #     self.chat.addMessage(None, "'%s' sets call onhold" % (self.peerUri))
                #     self.onhold = True
                # elif mi.status == pj.PJSUA_CALL_MEDIA_ACTIVE and self.onhold:
                #     self.chat.addMessage(None, "'%s' sets call active" % (self.peerUri))
                #     self.onhold = False

    def accept(self):
        prm = pj.CallOpParam()
        prm.statusCode = pj.PJSIP_SC_OK
        self.answer(prm)

    def subscribe(self, callback, event_t):
        self.callbacks[event_t].append(callback)

    def notify(self, event_t, **attrs):
        e = event.Event()
        e.source = self
        for k, v in attrs.items():
            setattr(e, k, v)
        for fn in self.callbacks[event_t]:
            fn(e)
