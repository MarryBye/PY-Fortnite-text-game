class Class:
    def __init__(self, classname):
        self.classname = classname
        self.pupils = []

    def getClassInfo(self):
        for pupil in self.pupils:
            print(self.classname, "|", pupil.name,
                  pupil.surname, "| Оцінка:", pupil.mark)

    def getAverageMark(self):
        avg_mark = 0
        for pupil in self.pupils:
            avg_mark += pupil.mark
        avg_mark /= len(self.pupils)
        return avg_mark

    def getBestPupils(self):
        best_pupils = []
        for pupil in self.pupils:
            if pupil.mark == 5:
                best_pupils.append(pupil)
        return best_pupils

    def addPupil(self, pupil):
        self.pupils.append(pupil)


class Pupil(Class):
    def __init__(self, name, surname, mark):
        self.name = name
        self.surname = surname
        self.mark = int(mark)
