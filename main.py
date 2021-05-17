import multiprocessing
import socket
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Tools.scripts.serve import app

from ServerSocketUI import *
import threading

# create apllication





SERVER_ip = socket.gethostbyname(socket.gethostname())   #getting ip from computer
PORT = 10001                                             # defining port
income_client, income_data, client_data = [], [],[]
con_count = 0



def get_time():
    """
    get the time and date
    :return: example:... 13:51:55, 04/19/2021
    """
    from datetime import datetime
    now = datetime.now()
    datetime = now.strftime("%H:%M:%S, %m/%d/%Y")
    #print(datetime)
    return datetime


def handle(connection, address):

   # global connection_count
    import logging
    date_time = []
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-%r" % (address,))


    try:
        logger.debug("Connected %r at %r", connection, address)



        while True:
            data = connection.recv(1024)
            data = data.decode("UTF-8")
            if data == "":
                logger.debug("Socket closed remotely")

                break
            logger.debug(f"Received data %r", data)
            logger.debug(f"PMDs addres %r",address)
            c =  Pmd(data, address)
            print("Connected :",c.serialPmd())
            #send_message(connection)
            #income_client.append(address[0])
            #income_data.append(data)
            #d = get_time()
            #date_time.append(d)


            #file = open("pmd_log.csv", "w")
            #file.write("data;" + data + ";" + "time;" + d)
            #connection.sendall(data) #send back data to the client
            #logger.debug("Sent data")

    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing socket")
        #Pmd.ipPmd()
        #file.close()
        #client_data = zip(income_client, income_data, date_time)
        #client_data = list(client_data)


        #print(f"client data: {client_data}\n ", end ="", flush=True)
        #liste = [i for i in client_data]

        #for liste in client_data:
            #print(f"Client adress and data: {liste}.....")





def get_serial():
    """
    split data for serial number
    :return:
    """


class Pmd:
    def __init__(self, income_data, pmd_address):
        """
        for create Pmd's object
        income data example: \x0221553PMO_0_2C00789EBD_0_333_0_...._V.5.2.2._\x0506\x03\r\n
        :param income_pmd: PMD's version, PMD's serial number, Command from PMD, PMD address for get PMD's ip address
        """
        self.pmd_address = pmd_address
        self.income_data = income_data
        self.verion_pmd = ""
        self.serial_pmd = ""
        self.command_pmd = ""
        self.ip_pmd = ""
        self.rfid_pmd = ""

    def incomePmd(self):
        """
        PMD's datas
        :return:
        """
        pass

    def versionPmd(self):
        """
        get the version of PMD
        income data: \x0221553PMO_0_2C00789EBD_0_333_0_...._V.5.2.2._\x0506\x03\r\n
        :return: V.5.2.2.
        """
        character_version = 8                       # V.5.2.2. is 8 character if its change we should redefine
        hyphen_version = 1                          # pass hyphen before \x05 bit
        index =  self.income_data.find("\x05")
        l_index = index - hyphen_version            # first index
        f_index = index - character_version         # last index
        self.version_pmd = self.income_data[f_index:l_index]

    def serialPmd(self):
        """
        income data: \x0221553PMO_0_2C00789EBD_0_333_0_...._V.5.2.2._\x0506\x03\r\n
        split serial number from income data
        :return: ex. 21553
        """
        len_of_serial = 6                          # ex. serial:  21553
        s_index = 0                                # start index: \x02
        f_index =  s_index + 1
        l_index =  s_index + len_of_serial
        self.serial_pmd = self.income_data[f_index:l_index]
        return self.serial_pmd

    def commandPMD(self):
        """
        income data: \x0221553PMO_0_2C00789EBD_0_333_0_...._V.5.2.2._\x0506\x03\r\n
        split comand from income data
        :return: PMO, MY, BB, SS
        """
        f_index = 6
        l_index = self.income_data.find("_0_") + 3    # _0_ include 3 character
        self.command_pmd = income_data[f_index:l_index]
        return self.command_pmd

    def ipPmd(self):
        """
        ex. socket address: ('10.10.11.3', 10829)
        :return:ex. '10.10.11.3'
        """
        self.ip_pmd = self.command_pmd[0]
        return self.ip_pmd

    def rfidPmd(self):
        """
        income data: \x0221553PMO_0_2C00789EBD_0_333_0_...._V.5.2.2._\x0506\x03\r\n
        split rfid numbers from income data
        :return:ex. 2C00789EBD
        """
        len_rfid = 10
        f_index = self.income_data.find("_0_") + 3    # _0_ include 3 character
        l_index = f_index + len_rfid
        self.rfid_pmd = self.income_data[f_index:l_index]
        return self.rfid_pmd









class Server(object):

    def __init__(self, hostname, port):
        import logging
        self.logger = logging.getLogger("server")
        self.hostname = hostname
        self.port = port
        self.ip = ""
        self.address = ""




    def start(self):

        con_count = 0
        self.logger.debug("listening")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            self.conn, self.address = self.socket.accept()
            connection_count = 1
            send_message(self.conn)
            con_count += 1
            print("Count of connection: ", con_count)
            # ui.TableWidget.insert(self.conn)
            #self.logger.debug("Got connection")
            self.ip = self.address[0]

            #print(f"connection object: {self.conn}")

            #starting multiprocessing between start() method and handle() func.
            process = multiprocessing.Process(target=handle, args=(self.conn, self.address))
            process.daemon = True
            process.start()

            #self.logger.debug("Started process %r", process)


# def thread():
    # thread = threading.Thread(target = Server)
    # thread.daemon = True
    # s.start

def send_message(conn):

    try:
        #addr = int(input("client addres: "))
       # sleep(.2)
        #message = input("Input message: ")
        #message = "\x0200000RS\x0531\x03"
        message = '\x0200000PMO\x0562\x03'
        message = message.encode("utf-8")
        #addr = ('192.168.1.25', 10000)
        conn.send(message)
        #print("data:", message)
    except EOFError as e:
        print(end = "")




if __name__ == "__main__":

    import logging
    logging.basicConfig(level=logging.DEBUG)
    server = Server(SERVER_ip, PORT)
    print(f"Server IP: {SERVER_ip}")

    Application = QApplication(sys.argv)

    mainwindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainwindow)
    #ui.pushButton.clicked.connect(thread)
    def show_application():
        mainwindow.show()


    app_thread = threading.Thread(target=show_application())

    app_thread.start()
    try:
        logging.info("Listening")
        server.start()
        

    except:
        logging.exception("Unexpected exception")
    finally:
        logging.info("Shutting down")
        for process in multiprocessing.active_children():
            logging.info("Shutting down process %r", process)
            process.terminate()
            process.join()
    logging.info("All done")
    sys.exit()
    # sys.exit(main.exec())
