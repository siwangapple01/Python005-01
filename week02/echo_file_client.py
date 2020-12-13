#!/usr/bin/env python
import socket
import typing
import sys
from pathlib import Path

HOST = "localhost"
PORT = 10000


def echo_file_client(inputFilePath: str):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    receivedBinary = b""

    try:
        with open(inputFilePath, "rb") as f:
            data = f.read(1024)
            while data:
                print(data)
                s.sendall(data)
                receivedBinary += s.recv(1024)
                data = f.read(1024)

    except Exception:
        print("Given file cannot be open or file is not exist")
        sys.exit(1)

    try:
        p = Path(inputFilePath)
        suffix = p.suffix
        inputName = p.stem
        parentPath = str(p.parent)

        if suffix:
            outputFilePath = "".join(
                (parentPath + "/" + inputName + "_echo", suffix))
        else:
            outputFilePath = parentPath + "/" + inputName + "_echo"

        with open(outputFilePath, "wb") as f:
            f.write(receivedBinary)
    except Exception:
        print("Cannot save to the echo file, please check permission of current path")
        sys.exit(1)

    s.close()


if __name__ == "__main__":
    echo_file_client("./output.png")
