import pjsua2 as pj
import callmanager_events as cme


class Call(pj.Call):
    def onCallState(self, prm):
        call_info = self.getInfo()
        if call_info.state == pj.PJSIP_INV_STATE_DISCONNECTED:
            del_call_scheduled = True

    def onCallMediaState(self, prm):
        print("bla")