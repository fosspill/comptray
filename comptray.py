#! /usr/bin/python2

import sys
import os
import os.path
import gtk
import gobject
from subprocess import CalledProcessError, check_output, call

pygtklibdir = os.path.join("/usr/lib", "pygtk", "2.0")
sys.path.insert(0, pygtklibdir)
# found on <http://files.majorsilence.com/rubbish/pygtk-book/pygtk-notebook-html/pygtk-notebook-latest.html#SECTION00430000000000000000>
# simple example of a tray icon application using PyGTK
 
def message(data=None):
  "Function to display messages to the user."
  msg=gtk.MessageDialog(None, gtk.DIALOG_MODAL,
    gtk.MESSAGE_INFO, gtk.BUTTONS_OK, data)
  msg.run()
  msg.destroy()
 
def close_app(data=None):
  gtk.main_quit()
 
def make_menu(event_button, event_time, data=None):
  menu = gtk.Menu()
  if airplanemode():
    toggle_item = gtk.MenuItem("Turn off airplane mode")
  else:
    toggle_item = gtk.MenuItem("Turn on airplane mode")
  open_item = gtk.MenuItem("About")
  close_item = gtk.MenuItem("Quit")
  
  #Append the menu items
  menu.append(toggle_item)
  menu.append(open_item)
  menu.append(close_item)
  #add callbacks
  toggle_item.connect_object("activate", toggleairplanemode, "Toggle")
  open_item.connect_object("activate", show_about_dialog, "About")
  close_item.connect_object("activate", close_app, "Quit")
  #Show the menu items
  toggle_item.show()
  open_item.show()
  close_item.show()
  
  #Popup the menu
  menu.popup(None, None, None, event_button, event_time)
  
def show_about_dialog(data=None):
    about_dialog = gtk.AboutDialog()
    about_dialog.set_destroy_with_parent (True)
    about_dialog.set_icon_name ("Pyplanemode")
    about_dialog.set_name('Pyplanemode')
    about_dialog.set_version('0.4')
    about_dialog.set_copyright("Copyleft 2015 Ole Erik Brennhagen")
    about_dialog.set_comments(("Fancy airplane mode applet"))
    about_dialog.set_authors(['Ole Erik Brennhagen <oleerik@startmail.com>', 'Ivanka Heins'])
    about_dialog.run()
    about_dialog.destroy()
 
def on_right_click(data, event_button, event_time):
  make_menu(event_button, event_time)
 
def on_left_click(event):
  toggleairplanemode()
  
def airplanemode():
    "This returns true or false depending on airplane mode status"
    try:
        output = check_output(["rfkill", "list"])
    except CalledProcessError as e:
        output=(e.returncode)

    if "yes" not in output:
        curstatus=False
    else:
        curstatus=True
    return curstatus

def toggleairplanemode(data=None):
    if airplanemode():
        call(["gksudo", "rfkill unblock all"])
    else:
        call(["gksudo", "rfkill block all"])
        
def check_for_update():		
    if airplanemode():
        iconname="plane-on"
    else:
        iconname="plane-off"
    return iconname

def update_icon():
    tray.set_from_icon_name(check_for_update())
    return True

#Continuesly check for status update
gobject.timeout_add(100, update_icon)

 
if __name__ == '__main__':
  tray = gtk.StatusIcon()
  tray.set_from_icon_name(check_for_update())
  tray.set_tooltip(('Pyplanemode'))
  tray.connect('popup-menu', on_right_click)
  tray.connect('activate', on_left_click)
  gtk.main()
