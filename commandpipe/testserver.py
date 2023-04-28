import cmdpipe


def handler(data):
    print(str(data))


pipe = cmdpipe.Reciever("localhost", 8080)
pipe.listen(handler)
