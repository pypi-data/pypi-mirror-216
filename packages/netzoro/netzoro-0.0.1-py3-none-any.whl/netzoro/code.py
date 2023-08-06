def ping():
    code = '''
import subprocess
from twisted.internet import reactor

class PingProtocol:
    def ping(self, host):
        process = subprocess.Popen(['ping', host], stdout=subprocess.PIPE)
        output, _ = process.communicate()
        print(output.decode())
        
protocol = PingProtocol()
protocol.ping('google.com')
reactor.run()
'''
    filename = 'ping.py'
    with open(filename, "w") as f:
        f.write(code)
def traceroute():
    code='''
import subprocess
from twisted.internet import reactor

class PingProtocol:
    def ping(self, host):
        process = subprocess.Popen(['traceroute', host], stdout=subprocess.PIPE)
        output, _ = process.communicate()
        print(output.decode())
        
protocol = PingProtocol()
protocol.ping('google.com')
reactor.run()
    '''
    filename = 'traceroute.py'
    with open(filename, "w") as f:
        f.write(code)

def bus():
    code = '''
from twisted.internet import reactor, protocol
from twisted.protocols import basic

class DropLink(basic.LineOnlyReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None

    def connectionMade(self):
        self.factory.clients.append(self)
        print("New client connected to bus backbone.")

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print("Client disconnected.")

    def lineReceived(self, line):
        message = line.decode().strip()
        if not self.name:
            self.name = message
            print(f"{self.name} connected to bus.")
        else:
            if message.startswith("@"):
                recipient, private_message = message[1:].split(":", 1)
                self.sendPrivateMessage(recipient, private_message)
            else:
                print(f"{self.name}: {message}")
                self.broadcastMessage(f"{self.name}: {message}")

    def sendPrivateMessage(self, recipient, message):
        for client in self.factory.clients:
            if client.name == recipient:
                client.sendLine(f"(Private) {self.name}: {message}".encode())
                break
        else:
            self.sendLine(f"Error: User {recipient} not found.".encode())

    def broadcastMessage(self, message):
        for client in self.factory.clients:
            if client != self:
                client.sendLine(message.encode())


class BusBackbone(protocol.Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        return DropLink(self)

if __name__ == "__main__":
    reactor.listenTCP(8000, BusBackbone())
    print("Bus server started.")
    print("Enter your name as the first message to register. To send a message to a particular username, use '@username: message'.")
    reactor.run()
'''
    filename = 'bus.py'
    with open(filename, "w") as f:
        f.write(code)

def star():
    code='''
from twisted.internet import protocol, reactor

class StarProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory  
        self.name = None  

    def connectionMade(self):
        print('New client connected: ', self.transport.getPeer())
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print("Client disconnected")
        self.factory.remove(self)

    def dataReceived(self, data):
        message = data.decode().strip()
        if not self.name:
            self.name = message
            print(self.name, ' has connected to the server.') 
        else:
            if message.startswith('@'):
                recipient, private_message = message[1:].split(":", 1)
                self.sendthroughServer(recipient, private_message)
            else:
                self.transport.write(message)

    def sendthroughServer(self, recipient, message):
        self.transport.write(message) 
        self.transport.write('message sending.....')
        self.sendPrivateMessage(recipient, message)  

    def sendPrivateMessage(self, recipient, message):
        for client in self.factory.clients:
            if client.name == recipient:
                client.transport.write(f"(Private) {self.name}: {message}\n".encode())
                break
        else:
            self.transport.write(f"Error: User {recipient} not found.\n".encode())

class StarFactory(protocol.Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        return StarProtocol(self)

if __name__ == "__main__":
    reactor.listenTCP(8080, StarFactory())
    print("Server started. Listening on port 8080...")
    print("Enter client name to register. Enter @ before the starting of a message to send message to another client.")
    reactor.run()
    '''
    filename = 'star.py'
    with open(filename, "w") as f:
        f.write(code)

