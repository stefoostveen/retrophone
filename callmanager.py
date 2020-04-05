import pjsua2 as pj
import logging
import account as acc
import callmanager_events as cme
import event
import signal
import time
import random
import threading
import os


class CallManager:

    def __init__(self):
        # self.call = None
        self.ep = None
        self.account = None
        self.callbacks = {
                cme.CM_CALL_INCOMING: [],
                cme.CM_CALL_ENDED: [],
                cme.CM_CALL_ACCEPTED: [],
                cme.CM_ACCOUNT_REG_START: [],
                cme.CM_ACCOUNT_REG_COMPLETE: []
        }
        confdir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        confdir = confdir + "/conf/"


        self.account_config = self.getConfig(confdir+"AccountConfig.json", pj.AccountConfig())
        if not self.account_config:
            # AccountConfig file not found, create dummy file
            self.account_config = pj.AccountConfig()

            self.account_config.idUri = "SIP:SOMEONE@SIP.EXAMPLE.COM"
            self.account_config.regConfig.registrarUri = "SIP:SIP.EXAMPLE.COM"
            self.account_config.sipConfig.authCreds.push_back(pj.AuthCredInfo("digest", "*", "USERNAME", 0, "PASSWORD"))

            self.account_config.natConfig.sipStunUse = pj.PJSUA_STUN_USE_DEFAULT
            self.account_config.natConfig.iceEnabled = True

            self.saveConfig(self.account_config, confdir+"AccountConfig.json")
        self.endpoint_config = self.getConfig(confdir+"EPConfig.json", pj.EpConfig())
        if not self.endpoint_config:
            # EPConfig file not found, create dummy file
            self.endpoint_config = pj.EpConfig()
            self.saveConfig(self.endpoint_config, confdir+"EPConfig.json")
        self.transport_config = self.getConfig(confdir+"TransportConfig.json", pj.TransportConfig())
        if not self.transport_config:
            # TransportConfig file not found, create dummy file
            self.transport_config = pj.TransportConfig()
            self.transport_config.port = 5060
            self.saveConfig(self.transport_config, confdir+"TransportConfig.json")

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
            self.account = acc.Account()
            # acc = pj.Account()
            self.account.create(self.account_config)
            self.account.callbacks = self.callbacks
            self.account.subscribe(self.on_incoming_call, cme.CM_CALL_INCOMING)
        except Exception as e:
            logging.exception(e)

    def accept_call(self):
        print("[CALL] Trying to accept call")
        if self.account.call:
            op = pj.CallOpParam()
            op.statusCode = pj.PJSIP_SC_OK
            self.account.call.answer(op)

    def on_incoming_call(self, cbe):
        pass

    def on_media_state_change(self, ci=None):
        pass

    def unregister(self):
        self.ep.libDestroy()

    def invoke_call(self, uri):
        logging.exception("Not implemented")

    def end_calls(self):
        self.ep.hangupAllCalls()
        #self.call = None

    def subscribe(self, callback, event_t):
        if self.account:
            self.account.callbacks[event_t].append(callback)
        self.callbacks[event_t].append(callback)

    def notify(self, event_t, **attrs):
        e = event.Event()
        e.source = self
        for k, v in attrs.items():
            setattr(e, k, v)
        for fn in self.callbacks[event_t]:
            fn(e)

    def run(self):
        # todo: define minimums. Around 10 or 20 ms seems fine in order to reduce audio lag.
        return self.ep.libHandleEvents(10)

