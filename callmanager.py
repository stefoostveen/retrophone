import pjsua2 as pj
import logging
import signal
import time
import random
import threading


class Call(pj.Call):
    def onCallState(self, prm):
        print("bla")

    def onCallMediaState(self, prm):
        print("bla")


class Account(pj.Account):
    def onRegState(self, prm):
        print("[ACCOUNT] onRegState")

    def onRegStarted(self, prm):
        print("[ACCOUNT] regstarted")

    def onIncomingCall(self, prm):
        print("[CALL] incoming")


class CallManager:

    def __init__(self):
        self.call = None
        self.ep = None
        self.account = None

        self.account_config = self.getConfig("AccountConfig.json", pj.AccountConfig())
        if not self.account_config:
            # AccountConfig file not found, create dummy file
            self.account_config = pj.AccountConfig()

            self.account_config.idUri = "SIP:SOMEONE@SIP.EXAMPLE.COM"
            self.account_config.regConfig.registrarUri = "SIP:SIP.EXAMPLE.COM"
            self.account_config.sipConfig.authCreds.push_back(pj.AuthCredInfo("digest", "*", "USERNAME", 0, "PASSWORD"))

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
            return pjobject
        except Exception as e:
            logging.exception(e)
            return None

    def saveConfig(self, pjobject, filename):
        jdoc = pj.JsonDocument()
        jdoc.writeObject(pjobject)
        jdoc.saveFile(filename)

    def register(self):
        try:
            self.ep = pj.Endpoint()
            self.ep.libCreate()
            # set threadcnt to zero, due to python not liking multiple processes or such
            self.endpoint_config.uaConfig.threadCnt = 0
            self.endpoint_config.uaConfig.setMainThreadOnly = True
            self.ep.libInit(self.endpoint_config)
        except Exception as e:
            logging.exception(e)

        try:
            self.ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, self.transport_config)
            self.ep.libStart()
        except Exception as e:
            logging.exception(e)

        try:
            self.account = Account()
            #acc = pj.Account()
            self.account.create(self.account_config)
        except Exception as e:
            logging.exception(e)

        #self.run()

    def run(self):
        return self.ep.libHandleEvents(100)

    def unregister(self):
        self.ep.libDestroy()

    def invoke_call(self, uri):
        logging.exception("Not implemented")

    def end_calls(self):
        self.ep.hangupAllCalls()
        self.call = None