def ring():
    code = '''
from twisted.internet import protocol, reactor

class RingProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.name = None

    def connectionMade(self):
        print('New client connected: ', self.transport.getPeer())
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        print("Client disconnected")
        index = self.factory.clients.index(self)
        self.factory.clients[index] = None

    def dataReceived(self, data):
        message = data.decode().strip()
        if not self.name:
            self.name = message
            print(self.name, ' has connected to the server.')
            self.factory.names.append(self.name)  # if the client has not connected to the server before
        else:
            if message.startswith('@'):
                recipient, private_message = message[1:].split(":", 1)
                receiver_index = self.factory.names.index(recipient)
                sender_index = self.factory.names.index(self.name)
                while sender_index != receiver_index:
                    sender_index += 1
                    if sender_index == len(self.factory.names):
                        sender_index = 0
                    if self.factory.clients[sender_index] is None:
                        self.transport.write('link failure. message cannot be sent'.encode())
                        break
                    self.sendPrivateMessage(self.factory.names[sender_index], private_message)
            else:
                self.transport.write(message.encode())

    def sendPrivateMessage(self, recipient, message):
        for client in self.factory.clients:
            if client is not None:
                if client.name == recipient:
                    client.transport.write(f"(Private) {self.name}: {message}\n".encode())
                    break
        else:
            self.transport.write(f"Error: User {recipient} not found.\n".encode())

class RingFactory(protocol.Factory):
    def __init__(self):
        self.clients = []
        self.names = []

    def buildProtocol(self, addr):
        return RingProtocol(self)

if __name__ == "__main__":
    reactor.listenTCP(8080, RingFactory())
    print("Server started. Listening on port 8080...")
    print("Enter client name to register. Enter @ before the starting of a message to send message to another client.")
    reactor.run()

    '''
    filename = 'ring.py'
    with open(filename, "w") as f:
        f.write(code)

def mesh():
    code='''
from twisted.internet import reactor, protocol

class MeshProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory
        self.name = None

    def connectionMade(self):
        self.factory.clients.append(self)
        print("New client connected.")

    def connectionLost(self, reason):
        self.factory.clients.remove(self)
        print("Client disconnected.")

    def dataReceived(self, data):
        message = data.decode().strip()
        if not self.name:
            self.name = message
            print(f"{self.name} joined the chat.")
        else:
            if message.startswith("@"):
                recipient, private_message = message[1:].split(":", 1)
                self.sendPrivateMessage(recipient, private_message)
            else:
                print(f"{self.name}: {message}")
                self.broadcastMessage(f"{self.name}: {message}")

    def sendPrivateMessage(self, recipient, message):
        for client in self.factory.clients:
            if client.name == recipient:
                client.transport.write(f"(Private) {self.name}: {message}\n".encode())
                break
        else:
            self.transport.write(f"Error: User {recipient} not found.\n".encode())

    def broadcastMessage(self, message):
        for client in self.factory.clients:
            if client != self:
                client.transport.write(f"{message}\n".encode())

class MeshFactory(protocol.Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self, addr):
        return MeshProtocol(self)

if __name__ == "__main__":
    reactor.listenTCP(8000, MeshFactory())
    print("Bus server started.")
    print("Enter your name as first message to register. To send a message to a particular username use '@username: message'.")
    reactor.run()

    '''
    filename = 'mesh.py'
    with open(filename, "w") as f:
        f.write(code)
def tcpchat():
    code = '''
from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineOnlyReceiver 

class ChatProtocol(LineOnlyReceiver): 
    def __init__(self, factory): 
        self.factory = factory 
        self.name = None 
        self.state = "GETNAME" 
        self.client = None 

    def lineReceived(self, line):
        if self.state == "GETNAME": 
            self.handle_GETNAME(line.decode()) 
        else: 
            self.handle_CHAT(line.decode()) 

    def handle_GETNAME(self, name): 
        if name in self.factory.users: 
            self.sendLine("Name already taken, please choose another name.".encode()) 
            return 
        self.sendLine(f"Welcome, {name}!".encode()) 
        self.broadcastMessage(f"{name} has joined the chat room.") 
        self.name = name
        self.factory.users[name] = self
        self.state = "CHAT" 

    def handle_CHAT(self, message): 
        if message.lower() == "/quit": 
            self.transport.loseConnection() 
        else: 
            message = f"<{self.name}> {message}" 
            self.broadcastMessage(message) 

    def broadcastMessage(self, message):
        for name, protocol in self.factory.users.items(): 
            if protocol != self: 
                protocol.sendLine(message.encode()) 

    def connectionMade(self): 
        self.sendLine("Connected to the chat server. Type '/quit' to exit.".encode()) 
        self.factory.clients.append(self) 

    def connectionLost(self, reason): 
        self.factory.clients.remove(self)

class ChatFactory(protocol.Factory): 
    def __init__(self): 
        self.users = {} 
        self.clients = [] 

    def buildProtocol(self, addr): 
        return ChatProtocol(self) 
           
if __name__ == "__main__": 
    reactor.listenTCP(9000, ChatFactory()) 
    print("Chat server started. Listening on port 9000...") 
    reactor.run() 
    '''
    filename = 'tcpchat.py'
    with open(filename, "w") as f:
        f.write(code)

