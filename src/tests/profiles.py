from core.modem import ModemConfig


@staticmethod
def combat_tx() -> ModemConfig:
    """TX боевой режим из документации"""
    return ModemConfig(
        freq=3500,
        code=11,
        fhss=0,
        dsss=0,
        rate=50,
        attenuation=0,
        address=29131,
        pan=56064,
        ack=0,
        ttl=0,
        trim=111,
        timeslot=0,
        baudrate=400000,
        parity="none",
        stopbits=1,
        inverted=False,
        mode="100kbps"
    )
@staticmethod
def default_tx() -> ModemConfig:
    """TX боевой режим из документации"""
    return ModemConfig(
        freq=3500,
        code=11,
        fhss=0,
        dsss=0,
        rate=50,
        attenuation=0,
        address=29131,
        pan=56064,
        ack=0,
        ttl=0,
        trim=111,
        timeslot=0,
        baudrate=400000,
        parity="none",
        stopbits=1,
        inverted=False,
        mode=""
    )

@staticmethod
def combat_rx() -> ModemConfig:
    """RX боевой режим из документации"""
    return ModemConfig(
        freq=3500,
        code=11,
        fhss=0,
        dsss=0,
        rate=50,
        attenuation=0,
        address=65535,
        pan=56064,
        bind=29131,
        trim=111,
        timeslot=0,
        ewtests=0,
        baudrate=420000,
        parity="none",
        stopbits=1,
        inverted=False,
        mode="100kbps"
    )