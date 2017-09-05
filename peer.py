import socket
import threading
import SocketServer
import time
import sys
import os	

class Peer_2_Peer:	
    list_peers = []
    list_connected_peers = []
    discover_list = []
    discover_list_2 = []

    def __init__(self):
	Peer_2_Peer.list_peers = [['127.0.0.1', 5000]]

	Peer_2_Peer.list_connected_peers = []

    def discover_peers(self, list_n, arg_TTL, check_bit):
        for peers_ip, peer_prt in list_n:
            a1 = self.check_if_peer_connected(peers_ip, int(peer_prt))
            if a1 != 1:
                sock = self.connect_funct(peers_ip, peer_prt)
            else:
                for iip, s, pprt in Peer_2_Peer.list_connected_peers:
                    if iip == peers_ip and pprt == peer_prt:
                        sock = s
            sock.sendall('DISCOVER')#send command
            data = sock.recv(64)
            print data
            sock.sendall(str(arg_TTL-1))#send TTL
            data = sock.recv(64)
            print data
            data = sock.recv(1) #recieve # of knwn peers
            data_s = int(data)
            while(data_s != 0):
                #print 'size = ' + str(data_s)
                data_size_1 = sock.recv(1)
                data_ip = sock.recv(int(data_size_1))#recieve ip for each peer
                data_size_2 = sock.recv(1)
                data_port = sock.recv(int(data_size_2))#recieve ip for each peer
                data = [data_ip, int(data_port)]
                a = self.check_if_peer_known(data)
                if a != 1:
                    if check_bit == 0:
                        Peer_2_Peer.discover_list.append(data)
                        #print 'discover_list: '
                        #print Peer_2_Peer.discover_list
                        #print '' 
                        if len(Peer_2_Peer.discover_list_2) != 0:
                            for n in Peer_2_Peer.discover_list_2:
                                a_check = self.check_if_peer_known(n)
                                if a_check != 1:
                                    Peer_2_Peer.list_peers.append(n)
                            Peer_2_Peer.discover_list_2 = []
                        #print '===='
                        #print Peer_2_Peer.list_peers
                    else:
                        Peer_2_Peer.discover_list_2.append(data)
                        #print 'discover_list_2: '
                        #print Peer_2_Peer.discover_list_2
                        #print ''
                        if len(Peer_2_Peer.discover_list) != 0:
                            for n in Peer_2_Peer.discover_list:
                                a_check = self.check_if_peer_known(n)
                                if a_check != 1:
                                    Peer_2_Peer.list_peers.append(n)
                            Peer_2_Peer.discover_list = []
                        #print '++++++'
                        #print Peer_2_Peer.list_peers
                data_s = data_s - 1
        return None
				
    def add_peer(self, ip_peer):
	Peer_2_Peer.list_peers.append(ip_peer)
	return None
	
    def get_args(self, a):
	arg_command = ''
	arg_1 = ''
	arg_2 = ''
	arg_3 = ''
	arg_number = 0
		
	try:
            for i in a:
		if arg_number == 0:
			if i == ' ':
				arg_number = arg_number + 1
			else:
				arg_command = arg_command + i
		elif arg_number == 1:
			if i == ' ':
				arg_number = arg_number + 1
			else:
				arg_1 = arg_1 + i
		elif arg_number == 2:
			if i == ' ':
				arg_number = arg_number + 1
			else:
				arg_2 = arg_2 + i
		elif arg_number == 3:
			if i == ' ':
				arg_number = arg_number + 1
			else:
				arg_3 = arg_3 + i
		else:
			print 'You have Entered too many arguments'
	except:
		print 'Usage Error!'
		print 'Usage : <FileName> <IP> <PortNumber>'
		print ''
		sys.exit(-1)
			
	return arg_command, arg_1, arg_2, arg_3

    def lists_all(self, sock):
	f = []
	ff = []
	i = 1
	
	while True:
            data_number = sock.recv(1)
	    print '----------------------------'
            data_size = sock.recv(int(data_number))
            data = sock.recv(int(data_size))
            if 'DONE***DONE***DONE' in data:
                break
            print data
            print '----------------------------'

            data_number = sock.recv(1)
            data_size = sock.recv(int(data_number))
            if int(data_size) != 0:
                while True:
                    data_number_1 = sock.recv(1)
                    data_size_1 = sock.recv(int(data_number_1))
                    data = sock.recv(int(data_size_1))
                    f.append(data)
                    print data
                    if int(data_size) == i:
                        break
                    else:
                        i = i + 1
            i = 1
            data_number = sock.recv(1)
            data_size = sock.recv(int(data_number))
            if int(data_size) != 0:
                while True:
                    data_number_1 = sock.recv(1)
                    data_size_1 = sock.recv(int(data_number_1))
                    data = sock.recv(int(data_size_1))
                    ff.append(data)
                    print data
                    if int(data_size) == i:
                        break
                    else:
                        i = i + 1
	return None

    def print_name(self, f):
		f_dir = ''
		n = 1 
		for i in f:
			if n > (len('C:\Users\Coordinator\Desktop\S\Database')+ 1):
				f_dir = f_dir + i
				n = n + 1
			n = n + 1
		#print f_dir + ':'
		return f_dir

    def print_list(self, f):         
	for i in f:
            print i
	return None

    def list_all(self):
        for f_1, f_2, f_3 in os.walk('C:\Users\Coordinator\Desktop\S\Database'):
            print self.print_name(f_1)
            print'-----------------------------------'
            if len(f_2) != 0:
                self.print_list(f_2)

            if len(f_3) != 0:
                self.print_list(f_3)
            print'-----------------------------------'
	return None

    def connect_funct(self, arg_1, arg_2):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (arg_1, int(arg_2))
        print 'Connecting to ip-address %s port %s' % address
	sock.connect(address)
	print Peer_2_Peer.list_connected_peers
	Peer_2_Peer.list_connected_peers.append([arg_1, sock, int(arg_2)])
	#print Peer_2_Peer.list_peers
	i = self.check_if_peer_known([arg_1, int(arg_2)])
	if i != 1:
            self.add_peer([arg_1, int(arg_2)])
        #print Peer_2_Peer.list_peers
        print Peer_2_Peer.list_connected_peers
	return sock

    def check_if_peer_known(self, elemt):
        for n in Peer_2_Peer.list_peers:
            if n == elemt:
                return 1
        return None

    def check_if_peer_connected(self, elemt1, elemt2):
        for ip, sock, prt in Peer_2_Peer.list_connected_peers:
            if ip == elemt1 and prt == elemt2:
                return 1
        return None
 
    def client_logic(self, arg_command, arg_1, arg_2, arg_3, letter):
        try:
	    if((arg_command.upper() == 'LISTL') or (arg_command == '2')):
                #print 'Recieved ' + arg_command
                self.list_all()
                return None
                ###############1##############
            elif((arg_command.upper() == 'RESET') or (arg_command == '6')):
                print 'Resetting List of Peers'
                print 'Before: '
                print Peer_2_Peer.list_peers
                Peer_2_Peer.list_peers = [['127.0.0.1', 5000]]
                print 'After: '
                print Peer_2_Peer.list_peers
                return None
                ###############2##############
            elif((arg_command.upper() == 'QUIT') or (arg_command == '7')):
                if(len(Peer_2_Peer.list_connected_peers)) != 0:
                    print '%s Peers connected to this system that needs to be closed first' % str(len(Peer_2_Peer.list_connected_peers))
                    for iip, sock, prtt in Peer_2_Peer.list_connected_peers:
                        sock.sendall('BYE')
                        #sock.sendto('BYE', address)
		return 1
                ###############3##############
	    elif((arg_command.upper() == 'LISTR') or (arg_command == '1')):
                if arg_1 == None or arg_1 == '' or arg_2 == '' or arg_2 == None:
                    print 'Missing Arguments'
                    return None
                a2 = self.check_if_peer_connected(arg_1, int(arg_2))
                if a2 != 1:
                    sock = self.connect_funct(arg_1, arg_2)
                    sock.sendall('LISTR')
                    data = sock.recv(64)
                    print data
                    self.lists_all(sock)
                else:
                    print 'Peer already connected'
                    for iip, sock, prtt in Peer_2_Peer.list_connected_peers:
                        if iip == arg_1 and prtt == int(arg_2):
                            sock.sendall('LISTR')
                            data = sock.recv(64)
                            print data
                            self.lists_all(sock)
                return None
                ###############4############
            elif((arg_command.upper() == 'SEARCH') or (arg_command == '5')):
                if arg_1 == None or arg_1 == '' or arg_2 == '' or arg_2 == None:
                    print 'Missing Arguments'
                    return None
                #---------------------------------DISCOVER--------------------#
                print 'List of Known Peers before '
                print Peer_2_Peer.list_peers
                ii = int(arg_2)
                self.discover_peers(Peer_2_Peer.list_peers, ii, 0)
                ii = ii - 1
                check_bit = 1
                while ii != 0:
                    if check_bit == 1:
                        self.discover_peers(Peer_2_Peer.discover_list, ii, check_bit)
                    else:
                        self.discover_peers(Peer_2_Peer.discover_list_2, ii, check_bit)
                    check_bit = (check_bit + 1) % 2
                    ii = ii - 1
                print 'Known Peers After '
                print Peer_2_Peer.list_peers
                #-------------------------------------------------------------#
                for peers_ip, peer_prt in Peer_2_Peer.list_peers:
                    a1 = self.check_if_peer_connected(peers_ip, peer_prt)
                    if a1 != 1:
                        sock = self.connect_funct(peers_ip, peer_prt)
                        sock.sendall('SEARCH')#send command
                        data = sock.recv(64)
                        print data
                        sock.sendall(arg_1)#send filename
                        data = sock.recv(64)
                        if 'SUCCESS' in data:
                            print data +  ' ' + str(peers_ip) + ' ' + str(peer_prt)              
                    else:
                        print 'Peer already connected'
                        for iip, sock, prtt in Peer_2_Peer.list_connected_peers:
                            if iip == peers_ip and prtt == int(peer_prt):
                                sock.sendall('SEARCH')#send command
                                data = sock.recv(64)
                                print data
                                sock.sendall(arg_1)#send filename
                                data = sock.recv(64)
                                if 'SUCCESS' in data:
                                    print data +  ' ' + str(peers_ip) + ' ' + str(peer_prt)           
                return None
                ###############5##############
            elif((arg_command.upper() == 'DISCOVER') or (arg_command == '4')):
                if arg_1 == None or arg_1 == '':
                    print 'Missing Argument'
                    return None
                print 'List of Known Peers before '
                print Peer_2_Peer.list_peers
                ii = int(arg_1)
                self.discover_peers(Peer_2_Peer.list_peers, ii, 0)
                ii = ii - 1
                check_bit = 1
                while ii != 0:
                    #print Peer_2_Peer.discover_list
                    #print ii
                    if check_bit == 1:
                        self.discover_peers(Peer_2_Peer.discover_list, ii, check_bit)
                    else:
                        self.discover_peers(Peer_2_Peer.discover_list_2, ii, check_bit)
                    check_bit = (check_bit + 1) % 2
                    ii = ii - 1
                print 'Known Peers After '
                print Peer_2_Peer.list_peers
                ###############6##############
            elif((arg_command.upper() == 'GET') or (arg_command == '3')):
                if arg_1 == None or arg_1 == '' or arg_2 == '' or arg_2 == None or arg_3 == '' or arg_3 == None:
                    print 'Missing Arguments'
                    return None
                a1 = self.check_if_peer_connected(arg_2, int(arg_3))
                if a1 != 1:
                    sock = self.connect_funct(arg_2, int(arg_3))
                    sock.sendall('GET')
                    data = sock.recv(64)
                    print data
                    sock.sendall(arg_1)
                    data = sock.recv(128)
                    if '$ERROR$' in data:
                            print data
                            return None
                    print data
                    xsx, ddrrx = self.file_receive(sock, arg_1)
                    if xsx != 1:                         
                        self.remove_file(ddrrx)
                    data = sock.recv(128)
                    print data
                    print '--***********----***DONE***----***********--'
                else:
                    for iip, sock, pprrtt in Peer_2_Peer.list_connected_peers:
                        if iip == arg_2 and pprrtt == int(arg_3):
                            #sock = s
                            sock.sendall('GET')
                            data = sock.recv(64)
                            print data
                            sock.sendall(arg_1)
                            data = sock.recv(128)
                            if '$ERROR$' in data:
                                    print data
                                    return None
                            print data
                            xsx, ddrrx = self.file_receive(sock, arg_1)
                            if xsx != 1:                         
                                self.remove_file(ddrrx)
                            data = sock.recv(128)
                            print data
                            print '--***********----***DONE***----***********--'
            else:
                print 'ERROR. No such command'
        except:
            print ''
	    print("Error. Something went wrong somewhere")
        return None

    def check_file_name_exist(arg_n):
        f_dir = []
        drr = None
        actual_name = None
        for f_1, f_2, f_3 in os.walk('C:\Users\Coordinator\Desktop\S\Database'):
            if len(f_2) != 0:
                for d in f_2:
                    f_dir.append(d)

        for dr in f_dir:   
            f_dir = 'C:\Users\Coordinator\Desktop\S\Database\%s' % (dr)
            f = os.listdir(f_dir)
            for fl in f:
                if arg_n == fl:
                    drr = dr
                    actual_name = fl
                    return 1, drr, actual_name

        return 0, drr, actual_name

    def remove_file(self, ddrr):
        print 'Deleted ' + ddrr
        os.remove(ddrr)
        return None

    def file_receive(self, sock, arg_n):
        iss = 0
        mss = ''
        nn = 'wb'
        
        for i in arg_n:
            if iss == 1:
                mss = mss + i
            if i == '.':
                iss = 1
        if mss == 'mov' or mss == 'wmv':
            name = 'C:\Users\Coordinator\Desktop\S\Database\Vidoes\%s' % (arg_n)
        elif mss == 'wma' or mss == 'mp3' or mss == 'mp4':
            name = 'C:\Users\Coordinator\Desktop\S\Database\Music\%s' % (arg_n)
        elif mss == 'jpg' or mss == 'bmp':
            name = 'C:\Users\Coordinator\Desktop\S\Database\Pictures\%s' % (arg_n)
        elif mss == 'txt' or mss == 'py' or mss == 'c':
            name = 'C:\Users\Coordinator\Desktop\S\Database\Files\%s' % (arg_n)
        else:
            name = 'C:\Users\Coordinator\Desktop\S\Database\Files\%s' % (arg_n)
        try:
            size = sock.recv(64)
            print size

            f1 = open(name, nn)   

            i = 1
            quit_bit = 0
            sum_bytes = 0
            # Receive the data in small chunks and write it to a file
            # the file is is known in advance to be 16,958,907 bytes
            while True:
                data = sock.recv(4096)
                if '^^DONE+DONE/DONE-DONE^^' in data:
                    new_data = ''
                    n = 0

                    for iii in data:
                        if n < (len(data) - 23):
                            new_data = new_data + iii
                        n = n + 1
                    data = new_data
                    quit_bit = 1
                #print '----------------'
                if data:
                # write the data to the file
                    f1.write(data)
                    i = i + 1
                    sum_bytes = sum_bytes + len(data)
                    print 'received chunk ', i, 'with ', len(data), ' bytes, ', \
                    ' sum_bytes = ', sum_bytes, ' size', size
                    if quit_bit:
                        break
                else:
                    print 'received line with no data ?? '
                    print ' sum_bytes = ', sum_bytes
                    break
            print '------'
            print 'sum_bytes = ', sum_bytes
            f1.close
            if(quit_bit == 1):
                #data = sock.recv(128)
                #print data
                print 'Received file with', sum_bytes, ' bytes, Closing file ', arg_n
                return 1, name
            else:
                print '**ERROR**'
                return 0, name
        except:
            #data = sock.recv(64)
            #print data
            print " Error. Something went wrong somewhere. Try Again"
            return 0, name
        return None, name

    def send_file(connection, arg_n):
        iss = 0
        mss = ''
        nn = 'rb'
        
        for i in arg_n:
            if iss == 1:
                mss = mss + i
            if i == '.':
                iss = 1
            # Send a file over a socket
        if mss == 'mov' or mss == 'wmv':
            name = 'C:\Users\Coordinator\Desktop\S\Database\Vidoes\%s' % (arg_n)
        elif mss == 'wma' or mss == 'mp3' or mss == 'mp4':
            name = 'C:\Users\Coordinator\Desktop\S\Database\Music\%s' % (arg_n)
        elif mss == 'jpg' or mss == 'bmp':
            name = 'C:\Users\Coordinator\Desktop\S\Database\Pictures\%s' % (arg_n)
        elif mss == 'txt' or mss == 'py' or mss == 'c':
            name = 'C:\Users\Coordinator\Desktop\S\Database\Files\%s' % (arg_n)
        else:
            name = 'C:\Users\Coordinator\Desktop\S\Database\Files\%s' % (arg_n)
        
        print 'Peer openning file : %s' % (arg_n)
        
        try:
            f1 = open(name, nn)
            f1.seek(0, os.SEEK_END)
            size = f1.tell()
            print size
            connection.sendall(str(size))
            f1.seek(0, 0)
      
            i = 1
            sum_bytes = 0
            lines = f1.readlines()
            for line in lines:
                print 'Sending Line', i, ' with ', len(line), ' bytes. sum_bytes = ', sum_bytes
                #connection.sendall('CONTINUESENDING')
                connection.sendall(line)
                i = i+1
                sum_bytes = sum_bytes + len(line)
            print '------'
            print ' sum_bytes = ', sum_bytes
            #connection.sendall('PLZCEASESENDING')
            connection.sendall('^^DONE+DONE/DONE-DONE^^')
            f1.close()
            if(size == sum_bytes):
                #connection.sendall(('SERVER: Server sent file with ' + str(size) +  ' bytes'))
                print 'Peer sent file with ', sum_bytes/(1000*1000), ' Megabytes'
                return 1
            else:
                print 'ERROR'
                return 0
        except:
            print ' Except Error'
            return 0
        return 0

    
 
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
    
        cur_thread = threading.current_thread()  # identify current thread
        thread_name = cur_thread.name   # get thread-number in python     
    
        print '\nThread %s receives request' % thread_name
        a = 0
        print 'Received connection from ', self.client_address
        print 'Enter your Command:'
        try:        
            while True:
                a = server_logic(self.request, self.client_address)
                if a:
                    break            
        finally:        
            print '******************************************************'
            print 'Server  Thread %s terminating connection' % thread_name
            self.request.close()

