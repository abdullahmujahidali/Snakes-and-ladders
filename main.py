from collections import namedtuple
import datetime

Reservation = namedtuple('Reservation','room arr_date dept_date guest_name confirmation_num')

#----------global variables / lists----------#

confirmation_counter = 0
bedroom_list = []
reservation_list = []

#main function
def Anteater_BandB (file_name:str)-> None:
    '''main function. reads a file named file_name'''
    infile = open(file_name, 'r')
    data = infile.readlines()
    infile.close()
    for line in data:
        line = line.strip()
        line_reader(line)

def line_reader(l: str) -> None:
    '''takes in one line of input and calls appropriate functions'''
    command = l[:2].upper()
    rest_of_input = l[2:].strip()
    if command == '**':
        pass;
    elif command == 'AB':
        add_bedroom(rest_of_input)
    elif command == 'BL':
        display_bedroom_list()
    elif command == 'PL':
        print_line(rest_of_input)
    elif command == 'BD':
        delete_bedroom(rest_of_input)
    elif command == 'NR':
        new_reservation(rest_of_input)
    elif command == 'RL':
        display_reservation_list()
    elif command == 'RD':
        delete_reservation(rest_of_input)
    elif command == 'RB':
        reservations_by_bedroom(rest_of_input)
    elif command == 'RC':
        reservations_by_guest(rest_of_input)
    elif command == 'LA':
        list_arrivals(rest_of_input)
    elif command == 'LD':
        list_departures(rest_of_input)
    elif command =='LF': 
        list_free_beds(rest_of_input)       
    elif command == 'LO': 
        list_occupied(rest_of_input)

def dashes():
    return '------------------------------------'

#AB

def add_bedroom(room: str)-> None:
    '''takes in a room number as a string and puts it into bedroom_list'''
    global bedroom_list
    if room in bedroom_list:
        print('The bedroom is already in the list.')
    else:
        bedroom_list.append(room)

#BL

def display_bedroom_list():
    '''prints items in bedroom_list'''
    global bedroom_list
    print('Number of bedrooms in service:\t', len(bedroom_list))
    print(dashes())
    for bed in bedroom_list:
        print(bed)

#PL

def print_line(r: str):
    print(r)

#BD

def delete_bedroom(room:str)-> None:
    '''deletes specified room from the list. print error message if
    room isn't on the list'''
    global bedroom_list
    if room in bedroom_list:
        bedroom_list.remove(room)
        cancel_room_reservations(room)
    else:
        print('Sorry, can\'t delete room '+room+'; it is not in service now')


def compare_date(date1:str,date2:str)->bool:
    '''compares two dates. returns true if date 2 is after date 1'''
    date1 = date1.split('/')
    date_1 = datetime.date(int(date1[2]),int(date1[0]),int(date1[1]))
    date2 = date2.split('/')
    date_2 = datetime.date(int(date2[2]),int(date2[0]),int(date2[1]))
    if date_2>date_1:
        return True
    else:
        return False

def date(date:str)->int:
    date = date.split('/')
    result = datetime.date(int(date[2]),int(date[0]),int(date[1]))
    return result

def conf_num(r: Reservation) -> int:
    return r.confirmation_num

#NR

def new_reservation(rest_input: str)->None:
    '''creates a new reservation namedtuple and adds it to reservation_list'''
    global reservation_list
    global bedroom_list
    global confirmation_counter
    #chop up input to get variables
    parts = rest_input.split()
    room_request = parts[0]
    arrival = parts[1]
    departure = parts[2]
    name = ''
    for item in parts[3:]:
        name+=item
        name+=' '
    if (room_request in bedroom_list) and (allow_reservation(arrival, departure)) and room_not_taken(room_request) :
        confirmation_counter+=1
        reservation = Reservation(room_request, arrival, departure, name, confirmation_counter)
        reservation_list.append(reservation)
        print('Reserving room '+room_request+' for '+name+' -- Confirmation # ' + str(confirmation_counter))
        print('(arriving ' + arrival + ', departing ' + departure + ' )')
    elif allow_reservation(arrival, departure) == False:
        print("Sorry, can't reserve room ",room_request,'(',arrival,' to ',departure,"); \n can't leave before you arrive.")
    elif room_not_taken(room_request)==False:
        print("Sorry, can't reserve room ",room_request,'(',arrival,' to ',departure,"); \n it is already booked (conf # ",str(confirmation_counter)) 
    else:
        print("Sorry, can't reserve room", room_request,'; room not in service')




#RL

def display_reservation_list():
    global reservation_list
    print('Number of reservations:\t' + str(len(reservation_list)))
    print('{:>3}{:>4}{:>11}{:>11}{}{}'.format('No.','Rm.','Arrive','Depart',' ','Guest'))
    print(dashes())
    for r in reservation_list:
        print('{:>3}{:>4}{:>11}{:>11}{}{}'.format(
            str(r.confirmation_num),r.room,r.arr_date,r.dept_date,' ',r.guest_name))