def tcpechoclient():
    code1 =  '''
#cllient
from twisted.internet import reactor, protocol 
class EchoClient(protocol.Protocol): 
    def connectionMade(self):
        msg = input("Enter the message to Server - ") 
        self.transport.write(msg.encode()) 

    def dataReceived(self, data):
        print ("Acknoledgement from Server -", data.decode()) 
        self.transport.loseConnection()
        
class EchoFactory(protocol.ClientFactory): 
    def buildProtocol(self, addr): 
        return EchoClient()
        
reactor.connectTCP("localhost", 8000, EchoFactory())
reactor.run() 
    '''
    filename = 'tcpclient.py'
    with open(filename, "w") as f:
        f.write(code1)

    code2='''
from twisted.internet import protocol,reactor 
class echo(protocol.Protocol): 
    def dataReceived(self, data):
        print("Message from Client -", data.decode()) 
        print("Client Connected!")
        ack_msg = f"{data.decode()}"
        ack = "ACK[" + ack_msg + "]" 
        print("Acknoledgement Sent!") 
        self.transport.write(ack.encode()) 

class echofactory(protocol.Factory): 
    def buildProtocol(self, addr): 
        return echo() 
    
reactor.listenTCP(8000,echofactory())
reactor.run() 
    '''
    filename = 'tcpserver.py'
    with open(filename, "w") as f:
        f.write(code2)

def tcpftp():
    code1='''
from twisted.internet import reactor, protocol 
import os

class FileTransferProtocol(protocol.Protocol): 
    def connectionMade(self): 
        print("Client connected.") 

    def dataReceived(self, data): 
        if data == b"SEND": 
            self.transport.write(b"READY") 
            self.transferFile = True 
        elif self.transferFile: 
            with open("received_file.txt", "wb") as f: 
                f.write(data) 
            self.transport.write(b"RECEIVED") 
            self.transferFile = False
        else: 
            self.transport.write(b"ERROR")

class FileTransferFactory(protocol.Factory): 
    protocol = FileTransferProtocol 

    
if __name__ == "__main__": 
    reactor.listenTCP(7000, FileTransferFactory()) 
    print("Server started.")
    reactor.run() 
    '''
    code2='''
from twisted.internet import reactor, protocol 
import os

class FileTransferClientProtocol(protocol.Protocol):
    def connectionMade(self): 
        try: 
            f = open("myfile.txt", "rb") 
            self.fileData = f.read() 
            f.close()
            if len(self.fileData) == 0: 
                print("File is empty.") 
                self.transport.loseConnection() 
            else: 
                self.transport.write(b"SEND") 
        except FileNotFoundError: 
            print("File not found.") 
            self.transport.loseConnection()

    def dataReceived(self, data): 
        if data == b"READY": 
            if self.fileData: 
                self.transport.write(self.fileData) 
            else: 
                self.transport.loseConnection() 
        elif data == b"RECEIVED":
            print("File transfer complete.") 
            self.transport.loseConnection() 
        else:
            print("Error:", data.decode()) 
            self.transport.loseConnection() 

class FileTransferClientFactory(protocol.ClientFactory): 
    protocol = FileTransferClientProtocol 

if __name__ == "__main__":
    reactor.connectTCP("localhost", 7000, FileTransferClientFactory()) 
    reactor.run() 
    '''
    filename = 'ftpserver.py'
    with open(filename, "w") as f:
        f.write(code1)
    filename = 'ftpclient.py'
    with open(filename, "w") as f:
        f.write(code2)

def udpechoclient():
    code1='''
#client
from twisted.internet import reactor,protocol

class UDPClient(protocol.DatagramProtocol):
    def startProtocol(self):
        self.transport.connect('127.0.0.2',8000)
        self.send_message()
    
    def send_message(self):
        message=input('Enter message: ')
        self.transport.write(message.encode())

    def datagramReceived(self, data, addr):
        print("Recieved message: ",data.decode())
        self.send_message()
    
client=reactor.listenUDP(0,UDPClient())
reactor.run()
    '''
    code2 = '''
#server
from twisted.internet import reactor,protocol

class UDPServer(protocol.DatagramProtocol):
    def datagramReceived(self, data, addr):
        print("Recieved message from",addr[0],": ",data.decode())
        self.transport.write(data,addr)

server_port=8000
server=reactor.listenUDP(server_port,UDPServer())
print("Server started on port",server_port)

reactor.run()
    '''
    filename = 'udpserver.py'
    with open(filename, "w") as f:
        f.write(code1)
    filename = 'udpclient.py'
    with open(filename, "w") as f:
        f.write(code2)

