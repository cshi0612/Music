
import tkinter as tk
import os
import playsound


genreDic={}
music_folder="./Music"
for genre in os.listdir(music_folder):
    genreDic[genre]=os.listdir(music_folder+"/"+genre)
root1 = tk.Tk()
root1.geometry('800x400')
frame1 = tk.Frame(root1)

l1= tk.Label(frame1,text="Word Count:")
l1.grid(column=0,row=0,pady=10)

l2 = tk.Label(frame1,text= "Words Per Min:")
l2.grid(column=0,row=1,pady=10)

l3=tk.Label(frame1,text="# of Typos:")
l3.grid(column=10,row=0,pady=10)

l5=tk.Label(frame1,text="0")
l5.grid(column=1,row=0,pady=10,padx=5)

l6=tk.Label(frame1,text="0")
l6.grid(column=12,row=0,pady=10,padx=5)

l4=tk.Label(frame1,text="Efficiency:")
l4.grid(column=10,row=1,pady=10)

l7=tk.Label(frame1,text="0")
l7.grid(column=12,row=1,pady=10,padx=5)

l8=tk.Label(frame1,text="0")
l8.grid(column=1,row=1,pady=10,padx=5)

frame1.grid(column=0,row=0, padx=20, pady=20)

frame2 = tk.Frame(root1, bg='orange')
textBox=tk.Text(frame2,height=40, width= 40)
textBox.grid(row=0,column=0,padx=20,sticky="nesw")

frame2.grid(column=0,row=3, padx=20, pady=20)
frame3= tk.Frame(frame2)
counter = 0
for genre in genreDic:
    genre_label = tk.Label(frame3, text=genre)
    genre_label.grid(row=2 * counter, column=0)
    # Create a frame for the canvas with non-zero row&column weights
    frame_canvas = tk.Frame(frame3)
    frame_canvas.grid(row=2 * counter + 1, column=0)
    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)
    # Set grid_propagate to False to allow 5-by-5 buttons resizing later
    frame_canvas.grid_propagate(False)

    # Add a canvas in that frame
    canvas = tk.Canvas(frame_canvas, bg="yellow")
    canvas.grid(row=0, column=0, sticky="news")

    # Link a scrollbar to the canvas
    vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=vsb.set)

    # Create a frame to contain the buttons
    frame_buttons = tk.Frame(canvas, bg="blue")
    canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
    current_music=None
    # Add 9-by-5 buttons to the frame
    buttons = [tk.Button() for i in range(len(genreDic[genre]))]
    counter2 = 0
    for i in genreDic[genre]:
        def playMusic():
            global current_music
            if current_music!=i:
                current_music=i
                playsound.playsound(music_folder + "/" + genre + "/" + i,False)

            else:
                pass
        buttons[counter2] = tk.Button(frame_buttons, text=(f"{i}"),command=playMusic)
        buttons[counter2].grid(row=counter2, column=0, sticky='news')
        counter2 += 1

    # Update buttons frames idle tasks to let tkinter calculate buttons sizes
    frame_buttons.update_idletasks()

    n_rows_per_genre = 2
    column_width = buttons[0].winfo_width()
    first_n_rows_height = sum([buttons[i].winfo_height() for i in range(0, n_rows_per_genre)])
    frame_canvas.config(width=column_width + vsb.winfo_width(),
                        height=first_n_rows_height)

    # Set the canvas scrolling region
    canvas.config(scrollregion=canvas.bbox("all"))
    counter += 1
frame3.grid(row=0,column=1)
buttonPop=tk.Button(frame3, text="POP")


root1.mainloop()
