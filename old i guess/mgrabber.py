"""
This code is made by dream4sy

This is a program, to get a minecraft skin from other users.

~ Made with <3, dream4sy
"""
# Imports
from skingrabber import skingrabber
from res.modules import phasto as ps
# Imports End

sg = skingrabber()


JSON = ps.file.read_json('res/config.json')
_logo = ps.file.read(JSON['logo'])
_version = JSON['version']
_skinoutput = JSON['skin_output']

ps.os.window.title(JSON['wintitle'])

# Functions for Methods
def grab_skin_rendered(output):
    user = input('\nUsername of Player:  ')
    link = sg.get_skin_rendered(user)
    uuid = sg.get_uuid(user)
    print('\nSkin found!\n(%s)\n\nOpen in Webbrowser? [y/n]' % uuid)
    yn = ps.os.one_input()

    if yn == b'y':
        ps.web.open(link)
    else:
        print('\nLink to skin:\n', link)

    print('\nDo you want to save skin as png? [y/n]')
    yn = ps.os.one_input()

    if yn == b'y':
        linknr = sg.get_skin(user)
        skinfile = ps.web.getcontent(linknr)
        ps.file.write_bytes(output + '/' + f'{user} ({uuid})' + '.png', skinfile)


    print('\nPress a key, to get to the menu')   
    ps.os.one_input()

def grab_skin(output):
    user = input('\nUsername of Player:  ')
    link = sg.get_skin(user)
    uuid = sg.get_uuid(user)
    print('\nSkin found!\n(%s)\n\nOpen in Webbrowser? [y/n]' % uuid)
    yn = ps.os.one_input()

    if yn == b'y':
        ps.web.open(link)
    else:
        print('\nLink to skin:\n', link)

    print('\nDo you want to save skin as png? [y/n]')
    yn = ps.os.one_input()

    if yn == b'y':
        skinfile = ps.web.getcontent(link)
        ps.file.write_bytes(output + '/' + f'{user} ({uuid})' + '.png', skinfile)


    print('\nPress a key, to get to the menu')   
    ps.os.one_input()

def grab_uuid():
    user = input('\nUsername of Player:  ')
    uuid = sg.get_uuid(user)
    print('\nUUID of %s:  %s' % (user, uuid))

    print('\nPress a key, to get to the menu')   
    ps.os.one_input()
# Functions of Methods End

while True:
    # Menu
    ps.os.clear()
    print(_logo)
    print(_version)
    ps.next_line(1)

    print('Methods:')
    print('<1> Grab Skin Rendered')
    print('<2> Grab Skin No Render')
    print('<3> Get UUID of Player')
    print('<4> Quit')

    getch = ps.os.one_input()


    if getch == b'1':
        grab_skin_rendered(_skinoutput)
    elif getch == b'2':
        grab_skin(_skinoutput)
    elif getch == b'3':
        grab_uuid()
    elif getch == b'4': break
    # Menu End