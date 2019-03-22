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

def event_loop(stdscr):
    while 1:
        stdscr.nodelay(0)
        c = stdscr.getch()
        if c == ord('p'):
                outline = execmd("./merge.sh x")
        elif c == ord('c'):
                stdscr.erase()
        elif c == ord('q'):
                break  # Exit the while()

def exitScreen(mainwin):
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
        self.screen.addstr(y, x, str, curses.color_pair(colorpair))
        self.screen.refresh()

    def Border(self):
        self.screen.border()
        self.screen.refresh()

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
        self.Display(3, index+1, str(Item[0]))

    def SetCurrentItem(self, index):
        self.currentIndex = index
        self.Display(1, index+1, '->')

if __name__=='__main__':
    try:
#        desktop = initScreen()
        win = WidgetBase()
        win.Display(30,1,'Svn Tool Box V1.0',1)
        win.Border()

        menuWin = MenuList(win, 1, 3, 15, 30)
        menuWin.AppendItem(["1.更新"])
        menuWin.AppendItem(["2.合并"])
        menuWin.AppendItem(["3.提交"])
        menuWin.AppendItem(["4.浏览"])
        menuWin.SetCurrentItem(4)

        mainWin = WidgetBase(win, 17, 3, 100, 30)
        mainWin.Border()
        mainWin.Display(1,2, execmd("cat merge.sh")[2])
#        testWin = WidgetBase(mainWin, 2, 2, 80, 4)
#        testWin.Border()
#        testWin.Display(3,1, execmd("ls -l")[2])


#        get_ch_and_continue(win.screen)
        event_loop(win.screen)
    except Exception,e:
        raise e
    finally:
#        testWin.Display(3,2, execmd("ls -l")[3])
        exitScreen(win.screen)