def udpftp():
    code1='''
#client
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class FileSender(DatagramProtocol):
    def startProtocol(self):
        self.transport.connect('127.0.0.1', 8000)
        file_path = "myfile.txt"
        with open(file_path, 'rb') as f:
            self.file_data = f.read()
        self.transport.write(self.file_data)

if __name__ == '__main__':
    reactor.listenUDP(0, FileSender())
    reactor.run()
    '''
    code2 = '''
#server
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class FileReceiver(DatagramProtocol):
    def datagramReceived(self, datagram, address):
        with open("received_file.txt", "wb") as f:
            f.write(datagram)

if __name__ == '__main__':
    reactor.listenUDP(8000, FileReceiver())
    reactor.run()

    '''
    filename = 'udpftpserver.py'
    with open(filename, "w") as f:
        f.write(code2)
    filename = 'udpftpclient.py'
    with open(filename, "w") as f:
        f.write(code1)

def arp():
    code1='''
#client
from twisted.internet import reactor, protocol
import struct

class RARPClient(protocol.Protocol):
    def connectionMade(self):
        rarp_packet_format = "!6s4s6s4s"
        request_packet = struct.pack(
            rarp_packet_format,
            bytes([00, 11, 22, 33, 44, 55]),  # Example source hardware address
            bytes([0, 0, 0, 0]),  # Example source protocol address
            bytes([17, 18, 19, 20, 21, 22]),  # Example target hardware address
            bytes([26, 27, 28, 29])  # Example target protocol address
        )
        a = input("Enter MAC address:")
        to_server = {'mac': a, 'req_format': request_packet, 'req': 'RARP_REQUEST'}
        self.transport.write(str(to_server).encode())
    
    def dataReceived(self, data):
        recv = eval(data.decode())
        rarp_packet_format = "!6s4s6s4s"
        (
            Source_Hardware_Address,
            Source_Protocol_Address,
            Target_Hardware_Address,
            Target_Protocol_Address
        ) = struct.unpack(rarp_packet_format, recv.get('reply_format'))
        
        print("Received RARP reply:")
        print("Source Hardware Address:", ":".join("{:02x}".format(byte) for byte in Source_Hardware_Address))
        print("Source Protocol Address:", ".".join(str(byte) for byte in Source_Protocol_Address))
        print("Target Hardware Address:", ":".join("{:02x}".format(byte) for byte in Target_Hardware_Address))
        print("Target Protocol Address:", ".".join(str(byte) for byte in Target_Protocol_Address))
        
        if recv.get('data').startswith('RARP_REPLY'):
            reply_parts = recv.get('data').split()
            if len(reply_parts) == 3:
                mac_address = reply_parts[1]
                ip_address = reply_parts[2]
                print(f"Received RARP reply: MAC = {mac_address}, IP = {ip_address}")
                self.transport.loseConnection()
            else:
                print("Invalid RARP reply")
                self.transport.loseConnection()
        else:
            print("Invalid MAC Address given!")
            self.transport.loseConnection()

class RARPClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return RARPClient()
    
    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()

reactor.connectTCP('localhost', 1234, RARPClientFactory())
reactor.run()
    '''
    code2='''
#server
from twisted.internet import reactor, protocol
import struct

class ARPServer(protocol.Protocol):
    def connectionMade(self):
        print("client connected")
    
    def dataReceived(self, data):
        global arp_table
        rec = eval(data.decode())
        mac_address = '0:0:0:0:0:0'
        
        arp_packet_format = "!6s4s6s4s"
        arp_data = struct.unpack(arp_packet_format, rec.get('req_format'))
        (
            Source_Hardware_Address,
            Source_Protocol_Address,
            Target_Hardware_Address,
            Target_Protocol_Address
        ) = arp_data
        
        print("Received ARP packet:")
        print("Source Hardware Address:", ":".join("{:02x}".format(byte) for byte in Source_Hardware_Address))
        print("Source Protocol Address:", ".".join(str(byte) for byte in Source_Protocol_Address))
        print("Target Hardware Address:", ":".join("{:02x}".format(byte) for byte in Target_Hardware_Address))
        print("Target Protocol Address:", ".".join(str(byte) for byte in Target_Protocol_Address))
        
        if rec.get('req') == "ARP_REQUEST":
            for i in arp_table:
                if i == rec.get('ip'):
                    mac_address = arp_table[i]
                else:
                    continue
            
            l = []
            for i in mac_address.split(':'):
                l.append(int(i))
            
            ip_address = rec.get('ip')
            response_packet = struct.pack(
                arp_packet_format,
                Target_Hardware_Address,
                Target_Protocol_Address,
                Source_Hardware_Address,
                bytes(l),
            )
            
            to_client = {'reply_format': response_packet}
            
            if mac_address != '0:0:0:0:0:0':
                arp_reply = f'ARP_REPLY {ip_address} {mac_address}\n'
                to_client['data'] = arp_reply
                self.transport.write(str(to_client).encode())
                print("MAC Address sent")
            else:
                self.transport.write(b'hi')
                print("Invalid IP received")
    
    def connectionLost(self, reason):
        print("client removed")
        return

class ARPServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return ARPServer()

arp_table = {}
arp_table['192.168.1.1'] = '00:11:22:33:44:55'

reactor.listenTCP(1234, ARPServerFactory())
reactor.run()
    '''
    filename = 'arpclient.py'
    with open(filename, "w") as f:
        f.write(code2)
    filename = 'arpserver.py'
    with open(filename, "w") as f:
        f.write(code1)