def server_logic(connection, client_address):
    try:
        data = connection.recv(64)		
        if data == 'LISTR':
            connection.sendall('\nINCOMING: Received LIST-ALL command from client')
	    send_list_all(connection)
        elif data == 'GET':
            connection.sendall('\nINCOMING: Received GET command from client')			
            arg_name = connection.recv(128)
            ixi, ddrr, actual_n = check_file_name_exist(arg_name)
            if ixi == 0:
                connection.sendall('INCOMING: $ERROR$ File ' + arg_name + ' does not exist')
	    else:
                connection.sendall('INCOMING: Recieved File name ' + arg_name + ' to be transferred')
                xx = send_file(connection, arg_name)
                if xx == 1:
                    connection.sendall('INCOMING: File ' + arg_name + ' has been sent successfully')
                else:
                    connection.sendall('INCOMING: **ERROR**: File transfer unsuccessful, Try Again')
                    ##############################
        elif data == 'SEARCH':
            connection.sendall('\nINCOMING: Received SEARCH command from client')			
            arg_name = connection.recv(128)
            ixi, ddrr, actual_n = check_file_name_exist(arg_name)
            if ixi == 0:
                connection.sendall('INCOMING: File ' + arg_name + ' does not exist. Checking other peers')
	    else:
                connection.sendall('INCOMING: SUCCESS File name ' + arg_name + ' found')
                    ##############################
        elif data == 'DISCOVER':
            connection.sendall('\nINCOMING: Received DISCOVER command from client')			
            arg_TTL = connection.recv(64)
            connection.sendall('\nINCOMING: Received MAX_HOPS: ' + arg_TTL )
            connection.sendall(str(len(Peer_2_Peer.list_peers)))
            for n, p in Peer_2_Peer.list_peers:
                connection.sendall(str(len(n)))
                connection.sendall(str(n))
                connection.sendall(str(len(str((p)))))
                connection.sendall(str(p)) 
        elif data == 'BYE':
            print '\nINCOMING: Peer left: ', client_address
            iip, prt = client_address
            for n, s, p in Peer_2_Peer.list_connected_peers:
                if n == iip and p == prt:
                    Peer_2_Peer.list_connected_peers.remove(iip)
            
            return 1
    except:
        print ''
        print 'ERoRoRORoR. Something went wrong somewhere'
    return None

