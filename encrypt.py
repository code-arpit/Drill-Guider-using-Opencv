import datetime 

with open('/etc/machine-id', 'r') as f:
    machine = f.read()

# print(f'Machine key -> {machine}')
encryption = {'0':'a',
        '1':'b',
        '2':'c',
        '3':'d',
        '4':'e',
        '5':'f',
        '6':'g',
        '7':'h',
        '8':'i',
        '9':'j',
        'a':'0',
        'b':'1',
        'c':'2',
        'd':'3',
        'e':'4',
        'f':'5',
        'g':'6',
        'h':'7',
        'i':'8',
        'j':'9'
    }

def encrypt(machine):
    #time
    now = datetime.datetime.now()
    time = now.strftime('%H%M')
    time = list(time)
    # print(f'time -> {time}')


    #date 
    date = datetime.date.today()
    date = str(date)
    date = date.split('-')
    date = ''.join(date)
    date = list(date)
    # print(f'date -> {date}')
    
    #machine code
    m = list(machine)
    m.pop(-1)
    # print(m)
    m = date + m + time
    # print(m)
    
    E = []
    for i in m:
        E.append(encryption[i])
    # print(E)
    E = ''.join(E)
    # print(E)
    return E

def decrypt(machine):
    D = []
    m = list(machine)
    # print(m)
    for i in m:
        D.append(encryption[i])
    # print(D)
    D = ''.join(D)
    date = (D[0:4]+'/'+D[4:6]+'/'+D[6:8])
    # print(date)
    time = (D[-4:-2]+'/'+D[-2:])
    # print(time)
    id = D[8:40]
    # print(id)
    # print(D)
    return [date, time, id]

encrypted_key = encrypt(machine)
decrypted_key = decrypt(encrypted_key)

print(f'Encrypted machine key -> {encrypted_key}')
print(f'Decrypted machine key -> {decrypted_key}')