def rarap():
    code1='''
#client
from twisted.internet import reactor, protocol
import struct

class RARPClient(protocol.Protocol):
    def connectionMade(self):
        rarp_packet_format = "!6s4s6s4s"
        request_packet = struct.pack(
            rarp_packet_format,
            bytes([00, 11, 22, 33, 44, 55]),  # Example source hardware address
            bytes([0, 0, 0, 0]),  # Example source protocol address
            bytes([17, 18, 19, 20, 21, 22]),  # Example target hardware address
            bytes([26, 27, 28, 29])  # Example target protocol address
        )
        a = input("Enter MAC address:")
        to_server = {'mac': a, 'req_format': request_packet, 'req': 'RARP_REQUEST'}
        self.transport.write(str(to_server).encode())
    
    def dataReceived(self, data):
        recv = eval(data.decode())
        rarp_packet_format = "!6s4s6s4s"
        (
            Source_Hardware_Address,
            Source_Protocol_Address,
            Target_Hardware_Address,
            Target_Protocol_Address
        ) = struct.unpack(rarp_packet_format, recv.get('reply_format'))
        
        print("Received RARP reply:")
        print("Source Hardware Address:", ":".join("{:02x}".format(byte) for byte in Source_Hardware_Address))
        print("Source Protocol Address:", ".".join(str(byte) for byte in Source_Protocol_Address))
        print("Target Hardware Address:", ":".join("{:02x}".format(byte) for byte in Target_Hardware_Address))
        print("Target Protocol Address:", ".".join(str(byte) for byte in Target_Protocol_Address))
        
        if recv.get('data').startswith('RARP_REPLY'):
            reply_parts = recv.get('data').split()
            if len(reply_parts) == 3:
                mac_address = reply_parts[1]
                ip_address = reply_parts[2]
                print(f"Received RARP reply: MAC = {mac_address}, IP = {ip_address}")
                self.transport.loseConnection()
            else:
                print("Invalid RARP reply")
                self.transport.loseConnection()
        else:
            print("Invalid MAC Address given!")
            self.transport.loseConnection()

class RARPClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return RARPClient()
    
    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()

reactor.connectTCP('localhost', 1234, RARPClientFactory())
reactor.run()
    '''
    code2='''
from twisted.internet import reactor, protocol
import struct

class RARPServer(protocol.Protocol):
    def connectionMade(self):
        print("client connected")
 
    def dataReceived(self, data):
        global rarp_table
        rec = eval(data.decode())
        ip_address = '0.0.0.0'
        
        rarp_packet_format = "!6s4s6s4s"
        rarp_data = struct.unpack(rarp_packet_format, rec.get('req_format'))
        (
            Source_Hardware_Address,
            Source_Protocol_Address,
            Target_Hardware_Address,
            Target_Protocol_Address
        ) = rarp_data
        
        print("Received RARP packet:")
        print("Source Hardware Address:", ":".join("{:02x}".format(byte) for byte in Source_Hardware_Address))
        print("Source Protocol Address:", ".".join(str(byte) for byte in Source_Protocol_Address))
        print("Target Hardware Address:", ":".join("{:02x}".format(byte) for byte in Target_Hardware_Address))
        print("Target Protocol Address:", ".".join(str(byte) for byte in Target_Protocol_Address))
 
        if rec.get('req') == "RARP_REQUEST":
            for i in rarp_table:
                if i == rec.get('mac'):
                    ip_address = rarp_table[i]
                else:
                    continue 
            l = []
            for i in ip_address.split('.'):
                l.append(int(i))
                
            mac_address = rec.get('mac')
            response_packet = struct.pack(
                rarp_packet_format,
                Target_Hardware_Address,
                Target_Protocol_Address,
                Source_Hardware_Address,
                bytes(l),
            )
            
            to_client = {'reply_format': response_packet}
            
            if ip_address != '0.0.0.0':
                rarp_reply = f'RARP_REPLY {mac_address} {ip_address}\n'
                to_client['data'] = rarp_reply
                self.transport.write(str(to_client).encode())
                print("IP Address sent")
            else:
                self.transport.write(b'hi')
                print("Invalid MAC received")
    
    def connectionLost(self, reason):
        print("client removed")
        return

class RARPServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return RARPServer()

rarp_table = {}
rarp_table['00:11:22:33:44:55'] = '192.168.1.1'

reactor.listenTCP(1234, RARPServerFactory())
reactor.run()
    '''
    filename = 'rarpclient.py'
    with open(filename, "w") as f:
        f.write(code2)
    filename = 'rarpserver.py'
    with open(filename, "w") as f:
        f.write(code1)

