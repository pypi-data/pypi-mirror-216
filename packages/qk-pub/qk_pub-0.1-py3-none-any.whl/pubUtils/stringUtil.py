class StringBuffer(list):
    def __init__(self, parent=None):
        super(StringBuffer, self).__init__()

    def __str__(self):
        return "".join(self)

    def append(self, item):
        super(StringBuffer, self).append(str(item))


# 截取起始位置之间的字符
def sub_str(start: str = None, end: str = None, source: str = None):
    if (start and start not in source) or (end and end not in source):
        return

    return source[0 if not start else source.index(start):-1 if not end else source.index(end)][
           0 if not start else len(start):]


if __name__ == '__main__':
    buffer = StringBuffer()
    buffer.append(1)
    buffer.append(2)
    buffer.append(3)
    print(buffer.__str__())