def send_file(connection, arg_n):
        iss = 0
        mss = ''
        nn = 'rb'
        
        for i in arg_n:
            if iss == 1:
                mss = mss + i
            if i == '.':
                iss = 1
            # Send a file over a socket
        if mss == 'mov' or mss == 'wmv':
            name = 'C:\Users\Coordinator\Desktop\S\Database\Vidoes\%s' % (arg_n)
        elif mss == 'wma' or mss == 'mp3' or mss == 'mp4':
            name = 'C:\Users\Coordinator\Desktop\S\Database\Music\%s' % (arg_n)
        elif mss == 'jpg' or mss == 'bmp':
            name = 'C:\Users\Coordinator\Desktop\S\Database\Pictures\%s' % (arg_n)
        elif mss == 'txt' or mss == 'py' or mss == 'c':
            name = 'C:\Users\Coordinator\Desktop\S\Database\Files\%s' % (arg_n)
        else:
            name = 'C:\Users\Coordinator\Desktop\S\Database\Files\%s' % (arg_n)
        
        print 'Peer openning file : %s' % (arg_n)
        
        try:
            f1 = open(name, nn)
            f1.seek(0, os.SEEK_END)
            size = f1.tell()
            print size
            connection.sendall(str(size))
            f1.seek(0, 0)
      
            i = 1
            sum_bytes = 0
            lines = f1.readlines()
            for line in lines:
                print 'Sending Line', i, ' with ', len(line), ' bytes. sum_bytes = ', sum_bytes
                #connection.sendall('CONTINUESENDING')
                connection.sendall(line)
                i = i+1
                sum_bytes = sum_bytes + len(line)
            print '------'
            print ' sum_bytes = ', sum_bytes
            #connection.sendall('PLZCEASESENDING')
            connection.sendall('^^DONE+DONE/DONE-DONE^^')
            f1.close()
            if(size == sum_bytes):
                #connection.sendall(('SERVER: Server sent file with ' + str(size) +  ' bytes'))
                print 'Peer sent file with ', sum_bytes/(1000*1000), ' Megabytes'
                return 1
            else:
                print 'ERROR'
                return 0
        except:
            print ' Except Error'
            return 0
        return 0

