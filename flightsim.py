import curses
import time

def main(stdscr):
    # Setup the screen
    curses.curs_set(0) # Hide the cursor
    stdscr.nodelay(1)  # Don't block waiting for user input
    stdscr.timeout(100) # Update every 100ms
    
    # Initial flight state
    alt = 1000
    speed = 250
    pitch = 0 # 0 is level, positive is up, negative is down
    running = True

    while running:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        # Input handling
        key = stdscr.getch()
        if key == curses.KEY_UP:
            pitch += 1
        elif key == curses.KEY_DOWN:
            pitch -= 1
        elif key == ord('q'):
            running = False

        # Physics (simplified)
        alt += pitch
        # If we pitch up, we lose speed; pitch down, we gain speed
        speed -= (pitch * 0.5) 
        
        # Boundary checks
        if alt <= 0:
            alt = 0
            speed = 0
            status = "CRASHED! Press 'q' to exit."
        else:
            status = "FLYING - Press 'q' to quit | Use Arrow Keys"

        # Visuals
        stdscr.addstr(1, 2, f"BYU OIT Flight Simulator", curses.A_BOLD)
        stdscr.addstr(3, 2, f"Altitude: {alt} ft")
        stdscr.addstr(4, 2, f"Airspeed: {speed:.1f} knots")
        stdscr.addstr(5, 2, f"Pitch:    {pitch} degrees")
        
        # Simple horizon line
        horizon_y = h // 2 + (pitch // 2)
        if 0 < horizon_y < h:
            stdscr.addstr(horizon_y, 0, "-" * (w - 1))
            stdscr.addstr(horizon_y, w // 2 - 5, "[ HORIZON ]")

        stdscr.addstr(h - 2, 2, status)
        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)