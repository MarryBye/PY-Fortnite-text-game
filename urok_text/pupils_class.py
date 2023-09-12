from second import *

txt_file = "second.txt"
main_class = Class("7-Б")

with open(txt_file, "r", encoding="utf-8") as file:
    for line in file.readlines():  # перебрати усі рядки файлу
        pupil_data = line.split(" ")  # Иванов О. 4 -> ["Иванов", "О.", "4"]
        new_pupil = Pupil(pupil_data[1], pupil_data[0], pupil_data[2])
        main_class.addPupil(new_pupil)

main_class.getClassInfo()
print(main_class.getAverageMark())

for pupil in main_class.getBestPupils():
    print(main_class.classname, "|", pupil.name, pupil.surname)
