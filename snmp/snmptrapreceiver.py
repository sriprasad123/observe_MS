from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.entity import engine, config
from pysnmp.hlapi.asyncio import *

async def snmp_trap_handler(snmp_engine, context, var_binds, cb_ctx):
    # Convert SNMP trap data to a dictionary
    trap_data = {}
    for oid, val in var_binds:
        trap_data[str(oid)] = val.prettyPrint()

    # Convert the trap data to JSON
    import json
    json_data = json.dumps(trap_data, indent=4)

    print("Received SNMP trap:")
    print(json_data)

def main():
    # Create an SNMP engine
    snmp_engine = engine.SnmpEngine()

    # Setup SNMPv3 parameters (update these with your SNMPv3 credentials)
    user = 'your_username'
    auth_key = 'your_auth_key'
    priv_key = 'your_priv_key'
    auth_protocol = usmHMACSHAAuthProtocol
    priv_protocol = usmDESPrivProtocol
    security_name = config.OctetString(user)

    config.addV3User(
        snmp_engine,
        user,
        auth_protocol,
        auth_key,
        priv_protocol,
        priv_key
    )

    # Create an SNMP context with SNMPv3 security settings
    snmp_context = context.SnmpContext(snmp_engine)

    # Register the SNMP trap handler
    snmp_engine.registerNotificationReceiver(snmp_context, snmp_trap_handler)

    # Listen for incoming SNMP traps
    transport_dispatcher = udp.UdpTransportDispatcher()
    transport_dispatcher.registerRecvCbFun(snmp_engine.receiveMessage)
    transport_dispatcher.jobStarted(1)

    try:
        transport_dispatcher.runDispatcher()
    except KeyboardInterrupt:
        transport_dispatcher.closeDispatcher()

if __name__ == '__main__':
    main()
