class iptools():
  def getIP():
    import socket
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

  def pingIP(target):
    import os
    cmd="ping "+target
    os.system(cmd)