def stopandwait():
    code1='''
from twisted.internet import reactor, protocol

class StopAndWaitClient(protocol.Protocol):
    def connectionMade(self):
        print("Connected to server.")
        self.send_ack()

    def send_ack(self):
        self.transport.write(input("Enter ack: ").encode())
        print("ACK sent")

    def dataReceived(self, data):
        message = data.decode()
        print("Message received:", message)
        self.send_ack()

    def connectionLost(self, reason):
        print("Connection lost:", reason.getErrorMessage())

class StopAndWaitClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return StopAndWaitClient()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed:", reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost:", reason.getErrorMessage())
        reactor.stop()

server_address = 'localhost'
server_port = 8000
factory = StopAndWaitClientFactory()
reactor.connectTCP(server_address, server_port, factory)
reactor.run()
    '''
    code2='''
from twisted.internet import reactor, protocol

class StopAndWaitServer(protocol.Protocol):
    def connectionMade(self):
        print("Client connected:", self.transport.getPeer())
        self.send_message()

    def send_message(self):
        message = input("Enter message: ")
        self.transport.write(message.encode())
        print("Message sent to client:", message)
        self.expected_ack = "ACK"

    def schedule_resend(self):
        self.resend_call = reactor.callLater(5, self.resend_message)

    def resend_message(self):
        print("ACK not received. Resending message...")
        self.send_message()

    def dataReceived(self, data):
        ack = data.decode()
        print("ACK received:", ack)
        if ack == self.expected_ack:
            print("ACK received. Message acknowledged.")
            self.send_message()
        else:
            print("Invalid ACK received.")
            self.schedule_resend()

    def connectionLost(self, reason):
        print("Client disconnected:")

class StopAndWaitServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return StopAndWaitServer()

server_port = 8000
factory = StopAndWaitServerFactory()
reactor.listenTCP(server_port, factory)
reactor.run()
    '''
    filename = 'stopandwaitclient.py'
    with open(filename, "w") as f:
        f.write(code2)
    filename = 'stopandwaitserver.py'
    with open(filename, "w") as f:
        f.write(code1)
def http():
    code='''
from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.client import readBody


def download_web_page(url):
    agent = Agent(reactor)

    def handle_response(response):
        d = readBody(response) 
        def process_body(body):
            print(body.decode()) 
            reactor.stop()

        d.addCallback(process_body)
        return d

    def handle_error(error):
        print(f"An error occurred: {error}") 
        reactor.stop()

    d = agent.request(b"GET", url.encode()) 
    d.addCallbacks(handle_response, handle_error)
    reactor.run()

if __name__ == "__main__":
    download_web_page("http://www.google.com/")
    '''
    filename = 'http.py'
    with open(filename, "w") as f:
        f.write(code)

def remoteprocedurecall():
    code1='''
from twisted.internet import reactor, protocol
class RPCClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(b"add 10 5")

    def dataReceived(self, data):
        result = data.decode().strip()
        print("Result:", result)
        self.transport.loseConnection()

class RPCClientFactory(protocol.ClientFactory):
    protocol = RPCClientProtocol

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        reactor.stop()

if __name__ == "__main__":
    from twisted.internet import endpoints

    endpoint = endpoints.TCP4ClientEndpoint(reactor, "localhost", 8000)
    factory = RPCClientFactory()
    endpoint.connect(factory)

    reactor.run()
    '''
    code2='''
from twisted.internet import reactor, protocol


class RPCServerProtocol(protocol.Protocol):
    def dataReceived(self, data):
        request = data.decode().strip()
        result = self.processRequest(request)
        self.transport.write(result.encode())

    def processRequest(self, request):
        # Process the request and return the result
        # Replace this with your own server-side logic
        if request == "add 10 5":
            return str(10 + 5)
        else:
            return "Invalid request"

class RPCServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return RPCServerProtocol()

if __name__ == "__main__":
    reactor.listenTCP(8000, RPCServerFactory())
    print("RPC server is running...")
    reactor.run()
    '''
    filename = 'client.py'
    with open(filename, "w") as f:
        f.write(code1)
    filename = 'server.py'
    with open(filename, "w") as f:
        f.write(code2)

