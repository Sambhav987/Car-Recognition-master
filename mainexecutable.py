import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2  
import threading

def create_ui():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.title("Traffic Management System")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    quad_width = screen_width // 2
    quad_height = screen_height // 2
    square_size = screen_width // 10

    x1 = (screen_width // 2) - (square_size // 2)
    y1 = 0
    x2 = x1 + square_size
    y2 = y1 + square_size

    gx1 = 0
    gy1 = (screen_height // 2) - (square_size // 2)
    gx2 = gx1 + square_size
    gy2 = gy1 + square_size

    bx1 = screen_width - square_size
    by1 = (screen_height // 2) - (square_size // 2)
    bx2 = screen_width
    by2 = by1 + square_size

    yx1 = (screen_width // 2) - (square_size // 2)
    yy1 = screen_height - square_size
    yx2 = yx1 + square_size
    yy2 = screen_height

    canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg='black')
    canvas.pack()

    canvas.create_rectangle(0, 0, quad_width, quad_height, fill='gray', outline='white', tags='quadrant')
    canvas.create_rectangle(quad_width, 0, screen_width, quad_height, fill='gray', outline='white', tags='quadrant')
    canvas.create_rectangle(0, quad_height, quad_width, screen_height, fill='gray', outline='white', tags='quadrant')
    canvas.create_rectangle(quad_width, quad_height, screen_width, screen_height, fill='gray', outline='white', tags='quadrant')

    red_square = canvas.create_rectangle(x1, y1, x2, y2, fill="red", tags=('square', 'red'))
    green_square = canvas.create_rectangle(gx1, gy1, gx2, gy2, fill="red", tags=('square', 'green'))
    blue_square = canvas.create_rectangle(bx1, by1, bx2, by2, fill="red", tags=('square', 'blue'))
    yellow_square = canvas.create_rectangle(yx1, yy1, yx2, yy2, fill="red", tags=('square', 'yellow'))

    exclamations = {}

    def create_exclamation_marks():
        red_center_x = (x1 + x2) // 2
        red_center_y = (y1 + y2) // 2
        green_center_x = (gx1 + gx2) // 2
        green_center_y = (gy1 + gy2) // 2
        blue_center_x = (bx1 + bx2) // 2
        blue_center_y = (by1 + by2) // 2
        yellow_center_x = (yx1 + yx2) // 2
        yellow_center_y = (yy1 + yy2) // 2
        exclamations['red'] = canvas.create_text(red_center_x, red_center_y, text='!', font=("Arial", 40), fill='yellow', tags=('exclamation', 'red'))
        exclamations['green'] = canvas.create_text(green_center_x, green_center_y, text='!', font=("Arial", 40), fill='yellow', tags=('exclamation', 'green'))
        exclamations['blue'] = canvas.create_text(blue_center_x, blue_center_y, text='!', font=("Arial", 40), fill='yellow', tags=('exclamation', 'blue'))
        exclamations['yellow'] = canvas.create_text(yellow_center_x, yellow_center_y, text='!', font=("Arial", 40), fill='yellow', tags=('exclamation', 'yellow'))

    create_exclamation_marks()

    canvas.tag_raise('square')
    for exclamation in exclamations.values():
        canvas.tag_raise(exclamation)

    blinking = False
    blink_state = True
    active_squares = []

    def blink():
        nonlocal blink_state
        if active_squares:
            state = 'normal' if blink_state else 'hidden'
            for square in active_squares:
                canvas.itemconfigure(exclamations[square], state=state)
            blink_state = not blink_state
            canvas.after(500, blink)
        else:
            for exclamation in exclamations.values():
                canvas.itemconfigure(exclamation, state='normal')

    def update_blinking():
        if active_squares:
            blink()
        else:
            for exclamation in exclamations.values():
                canvas.itemconfigure(exclamation, state='normal')

    def handle_key(event):
        key = event.keysym
        if key == 'Up':
            if 'red' not in active_squares:
                active_squares.append('red')
            else:
                active_squares.remove('red')
        elif key == 'Down':
            if 'yellow' not in active_squares:
                active_squares.append('yellow')
            else:
                active_squares.remove('yellow')
        elif key == 'Left':
            if 'green' not in active_squares:
                active_squares.append('green')
            else:
                active_squares.remove('green')
        elif key == 'Right':
            if 'blue' not in active_squares:
                active_squares.append('blue')
            else:
                active_squares.remove('blue')
        update_blinking()

    root.bind('<KeyPress>', handle_key)

    a = 1
    b = 1
    c = 1
    d = 1

    def create_traffic_light(x, y, state):
        light = canvas.create_rectangle(x - 30, y - 90, x + 30, y + 90, fill='black', outline='white', tags='traffic_light')
        red_light = canvas.create_oval(x - 20, y - 60, x + 20, y - 20, fill='black', outline='white', tags='traffic_light')
        yellow_light = canvas.create_oval(x - 20, y - 10, x + 20, y + 30, fill='black', outline='white', tags='traffic_light')
        green_light = canvas.create_oval(x - 20, y + 40, x + 20, y + 80, fill='black', outline='white', tags='traffic_light')
        if state == 1:
            canvas.itemconfig(red_light, fill='red')
        elif state == 2:
            canvas.itemconfig(yellow_light, fill='yellow')
        elif state == 3:
            canvas.itemconfig(green_light, fill='green')
        canvas.tag_raise('traffic_light')

    create_traffic_light(quad_width // 2, quad_height // 2, a)
    create_traffic_light(screen_width - (quad_width // 2), quad_height // 2, b)
    create_traffic_light(quad_width // 2, screen_height - (quad_height // 2), c)
    create_traffic_light(screen_width - (quad_width // 2), screen_height - (quad_height // 2), d)

    videos = {"TL": None, "TR": None, "BL": None, "BR": None}
    video_threads = {"TL": None, "TR": None, "BL": None, "BR": None}
    video_items = {"TL": None, "TR": None, "BL": None, "BR": None}
    stop_threads = {"TL": False, "TR": False, "BL": False, "BR": False}

    def open_file(section):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv")])
        if file_path:
            cap = cv2.VideoCapture(file_path)
            videos[section] = cap
            if video_items[section] is None:
                if section == "TL":
                    x = quad_width // 2
                    y = quad_height // 2
                elif section == "TR":
                    x = screen_width - (quad_width // 2) - 240
                    y = quad_height // 2
                elif section == "BL":
                    x = quad_width // 2
                    y = screen_height - (quad_height // 2)
                elif section == "BR":
                    x = screen_width - (quad_width // 2) - 240
                    y = screen_height - (quad_height // 2)
                video_items[section] = canvas.create_image(x, y, anchor='center', tags='video')
                thread = threading.Thread(target=play_video, args=(section,))
                thread.daemon = True
                video_threads[section] = thread
                thread.start()

    def play_video(section):
        cap = videos[section]
        while cap.isOpened() and not stop_threads[section]:
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (quad_width, quad_height))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                def update_frame():
                    if video_items[section]:
                        canvas.itemconfig(video_items[section], image=imgtk)
                        canvas.image_dict[section] = imgtk   
                        canvas.tag_raise('traffic_light')
                        canvas.tag_raise('square')
                        for exclamation in exclamations.values():
                            canvas.tag_raise(exclamation)
                root.after(0, update_frame)
            else:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        cap.release()

    def remove_video(section):
        if videos[section]:
            stop_threads[section] = True
            videos[section].release()
            videos[section] = None
            if video_items[section]:
                canvas.delete(video_items[section])
                video_items[section] = None
                stop_threads[section] = False

    canvas.image_dict = {}

    button_tl = tk.Button(root, text="Pick Video for TL", command=lambda: open_file("TL"), font=("Arial", 20), fg='white', bg='blue')
    button_tl.place(x=20, y=20)

    button_tr = tk.Button(root, text="Pick Video for TR", command=lambda: open_file("TR"), font=("Arial", 20), fg='white', bg='blue')
    button_tr.place(x=screen_width - 280, y=20)

    button_bl = tk.Button(root, text="Pick Video for BL", command=lambda: open_file("BL"), font=("Arial", 20), fg='white', bg='blue')
    button_bl.place(x=20, y=screen_height - 80)

    button_br = tk.Button(root, text="Pick Video for BR", command=lambda: open_file("BR"), font=("Arial", 20), fg='white', bg='blue')
    button_br.place(x=screen_width - 280, y=screen_height - 80)

    button_remove_tl = tk.Button(root, text="Remove Video for TL", command=lambda: remove_video("TL"), font=("Arial", 20), fg='white', bg='orange')
    button_remove_tl.place(x=20, y=80)

    button_remove_tr = tk.Button(root, text="Remove Video for TR", command=lambda: remove_video("TR"), font=("Arial", 20), fg='white', bg='orange')
    button_remove_tr.place(x=screen_width - 280, y=80)

    button_remove_bl = tk.Button(root, text="Remove Video for BL", command=lambda: remove_video("BL"), font=("Arial", 20), fg='white', bg='orange')
    button_remove_bl.place(x=20, y=screen_height - 160)

    button_remove_br = tk.Button(root, text="Remove Video for BR", command=lambda: remove_video("BR"), font=("Arial", 20), fg='white', bg='orange')
    button_remove_br.place(x=screen_width - 280, y=screen_height - 160)

    def start_function():
        pass

    start_button = tk.Button(root, text="Start", command=start_function, font=("Arial", 24), fg='white', bg='green')
    start_button.place(relx=0.5, rely=0.5, anchor='center')

    buttons = [button_tl, button_tr, button_bl, button_br,
               button_remove_tl, button_remove_tr, button_remove_bl, button_remove_br,
               start_button]

    for button in buttons:
        button.lift()

    root.mainloop()

create_ui()