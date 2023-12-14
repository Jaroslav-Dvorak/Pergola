from pymodbus.constants import Endian
from struct import pack, unpack

WC = {"b": 1, "h": 2, "e": 2, "i": 4, "l": 4, "q": 8, "f": 4, "d": 8}


@pyscript_compile
def _unpack_words(fstring, handle, byteorder, wordorder):
    wc_value = WC.get(fstring.lower()) // 2
    handle = unpack(f"!{wc_value}H", handle)
    if wordorder == Endian.LITTLE:
        handle = list(reversed(handle))
    handle = [pack(byteorder + "H", p) for p in handle]
    handle = b"".join(handle)
    return handle


@pyscript_compile
def decode_16bit_uint(payload, byteorder):
    payload = b"".join(pack("!H", x) for x in payload)
    pointer = 0x00
    pointer += 2
    fstring = byteorder + "H"
    handle = payload[pointer - 2: pointer]
    return unpack(fstring, handle)[0]


@pyscript_compile
def decode_32bit_uint(payload, byteorder, wordorder):
    payload = b"".join(pack("!H", x) for x in payload)
    pointer = 0x00
    pointer += 4
    fstring = "I"
    handle = payload[pointer - 4: pointer]
    handle = _unpack_words(fstring, handle, byteorder, wordorder)
    return unpack("!" + fstring, handle)[0]


class AddressRange:
    def __init__(self, start, end, name):
        if name:
            self.name = name
        self.start = start
        self.end = end
        self.range = range(start, end + 1)
        self.count = (end - start) + 1


class Register:
    def __init__(self, name, unit, device_class, datatype, gain):
        self.name = name
        self.unit = unit
        self.device_class = device_class
        self.datatype = datatype
        self.gain = gain
        self.register_values = []

    @pyscript_compile
    def decode(self, byteorder, wordorder):
        match self.datatype:
            case "uint16":
                return decode_16bit_uint(self.register_values, byteorder) * self.gain
            case "uint32":
                return decode_32bit_uint(self.register_values, byteorder, wordorder) * self.gain


class ModbusParser:
    def __init__(self, byteorder, wordorder):
        self.address_ranges = []
        self.registers = {}
        self.byteorder = byteorder
        self.wordorder = wordorder

    def add_address_range(self, start, end, name=None):
        address_range = AddressRange(start, end, name)
        self.address_ranges.append(address_range)

    def add_register(self, address, name, unit, device_class, datatype, gain):
        if isinstance(address, tuple):
            register = Register(name, unit, device_class, datatype, gain)
            for addr in address:
                self.registers[addr] = register
        else:
            self.registers[address] = Register(name, unit, device_class, datatype, gain)

    @pyscript_compile
    def get_all_values(self):
        ret = {}
        prev = None
        for reg in self.registers.values():
            if prev is reg:
                continue
            ret[reg.name] = reg.decode(self.byteorder, self.wordorder)
            prev = reg
        return ret
