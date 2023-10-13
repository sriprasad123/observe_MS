from pysnmp.hlapi import *

def send_snmpv3_trap():
    # SNMPv3 parameters for sending traps
    user = 'your_username'  # Replace with your SNMPv3 username
    auth_protocol = usmNoAuthProtocol  # No authentication
    priv_protocol = usmNoPrivProtocol  # No privacy

    # SNMPv3 trap receiver (your laptop's IP and port)
    receiver_ip = '127.0.0.1'
    receiver_port = 162

    snmp_user = UsmUserData(user, auth_protocol, None, priv_protocol, None)
    snmp_target = UdpTransportTarget((receiver_ip, receiver_port))

    var_binds = (
        ('1.3.6.1.2.1.1.1.0', OctetString('TestSystem')),
        ('1.3.6.1.4.1.12345.0.1', Integer(42))
    )

    errorIndication, errorStatus, errorIndex, varBindTable = next(
        sendNotification(
            snmpEngine=SnmpEngine(),
            authData=snmp_user,
            transportTarget=snmp_target,
            contextData=None,
            notifyType='trap',
            varBinds=var_binds
        )
    )

    if errorIndication:
        print(f'Failed to send SNMP trap: {errorIndication}')
    else:
        print('SNMP trap sent successfully')

if __name__ == '__main__':
    send_snmpv3_trap()