def subnetting():
    code = '''
from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineOnlyReceiver
import ipaddress


SUBNET = ipaddress.IPv4Network("192.168.0.0/24")
print(SUBNET)
class SubnetCheckerProtocol(LineOnlyReceiver):
    def connectionMade(self):
        self.sendLine(b"Enter an IP address to check:")

    def lineReceived(self, line):
        ip_address = line.strip().decode()
        if self.is_in_subnet(ip_address):
            self.sendLine(b"IP address is within the subnet")
        else:
            self.sendLine(b"IP address is outside the subnet")
        self.transport.loseConnection()

    def is_in_subnet(self, ip_address):
        try:
            ip = ipaddress.IPv4Address(ip_address)
            return ip in SUBNET
        except ipaddress.AddressValueError:
            return False

class SubnetCheckerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return SubnetCheckerProtocol()


if __name__ == "__main__":
    reactor.listenTCP(8000, SubnetCheckerFactory())
    print("Subnet checker server is running...")
    reactor.run()
    '''
    filename = 'server.py'
    with open(filename, "w") as f:
        f.write(code)
def dns():
    code1='''
#client
from twisted.internet import reactor, protocol

class DNSClientProtocol(protocol.Protocol):
    def connectionMade(self):
        domain = input("Enter a domain name: ")
        self.transport.write(domain.encode())

    def dataReceived(self, data):
        response = data.decode()
        print("Response:", response)
        self.transport.loseConnection()

class DNSClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return DNSClientProtocol()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

if __name__ == "__main__":
    reactor.connectTCP("localhost", 53, DNSClientFactory())
    reactor.run()
    '''
    code2 = '''
#server
from twisted.internet import reactor, protocol


class DNSProtocol(protocol.Protocol):
    def dataReceived(self, data):
        request = data.strip()
        response = self.processRequest(request)
        self.transport.write(response)

    def processRequest(self, request):
        # Replace this logic with your own DNS processing
        # Here, we simply return a hardcoded response
        if request == b"www.example.com":
            return b"192.168.0.1"
        else:
            return b"Unknown domain"

class DNSFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return DNSProtocol()


if __name__ == "__main__":
    reactor.listenTCP(53, DNSFactory())
    print("DNS server is running...")
    reactor.run()
    '''
    filename = 'client.py'
    with open(filename, "w") as f:
        f.write(code1)
    filename = 'server.py'
    with open(filename, "w") as f:
        f.write(code2)
def smtp():
    code1='''
#client
from twisted.internet import protocol, reactor

class SMTPClientProtocol(protocol.Protocol):
    def connectionMade(self):
        self.sendLine(b'HELO client.example.com')

    def dataReceived(self, data):
        response = data.decode().strip()
        print('Server:', response)

        if response.startswith('250'):
            self.sendLine(b'MAIL FROM:<john@example.com>')
        elif response.startswith('250'):
            self.sendLine(b'RCPT TO:<sarah@example.com>')
        elif response.startswith('250'):
            self.sendLine(b'DATA')
        elif response.startswith('354'):
            self.sendLine(b'From: john@example.com\r\n'
                          b'To: sarah@example.com\r\n'
                          b'Subject: Hello Sarah\r\n'
                          b'\r\n'
                          b'Hi Sarah, how are you doing? Just wanted to say hello!\r\n'
                          b'.')
        elif response.startswith('250'):
            self.sendLine(b'QUIT')
        elif response.startswith('221'):
            self.transport.loseConnection()

    def sendLine(self, line):
        self.transport.write(line + b'\r\n')

    def connectionLost(self, reason):
        print('Connection lost:', reason)

class SMTPClientFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return SMTPClientProtocol()

if __name__ == '__main__':
    reactor.connectTCP('localhost', 25, SMTPClientFactory())
    reactor.run()
    '''
    code2 ='''
#server
from twisted.internet import protocol, reactor

class SMTPServerProtocol(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(b'220 smtp.example.com Simple Mail Transfer Service Ready\r\n')

    def dataReceived(self, data):
        request = data.decode().strip()

        if request.startswith('HELO') or request.startswith('EHLO'):
            self.transport.write(b'250 Hello ' + request.split()[1].encode() + b', pleased to meet you\r\n')
        elif request.startswith('MAIL FROM:'):
            self.transport.write(b'250 OK\r\n')
        elif request.startswith('RCPT TO:'):
            self.transport.write(b'250 OK\r\n')
        elif request == 'DATA':
            self.transport.write(b'354 Start mail input; end with <CRLF>.<CRLF>\r\n')
            self.state = 'DATA'
        elif self.state == 'DATA' and request == '.':
            self.transport.write(b'250 OK, message received and queued for delivery\r\n')
            self.state = 'IDLE'
        elif request == 'QUIT':
            self.transport.write(b'221 Goodbye\r\n')
            self.transport.loseConnection()
        else:
            self.transport.write(b'500 Command not recognized\r\n')

    def connectionLost(self, reason):
        print('Connection lost:', reason)


class SMTPServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return SMTPServerProtocol()


if __name__ == '__main__':
    reactor.listenTCP(25, SMTPServerFactory())
    reactor.run()
    '''
    filename = 'client.py'
    with open(filename, "w") as f:
        f.write(code1)
    filename = 'server.py'
    with open(filename, "w") as f:
        f.write(code2)

