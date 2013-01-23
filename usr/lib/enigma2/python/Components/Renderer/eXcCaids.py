from Renderer import Renderer
from enigma import eCanvas, eRect, gFont
from skin import parseColor, parseFont

class eXcCaids(Renderer):
    GUI_WIDGET = eCanvas

    def __init__(self):
        Renderer.__init__(self)
        self.foregroundColor = parseColor('#ffffff')
        self.backgroundColor = parseColor('#171717')
        self.emmColor = parseColor('#f23d21')
        self.ecmColor = parseColor('#389416')
        self.font = gFont('Regular', 20)

    def pull_updates(self):
        if self.instance is None:
            return
        self.instance.clear(self.backgroundColor)
        caidlist = self.source.getCaidlist
        if caidlist is None:
            return
        self.draw(caidlist)

    def draw(self, caidlist):
        offset = 0
        pointSize = self.font.pointSize
        for key in caidlist:
            if caidlist[key][0]:
                length = len(caidlist[key][0]) * pointSize
                if caidlist[key][1] == 0:
                    bg = self.backgroundColor
                    self.instance.fillRect(eRect(offset + 1, 2, length - 3, pointSize + 1), bg)
                elif caidlist[key][1] == 1:
                    bg = self.emmColor
                    self.instance.fillRect(eRect(offset + 1, 2, length - 3, pointSize + 1), bg)
                else:
                    bg = self.ecmColor
                    self.instance.fillRect(eRect(offset + 1, 2, length - 3, pointSize + 1), bg)
                self.instance.writeText(eRect(offset, 0, length - 1, pointSize), self.foregroundColor, bg, self.font, caidlist[key][0], 2)
                offset = offset + length

    def changed(self, what):
        self.pull_updates()

    def applySkin(self, desktop, parent):
        attribs = []
        from enigma import eSize

        def parseSize(str):
            x, y = str.split(',')
            return eSize(int(x), int(y))

        for attrib, value in self.skinAttributes:
            if attrib == 'size':
                self.instance.setSize(parseSize(value))
                attribs.append((attrib, value))
            elif attrib == 'backgroundColor':
                self.backgroundColor = parseColor(value)
            elif attrib == 'emmColor':
                self.emmColor = parseColor(value)
            elif attrib == 'ecmColor':
                self.ecmColor = parseColor(value)
            elif attrib == 'font':
                self.font = parseFont(value, ((1, 1), (1, 1)))
            elif attrib == 'foregroundColor':
                self.foregroundColor = parseColor(value)
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)
