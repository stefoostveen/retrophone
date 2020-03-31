import pjsua2 as pj
import logging


class Call(pj.Call):
    def onCallState(self, prm):
        print("bla")

    def onCallMediaState(self, prm):
        print("bla")


class Account(pj.Account):
    def onRegState(self, prm):
        print("***OnRegState: " + prm.reason)

    def onIncomingCall(self, prm):
        call = Call(self, prm.callId)
        op = pj.CallOpParam()
        op.statusCode = pj.PJSIP_SC_DECLINE
        call.hangup(op)
        del call


class CallManager:

    def __init__(self):
        self.call = None
        self.ep = None

        self.account_config = self.getConfig("AccountConfig.json", pj.AccountConfig())
        if not self.account_config:
            # AccountConfig file not found, create dummy file
            self.account_config = pj.AccountConfig()
            self.account_config.idUri = "sip:test@pjsip.org"
            self.account_config.regConfig.registrarUri = "sip:pjsip.org"
            cred = pj.AuthCredInfo("digest", "*", "usrntest", 0, "pwtest")
            self.account_config.sipConfig.authCreds.append(cred)
            self.account_config.natConfig.sipStunUse = pj.PJSUA_STUN_USE_DEFAULT
            self.account_config.natConfig.iceEnabled = True
            self.saveConfig(self.account_config, "AccountConfig.json")
        self.endpoint_config = self.getConfig("EPConfig.json", pj.EpConfig())
        if not self.endpoint_config:
            # EPConfig file not found, create dummy file
            self.endpoint_config = pj.EpConfig()
            self.saveConfig(self.endpoint_config, "EPConfig.json")
        self.transport_config = self.getConfig("TransportConfig.json", pj.TransportConfig())
        if not self.transport_config:
            # TransportConfig file not found, create dummy file
            self.transport_config = pj.TransportConfig()
            self.transport_config.port = 5060
            self.saveConfig(self.transport_config, "TransportConfig.json")

    def getConfig(self, filename, pjobject):
        try:
            jdoc = pj.JsonDocument()
            jdoc.loadFile(filename)
            jdoc.readObject(pjobject)
        except Exception as e:
            logging.exception(e)
        return pjobject

    def saveConfig(self, pjobject, filename):
        jdoc = pj.JsonDocument()
        jdoc.writeObject(pjobject)
        jdoc.saveFile(filename)

    def register(self):
        try:
            self.ep = pj.Endpoint()
            self.ep.libCreate()
            self.ep.libInit(self.endpoint_config)
        except Exception as e:
            logging.exception(e)

        try:
            self.ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, self.transport_config)
            self.ep.libStart()
        except Exception as e:
            logging.exception(e)

        try:
            acc = Account()
            acc.create(self.account_config)
        except Exception as e:
            logging.exception(e)

    def unregister(self):
        self.ep.libDestroy()

    def invoke_call(self, uri):
        logging.exception("Not implemented")

    def end_calls(self):
        self.ep.hangupAllCalls()
        self.call = None