#RD
def delete_reservation(num: str):
    '''takes in a confirmation number and deletes the reservation with that confirmation number'''
    global reservation_list
    #reservation_list.sort(key = conf_num, reverse=False)
    confirmation_list = []
    for r in reservation_list:
        confirmation_list.append(r.confirmation_num)
    if (int(num) in confirmation_list):
        reservation_index = confirmation_list.index(int(num)) #find where the reservation is in the list
        reservation_list.remove(reservation_list[reservation_index]) #delete the reservation with that index
    else:
        print("Sorry, can't cancel reservation; no confirmation number " + num)


#First: reject if arrival of guest A is later than departure date of guest A

def allow_reservation(arr: str, dept: str)-> bool:
    '''takes in two dates as strings, converts them to dates to compare them,
    and determines whether, based on the arr and dept date, the reservation is valid
    '''
    if date(arr)>=date(dept):
        #print('can\'t leave before you arrive')
        return False
    return True

#Second: check conflicts with existing reservations

def room_not_taken(room_req: str) -> bool:
    '''return true if room is taken'''

    #based on whether bedroom is free
    global reservation_list
    reserved_rooms = []
    for r in reservation_list:
        reserved_rooms.append(r.room) #list of strings of taken rooms
    if (room_req not in reserved_rooms):
        return True
    return False

def reservations_conflict(r1:Reservation, r2:Reservation)-> bool:
    '''takes two reservations and compares them. return true if they conflict'''
    if (date(r1.arr_date)>=date(r2.arr_date) and date(r1.arr_date)<date(r2.dept_date)) or (date(r1.dept_date)>=date(r2.arr_date) and date(r1.dept_date)<date(r2.dept_date)):
            print('Sorry, can\'t reserve room '+room_request+'\t('+arrival+' to '+departure+');')
            print('it\'s already been booked')
            return True
    return False

#Finally, if user deletes bedroom, all reservations for that room are cancelled
def cancel_room_reservations(room:str):
    for r in reservation_list:
        if r.room == room:
            print('Deleting room',room,'forces cancellation of this reservation:')
            print('\t',r.guest_name,'arriving',r.arr_date,'and departing',r.dept_date,'(Conf. #',r.confirmation_num,')')
            delete_reservation(r.confirmation_num)


#RB
def reservations_by_bedroom(line:str):
    global reservation_list
    bedroom_reserve_list= []
    bedroom_num = line
    for r in reservation_list:
        if r.room == bedroom_num:
            bedroom_reserve_list.append(r)
    print("Reservations for room " + line +':')
    for re in bedroom_reserve_list:
        print(re.arr_date,' to ',re.dept_date, re.guest_name)
#RC
def reservations_by_guest(line:str):
    guest_reserve_list = []
    guest_name = line
    print('Reservation for',guest_name)
    for r in reservation_list:
        if r.guest_name == guest_name:
            print(r.arr_date + ' to ' + r.dept_date + ': room ' + r.room)

def display_guest(rl:list) -> None:
    '''takes in a reservation list and prints out guest name as well as room number
    '''
    for r in rl:
        print(r.guest_name+ '(room '+ r.room + ')')

def reserved_rooms(rl: list) -> list:
    '''takes in a list of reservations and returns a list of reserved rooms''' 
    reserved = []
    for r in rl:
        reserved.append(str(r.room))
    return reserved

#LA
def list_arrivals(line:str):
    guest_arrival_list = []
    guest_arrival = date(line)
    for r in reservation_list:
        if guest_arrival == date(r.arr_date):
            guest_arrival_list.append(r)
    print('Guests arriving on '+ line+ ':')
    display_guest(guest_arrival_list)

#LD
def list_departures(line:str):
    guest_departure_list = []
    guest_departure = date(line)
    for r in reservation_list:
        if guest_departure == date(r.dept_date):
            guest_departure_list.append(r)
    print('Guests departing on '+ line+ ':')
    display_guest(guest_departure_list)

#LF
def list_free_beds(line:str):
    global bedroom_list
    bedroom_requests = []
    two_dates = line.split()
    arr_date = two_dates[0]
    dept_date = two_dates[1]
    print('Bedrooms free between ' + arr_date + ' to ' + dept_date + ':')
    for r in reservation_list:
        if (date(dept_date)<=date(r.arr_date)) or (date(arr_date)>=date(r.dept_date)):
            bedroom_requests.append(str(r.room))
    for b in bedroom_list:
        if str(b) not in reserved_rooms(reservation_list):
            bedroom_requests.append(str(b))
    bedroom_requests = list(set(bedroom_requests))
    for beds in bedroom_requests:
        print(beds)

#LO
def list_occupied(line:str):
    global bedroom_list
    bedroom_requests = []
    two_dates = line[2:].split()
    arr_date = two_dates[0]
    dept_date = two_dates[1]
    print('Bedrooms occupied between ' + arr_date + ' to ' + dept_date + ':')
    for r in reservation_list:
        if not (date(dept_date)<=date(r.arr_date)) or (date(arr_date)>=date(r.dept_date)):
            bedroom_requests.append(str(r.room))
    bedroom_requests = list(set(bedroom_requests))
    for beds in bedroom_requests:
        print(beds)