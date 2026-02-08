import cv2 as cv
import numpy as np
import mss
import time
import win32api
import math

# ================== AYARLAR ==================

TEMPLATES = [
    "nameplate1.jpg",
    "nameplate2.jpg"
]
THRESHOLD = 0.65
Y_OFFSET = 50
X_OFFSET = 0
WAIT_DURATION = 10
LOCK_MOVE_INTERVAL = 0.03
IGNORE_TOP_RATIO = 0.10  

LOCK_RADIUS = 60
LOCK_GRACE_TIME = 0
LOST_FRAME_THRESHOLD = 5

Y_DEADZONE = 8
SMOOTH_ALPHA = 0.35

# ================== STATE ==================
LOCKED_ON_TARGET = 0
WAIT_TOP = 1
WAIT_BOTTOM = 2

state = WAIT_TOP
state_since = time.time()
last_lock_move = 0.0

locked_target = None
lock_time = 0.0
lost_frames = 0

# ================== YARDIMCI ==================
def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def smooth_update(old, new):
    return (
        int(old[0] + (new[0] - old[0]) * SMOOTH_ALPHA),
        int(old[1] + (new[1] - old[1]) * SMOOTH_ALPHA),
    )

# ================== MAIN ==================
def main():
    global state, state_since, last_lock_move
    global locked_target, lock_time, lost_frames

    templates = []
    for path in TEMPLATES:
        img = cv.imread(path, cv.IMREAD_GRAYSCALE)
        if img is None:
            print("❌ TEMPLATE BULUNAMADI:", path)
            return
        templates.append((path, img))

    with mss.mss() as sct:
        monitor = sct.monitors[1]

        screen_center_x = monitor["left"] + monitor["width"] // 2
        screen_top_y = monitor["top"] + int(monitor["height"] * 0.30)
        screen_bottom_y = monitor["top"] + int(monitor["height"] * 0.70)

        while True:
            frame = np.array(sct.grab(monitor))
            frame = cv.cvtColor(frame, cv.COLOR_BGRA2BGR)
            debug = frame.copy()
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            h, w = gray.shape[:2]
            ignore_top_px = int(h * IGNORE_TOP_RATIO)

            gray_roi = gray[ignore_top_px:, :]
            debug_roi = debug[ignore_top_px:, :]
            now = time.time()

            targets = []

            # -------- TÜM TEMPLATE'LER --------
            for name, tpl in templates:
                h, w = tpl.shape[:2]
                res = cv.matchTemplate(gray_roi, tpl, cv.TM_CCOEFF_NORMED)
                ys, xs = np.where(res >= THRESHOLD)

                for (x, y) in zip(xs, ys):
                    cx = x + w // 2 + X_OFFSET
                    cy = y + ignore_top_px + h // 2 + Y_OFFSET
                    targets.append((cx, cy))

                    cv.rectangle(debug, (x, y), (x+w, y+h), (0,255,0), 2)

            # ================= METİN VAR =================
            if targets:
                if locked_target:
                    if now - lock_time >= LOCK_GRACE_TIME:
                        still_there = False
                        for t in targets:
                            if distance(t, locked_target) <= LOCK_RADIUS:
                                new_x, new_y = t

                                if new_y < locked_target[1]:
                                    new_y = locked_target[1]

                                if abs(new_y - locked_target[1]) > Y_DEADZONE:
                                    locked_target = smooth_update(
                                        locked_target,
                                        (new_x, new_y)
                                    )

                                lost_frames = 0
                                still_there = True
                                break

                        if not still_there:
                            lost_frames += 1
                            if lost_frames >= LOST_FRAME_THRESHOLD:
                                locked_target = None
                                lost_frames = 0

                if locked_target is None:
                    center = (screen_center_x, (screen_top_y + screen_bottom_y)//2)
                    locked_target = min(targets, key=lambda p: distance(p, center))
                    lock_time = now
                    state = LOCKED_ON_TARGET


                if now - last_lock_move >= LOCK_MOVE_INTERVAL:
                    win32api.SetCursorPos(locked_target)
                    last_lock_move = now

                cv.circle(debug, locked_target, 6, (0,0,255), -1)

            # ================= METİN YOK =================
            else:
                locked_target = None
                lost_frames = 0

                if state == LOCKED_ON_TARGET:
                    state = WAIT_TOP
                    state_since = now
                    win32api.SetCursorPos((screen_center_x, screen_top_y))

                elif state == WAIT_TOP:
                    if now - state_since >= WAIT_DURATION:
                        state = WAIT_BOTTOM
                        state_since = now
                        win32api.SetCursorPos((screen_center_x, screen_bottom_y))

                elif state == WAIT_BOTTOM:
                    if now - state_since >= WAIT_DURATION:
                        state = WAIT_TOP
                        state_since = now
                        win32api.SetCursorPos((screen_center_x, screen_top_y))

            cv.imshow("DEBUG", debug)
            if cv.waitKey(1) == 27:
                break

    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
