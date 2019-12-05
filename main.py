#!/usr/bin/python
#-*- coding: UTF-8 -*-
import curses
import locale
import subprocess

locale.setlocale(locale.LC_ALL, '')

def execmd(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = []
    for line in iter(p.stdout.readline, b''):
        line = line.strip('\n')
        lines.append(line)
    return lines

def event_loop(win, app):
    stdscr=win.screen
    while 1:
        stdscr.nodelay(0)
        c = stdscr.getch()
        if c == ord('p'):
            outline = execmd("./merge.sh x")
        elif c == ord('j'):
            app.setNextMenu()
        elif c == ord('k'):
            app.setPrevMenu()
        elif c == ord('h'):
            stdscr.erase()
        elif c == ord('l'):
            mySvnBox.setWorkSpace()
        elif c == ord('q'):
            break  # Exit the while()

def exitScreen(win):
    mainwin=win.screen
    '''控制台重置'''
    #恢复控制台默认设置（若不恢复，会导致即使程序结束退出了，控制台仍然是没有回显的）
    curses.nocbreak()
    mainwin.keypad(0)
    curses.echo()
    #结束窗口
    curses.endwin()

class WidgetBase:
    def __init__(self, parent=0, x=0, y=0, w=0, h=0):
        if 0 == parent:
            self.screen = curses.initscr()
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_GREEN, -1)
            #关闭屏幕回显
            curses.noecho()
            #输入时不需要回车确认
            curses.cbreak()
            self.screen.keypad(1)
        else:
            self.screen = parent.screen.derwin(h, w, y, x)
            self.parent = parent

    def Display(self, x, y, str, colorpair = 1):
        self.screen.addnstr(y, x, str, 20, curses.color_pair(colorpair))
        self.screen.addstr(y+10, x, str[0:5], curses.color_pair(colorpair))
        self.screen.refresh()

    def Border(self):
        self.screen.border('|','|','-','-','|','|','|','|')
        self.screen.refresh()

    def Clear(self):
        self.screen.clear()
        self.Border()

class MenuList(WidgetBase):
    def __init__(self, parent=0, x=0, y=0, w=0, h=0):
        if 0 == parent:
            pass
        else:
            self.screen = parent.screen.derwin(h, w, y, x)
            self.parent = parent
            self.items = []
            self.Border()

    def AppendItem(self, Item):
        self.items.append(Item)
        index = len(self.items)
        self.Display(3, index+1, Item)

    def SetCurrentItem(self, index):
        self.currentIndex = index
        for i in range(0, len(self.items)):
            if i+1 == index:
                self.Display(1, i+2, '->')
            else:
                self.Display(1, i+2, '  ')

class SVNBox:
    def __init__(self, parent=0, x=0, y=0, w=50, h=30):
        self.window = WidgetBase(parent)
        self.window.Border()

        self.sidebar = MenuList(self.window, 1, 2, 16, h)

        self.workspace = WidgetBase(self.window, 17, 2, w-17, h)
        self.workspace.Border()

    def setBoxTital(self, tital):
        self.window.Display(30,1,tital,1)

    def setMenuList(self, itemlist):
        for number in range(0, len(itemlist)):
            self.sidebar.AppendItem(`number+1`+'.'+itemlist[number])
        self.sidebar.SetCurrentItem(1)

    def setNextMenu(self):
        self.sidebar.SetCurrentItem(self.sidebar.currentIndex % len(self.sidebar.items)+1)

    def setPrevMenu(self):
        self.sidebar.SetCurrentItem((self.sidebar.currentIndex + len(self.sidebar.items)-2) % len(self.sidebar.items)+1)

    def setWorkSpace(self):
        menu = self.sidebar.currentIndex
        if 1 == menu:
            lines = execmd("./merge.sh x")
        elif 2 == menu:
            lines = execmd("./merge.sh g")
        elif 3 == menu:
            lines = execmd("./merge.sh h")
        elif 4 == menu:
            lines = execmd("./merge.sh s")
        else:
            lines = ['']
        self.workspace.Clear()
        for i in range(len(lines)):
            self.workspace.Display(1,i+1, lines[i])

if __name__=='__main__':
    try:
        myScreen = WidgetBase()
        x,y=myScreen.screen.getmaxyx()
        mySvnBox = SVNBox(myScreen, 0, 0, y-1, x-3)
        mySvnBox.setBoxTital("Svn Tool Box V1.0")
        mySvnBox.setMenuList(['更新', '合并', '提交', '浏览'])

        event_loop(myScreen, mySvnBox)
    except Exception,e:
        raise e
    finally:
        exitScreen(myScreen)

