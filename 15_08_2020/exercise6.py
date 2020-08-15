"""
Historia de vida:


Joe conocio a Claudia
Tuvieron a Dany y a Leo


Joe aumento su felicidad en 30% cuando conocio a Claudia
Claudia aumento su felicidad en 40% cuando conocio a Joe
Joe crecio 2 años
Claudia crecio 2 años
Joe le dio flores a Claudia
Claudia le dio un lego star  wars a Joe
Claudia tuvo a Dany
Claudia tuvo a leo

Joe fue mordido por Dany, baja de felicidad 5%
Joe fue babeado ppor leo  , alta de felicidad 3%

Al final, que tan felices son todos sabiendo que las personas cuando nacen tienen una felicidiad de 50 puntos (no %)
"""

class Human:
    def __init__(self,name, years=0):
        self.happiness = 50
        self.years = years
        self.receivedGift = ""
        self.name = name
    def grow(self,y):
        self.years = self.years + y
    def haveChild(self, babyName):
        return Human(babyName)
    def meetSomeone(self,hp_perc):
        self.happiness = self.happiness*(1+hp_perc)
    def receiveGift(self,rg):
        self.receivedGift = rg
    def getBitten(self):
        self.happiness = self.happiness*(1-0.05)
    def getDrooled(self):
        self.happiness = self.happiness*(1-0.03)


joe = Human("Joe",years=27)
clau = Human("Claudia",years=27)
joe.grow(2)
clau.grow(2)
joe.meetSomeone(0.3,)
clau.meetSomeone(0.4)
joe.receiveGift("lego star wars")
clau.receiveGift("flores")
dany = clau.haveChild("Dany")
leo = clau.haveChild("Leo")

joe.getBitten()
joe.getDrooled()

print("Clau:" + str(clau.happiness))
print("Joe:" + str(joe.happiness))