def snmp():
    code1='''
#client
from twisted.internet import reactor, protocol
import socket

class SNMPClientProtocol(protocol.DatagramProtocol):
    def startProtocol(self):
        ip_address = socket.gethostbyname("localhost")
        self.transport.connect(ip_address, 161)
        self.sendRequest()

    def sendRequest(self):
        self.transport.write("SNMP GET request".encode())

    def datagramReceived(self, data, addr):
        print("Received data:", data.decode())
        # Process the received SNMP response
        reactor.stop()


if __name__ == "__main__":
    reactor.listenUDP(0, SNMPClientProtocol())
    reactor.callLater(1, reactor.stop) 
    reactor.run()

    '''
    code2='''
#server
from twisted.internet import reactor, protocol

class SNMPProtocol(protocol.DatagramProtocol):
    def datagramReceived(self, data, addr):
        print("Received data:", data.decode())
        response_data = "SNMP response"
        self.transport.write(response_data.encode(), addr)

if __name__ == "__main__":
    reactor.listenUDP(161, SNMPProtocol())
    reactor.run()

    '''
    filename = 'client.py'
    with open(filename, "w") as f:
        f.write(code1)
    filename = 'server.py'
    with open(filename, "w") as f:
        f.write(code2)

def flooding():
    code1='''
#client
from twisted.internet import reactor, protocol

class FloodingClient(protocol.Protocol):
    def __init__(self, node_id):
        self.node_id = node_id

    def connectionMade(self):
        print(f"Client {self.node_id} connected to the server.")
        self.sendMessage()

    def dataReceived(self, data):
        message = data.decode()
        print(f"Client {self.node_id} received message: {message}")

    def sendMessage(self):
        message = f"Hello from Client {self.node_id}"
        self.transport.write(message.encode())

    def connectionLost(self, reason):
        print(f"Client {self.node_id} disconnected from the server.")

    def startProtocol(self):
        pass

    def stopProtocol(self):
        reactor.stop()


class FloodingClientFactory(protocol.ClientFactory):
    def __init__(self, node_id):
        self.node_id = node_id

    def buildProtocol(self, addr):
        return FloodingClient(self.node_id)

    def clientConnectionFailed(self, connector, reason):
        print(f"Connection failed for Client {self.node_id}: {reason.getErrorMessage()}")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print(f"Connection lost for Client {self.node_id}: {reason.getErrorMessage()}")
        reactor.stop()


if __name__ == "__main__":
    node_id = "C"  # Replace with the ID of the client node
    factory = FloodingClientFactory(node_id)
    reactor.connectTCP("localhost", 8000, factory)  # Replace with the IP address and port of the server
    reactor.run()
    '''
    code2='''
#server
from twisted.internet import reactor, protocol

class FloodingProtocol(protocol.Protocol):
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = []

    def connectionMade(self):
        print(f"Node {self.node_id} connected to the network.")
        self.startFlooding()    

    def connectionLost(self, reason):
        print(f"Node {self.node_id} disconnected from the network.")

    def dataReceived(self, data):
        message = data.decode()
        print(f"Node {self.node_id} received message: {message}")

    def sendMessage(self, message):
        for neighbor in self.neighbors:
            self.transport.write(message.encode(), neighbor)

    def startFlooding(self):
        message = f"Hello from Node {self.node_id}"
        self.sendMessage(message)
        reactor.callLater(1, self.startFlooding)

    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def removeNeighbor(self, neighbor):
        if neighbor in self.neighbors:
            self.neighbors.remove(neighbor)

    def startProtocol(self):
        pass

    def stopProtocol(self):
        reactor.stop()


class FloodingFactory(protocol.Factory):
    def __init__(self, node_id):
        self.node_id = node_id

    def buildProtocol(self, addr):
        return FloodingProtocol(self.node_id)


if __name__ == "__main__":
    node_id = "A"  # Replace with the ID of the current node
    factory = FloodingFactory(node_id)
    reactor.listenTCP(8000, factory)  # Replace with the desired port number
    reactor.run()
    '''
    filename = 'client.py'
    with open(filename, "w") as f:
        f.write(code1)
    filename = 'server.py'
    with open(filename, "w") as f:
        f.write(code2)

def menulist():
    print("ping,traceroute,star,bus,mesh,ring,tcpchat,tcpechoclient,tcpftp,\nudpechoclient,udpftp,arp,rarp,stopandwait,http,remoteprocedurecall\nsubnetting,dns,snmp,flooding")