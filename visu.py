def display(window):
    curses.curs_set(False)
    curses.start_color()
    if curses.LINES < 25 or curses.COLS < 70:
		curses.endwin()
		print "Window is too small."
		exit(0)
    time.sleep(10)

curses.wrapper(display)
