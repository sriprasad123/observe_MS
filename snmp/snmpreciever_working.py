from pysnmp.carrier.asynsock.dispatch import AsynsockDispatcher
from pysnmp.carrier.asynsock.dgram import udp
from pyasn1.codec.ber import decoder
from pysnmp.proto import api

# Define a function to handle incoming SNMP traps
def trap_handler(cbCtx, transportDispatcher, transportDomain, transportAddress, wholeMsg):
    while wholeMsg:
        msgVer = api.decodeMessageVersion(wholeMsg)
        if msgVer in api.protoModules:
            pMod = api.protoModules[msgVer]
        else:
            print("Unsupported SNMP version")
            return

        reqMsg, wholeMsg = decoder.decode(wholeMsg, asn1Spec=pMod.Message())

        print("Received an SNMP trap:")
        reqPDU = pMod.apiMessage.getPDU(reqMsg)

        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            if reqPDU['trapType'] == 'coldStart':
                print("Cold Start Trap")
            elif reqPDU['trapType'] == 'warmStart':
                print("Warm Start Trap")
            elif reqPDU['trapType'] == 'linkDown':
                print("Link Down Trap")
            elif reqPDU['trapType'] == 'linkUp':
                print("Link Up Trap")
            else:
                print("Unknown Trap")

    return wholeMsg

# Create an SNMP trap receiver
transportDispatcher = AsynsockDispatcher()

# Register UDP socket to receive traps on port 162
transportDispatcher.registerTransport(
    udp.domainName, udp.UdpSocketTransport().openServerMode(('0.0.0.0', 162))
)

# Register the SNMP trap handler function
transportDispatcher.registerRecvCbFun(trap_handler)

print("SNMP Trap Receiver started on UDP port 162")

# Start the SNMP trap receiver
transportDispatcher.jobStarted(1)

try:
    # Run the receiver infinitely
    transportDispatcher.runDispatcher()
except Exception as e:
    print("Error: %s" % str(e))
    transportDispatcher.closeDispatcher()
