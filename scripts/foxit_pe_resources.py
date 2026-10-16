"""Independent read-only parser for standard and extended Win32 dialog resources."""
import struct


def dialog(data):
    """Decode standard/extended Win32 dialog control IDs, labels and layout."""
    offset = 0
    def unpack(fmt):
        nonlocal offset
        value = struct.unpack_from('<' + fmt, data, offset)
        offset += struct.calcsize('<' + fmt)
        return value
    def text():
        nonlocal offset
        value = unpack('H')[0]
        if value == 0: return ''
        if value == 0xffff: return {'ordinal': unpack('H')[0]}
        units = [value]
        while True:
            value = unpack('H')[0]
            if not value: break
            units.append(value)
        return struct.pack('<' + 'H' * len(units), *units).decode('utf-16-le', errors='replace')
    extended = data[:4] == b'\x01\x00\xff\xff'
    if extended:
        _, _, _, _, style, count, x, y, w, h = unpack('HHIIIHhhhh')
    else:
        style, _, count, x, y, w, h = unpack('IIHhhhh')
    menu, window_class, title = text(), text(), text()
    if style & 0x40:
        unpack('H')
        if extended: unpack('HBB')
        text()
    controls = []
    for _ in range(count):
        offset = (offset + 3) & ~3
        if extended:
            _, _, _, cx, cy, cw, ch, cid = unpack('IIIhhhhI')
        else:
            _, _, cx, cy, cw, ch, cid = unpack('IIhhhhH')
        klass, label = text(), text()
        extra = unpack('H')[0]
        if extra: offset += extra
        controls.append({'id': cid, 'class': klass, 'text': label, 'dialog_units': [cx, cy, cw, ch]})
    return {'title': title, 'dialog_units': [x, y, w, h], 'controls': controls}
