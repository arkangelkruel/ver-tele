#!/usr/bin/python
from gi.repository import Gtk
from subprocess import Popen
import xml.etree.ElementTree as ET
tree = ET.parse('channelList.xml')
root = tree.getroot()


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Orientation.VERTICAL
        Gtk.Window.__init__(self, title="Canales")
        self.set_border_width(10)
        self.set_default_size(200, 200)
        box = Gtk.Box(spacing=6)
        box.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(box)

        for channel in root.findall('channel'):
            button = Gtk.Button(label=channel.get('title'))
            button.instance = channel.get('instance')
            button.connect("clicked", self.on_button_clicked)
            box.pack_start(button, True, True, 0)

    def on_button_clicked(ventana, widget):
        findelement = root.find('channel[@instance="'+widget.instance+'"]')
        if findelement is None:
            print "Channel not found"
        else:
            pageUrl = findelement.find('pageUrl').text
            swfUrl = findelement.find('swfUrl').text
            rtmp = findelement.find('rtmp').text
            playpath = findelement.find('playpath').text
            videoTitle = findelement.get('title')

            try:
                Popen(
                    "rtmpdump"
                    + ' --pageUrl "' + pageUrl + '"'
                    + ' --swfUrl "' + swfUrl + '"'
                    + ' --rtmp "' + rtmp + '"'
                    + ' --playpath "' + playpath + '"'
                    + ' --live --flv - | cvlc --video-title="'+videoTitle+'" -',
                    shell=True)
            except OSError as e:
                print >> "Execution failed:", e

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
