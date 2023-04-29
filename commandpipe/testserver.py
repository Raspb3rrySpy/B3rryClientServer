import cmdpipe


def handler(data):
    print(str(data))


pipe = cmdpipe.Reciever("localhost", 32000)
pipe.listen(handler)
