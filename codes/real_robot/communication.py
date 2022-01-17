import socket

# Open TCP server
class server_tcp:
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = 0

    def __init__(self, port):
        server_address = ('', port)

        self.sock.bind(server_address)

        print('[#]: Socket a la espera...')
        self.sock.listen(1)

        self.reconnect()
        

    def reconnect(self):            

        try:
                self.connection, address = self.sock.accept()
                print('\t- Conectado a: ' + str(address[0]))
                self.connected+=1
        except (BlockingIOError, KeyboardInterrupt):
            pass


    def recibir(self):
        data = ""

        try:
            data = self.connection.recv(6).decode()
        except(ConnectionResetError, ValueError, KeyboardInterrupt) as e:
            print("[#]: Conexion cerrada!")
            self.connected = 0

        return data
         

    def __del__(self):
        print("[#]: Cerrando Servidor...")
        self.sock.detach()
        self.sock.close()



# Class to open TCP clients
class client_tcp:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    __is_open = False

    def __init__(self,server_host, port):
        server_address = (server_host, port)

        print('[#]: Conectandose a {} port {}'.format(*server_address))
        self.sock.connect(server_address) 
        print("[#]: Conectado al servidor!")
        self.__is_open = True


    def enviar(self, data):

        MESSAGE = data
        MESSAGE = MESSAGE.encode()
        try:
            self.sock.sendall(MESSAGE)
        except (ConnectionResetError, KeyboardInterrupt):
            print("[#]: Conexion cerrada!")
            self.__is_open = False


    def recibir(self):

        data = ""

        try:
            data = self.sock.recv(1).decode()
       
        except (ConnectionResetError, ValueError, KeyboardInterrupt):
            print("[#]: Conexion cerrada!")
            self.__is_open = False

        return data


    def is_open(self):
        return self.__is_open


    def __del__(self):
        print("[#]: Cerrando Cliente...")
        self.sock.close()