def send_list_all(connection):
    for f_1, f_2, f_3 in os.walk('C:\Users\Coordinator\Desktop\S\Database'):
        nm = print_name(f_1)

        element_length(connection, nm)
        connection.sendall(str(len(nm)))
        connection.sendall(nm)

        element_length(connection, f_2)
        connection.sendall(str(len(f_2)))
        if len(f_2) != 0:
            send_list(f_2, connection)

        element_length(connection, f_3)
        connection.sendall(str(len(f_3)))
        if len(f_3) != 0:
            send_list(f_3, connection)

    element_length(connection, 'DONE***DONE***DONE')
    connection.sendall('18')
    connection.sendall('DONE***DONE***DONE')
    return None

def check_file_name_exist(arg_n):
    f_dir = []
    drr = None
    actual_name = None
    for f_1, f_2, f_3 in os.walk('C:\Users\Coordinator\Desktop\S\Database'):
        if len(f_2) != 0:
            for d in f_2:
                f_dir.append(d)

    for dr in f_dir:   
        f_dir = 'C:\Users\Coordinator\Desktop\S\Database\%s' % (dr)
        f = os.listdir(f_dir)
        for fl in f:
            if arg_n == fl:
                drr = dr
                actual_name = fl
                return 1, drr, actual_name

    return 0, drr, actual_name

