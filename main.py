#-*- coding: UTF-8 -*-
import curses
import locale

locale.setlocale(locale.LC_ALL, '')

stdscr = curses.initscr()

def get_ch_and_continue():
    '''''演示press any key to continue'''
    global stdscr
    #设置nodelay，为0时会变成阻塞式等待
    stdscr.nodelay(0)
    #输入一个字符
    ch=stdscr.getch()
    #重置nodelay,使得控制台可以以非阻塞的方式接受控制台输入，超时1秒
    stdscr.nodelay(1)
    return True

def unset_win():
    '''控制台重置'''
    global stdstr
    #恢复控制台默认设置（若不恢复，会导致即使程序结束退出了，控制台仍然是没有回显的）
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    #结束窗口
    curses.endwin()

class WidgetBase:
    def __init__(self, parent=0, x=0, y=0, w=0, h=0):
        if 0 == parent:
            self.screen = curses.initscr()
            #使用颜色首先需要调用这个方法
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_GREEN, -1)
            #关闭屏幕回显
            curses.noecho()
            #输入时不需要回车确认
            curses.cbreak()
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
        win = WidgetBase()
        win.Display(30,1,'Svn Tool Box V1.0',1)
        win.Border()

        menuWin = MenuList(win, 1, 3, 15, 30)
        menuWin.AppendItem(["1.更新"])
        menuWin.AppendItem(["2.合并"])
        menuWin.AppendItem(["3.提交"])
        menuWin.SetCurrentItem(1)

        mainWin = WidgetBase(win, 17, 3, 100, 30)
        mainWin.Border()
        testWin = WidgetBase(mainWin, 2, 2, 40, 4)
        testWin.Border()
        testWin.Display(3,2, str(testWin.screen.getbegyx()))
#        print(str(mainWin.screen.getmaxyx()[1]))


        get_ch_and_continue()
    except Exception,e:
        raise e
    finally:
        unset_win()

