from gui import root

print("""Project Lazuli Cross
    Project Lazuli Cross: Personal Protective Equipment Detection and Safety Features Determination through YOLO Algorithm
    Copyright (C) 2021 Team Lazuli Cross

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.""")
while True and root.winfo_ismapped():
    try:
        root.mainloop()
        break
    except Exception as e:
        print("A runtime error occured: {}".format(str(e)))
        root.destroy()
exit()