def element_length(connection, nm):
    if len(nm) > 9:
        connection.sendall('2')
    elif len(nm) > 99:
         connection.sendall('3')
    elif len(nm) > 999:
        connection.sendall('4')
    elif len(nm) > 9999:
        connection.sendall('5')
    else:
        connection.sendall('1')
    return None

def send_list(f, connection):     
    for i in f:
        element_length(connection, i)
        connection.sendall(str(len(i)))
        connection.sendall(i)
    return None

def print_name(f):
    f_dir = ''
    n = 1 
    for i in f:
        if n > (len('C:\Users\Coordinator\Desktop\S\Database')+ 1):
            f_dir = f_dir + i
            n = n + 1
	n = n + 1
    return f_dir
        
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def main():
    	
    #create an object of class
    P1 = Peer_2_Peer();

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print '------------------------------------------------------'
    print '----------------Welcome to the Underground------------'
    print '------------------------------------------------------'

    
    HOST = '127.0.0.1' #raw_input("Enter Host: ")
    PORT = 4000 #raw_input("Enter Port: ")
    letter = 'A' #raw_input("Enter Code: ")

    #sock.bind((HOST, PORT))


    peer = ThreadedTCPServer((HOST, int(PORT)), ThreadedTCPRequestHandler)
    ip, port = peer.server_address

    peer_thread = threading.Thread(target=peer.serve_forever)
    peer_thread.daemon = True
    peer_thread.start()    
	
    print ''
    print '------------------------------------------------------'
    print 'This is the Peer %s Terminal on PORT %s' % (letter,PORT)
    print 'You have to choose from one of the following commands:'
    print '------------------------------------------------------'
    print '1. LISTR <ip-address> <port-number>'
    print '2. LISTL'
    print '3. GET <file-name> <ip-address> <port-number>'
    print '4. DISCOVER <TTL>'
    print '5. SEARCH <file-name> <TTL> '
    print '6. RESET'
    print '7. QUIT'
    print '------------------------------------------------------'
    print ' ' # print a blank line

    i = 0
    arg_command = ''
    arg_1 = ''
    arg_2 = ''
    arg_3 = ''
	
    try:
                while True:
                    answer = raw_input("Enter Your command: ")
                    arg_command, arg_1, arg_2, arg_3 = P1.get_args(answer)
                    i = P1.client_logic(arg_command, arg_1, arg_2, arg_3, letter)
                    if i == 1:
                        break
		    print '         ***********************    '
    except:
                print 'Error. The System is down'
    finally:
                print 'Main Peer %s closing any connections to at ip-address %s port %s' % (letter,HOST, PORT)
                print 'Main Peer %s shutting down and terminating' % letter
                sock.close();
    print 'BYE BYE'
    peer.shutdown()

if __name__ == "__main__":
	main()
