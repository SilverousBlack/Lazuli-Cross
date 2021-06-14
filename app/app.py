from gui import root

while True and root.winfo_ismapped():
    try:
        root.mainloop()
        break
    except Exception as e:
        print("A runtime error occured: {}".format(str(e)))
        root.destroy()
