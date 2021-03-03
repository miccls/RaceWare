# Klass för temperaturmätningar.
# RPI kan inte läsa adc. Dock kan man lösa detta med en kondensatorurladdning.
# Ladda upp den och låt sedan ladda ur genom ntc, när pinnen som ligger över kondingen inte längre
# är hög, då är spänningen 1.65V (tror) Då kan man beräkna resistansen! :D
import gpiozero
import math
class Thermometer:
    def __init__(self):
        self.BETA = 3950
        # Kelvin vid noll grader
        self.KELVIN_ADJ = 273.15
        # Dictionary med alla resistansvärden.

    def get_r(self,t):
        return 10000 * math.exp(self.BETA * ((1/(t + self.KELVIN_ADJ))-(1/(25 + self.KELVIN_ADJ))))

    def get_t(self,r):
        return 1/( (math.log(r/10000)/self.BETA) + (1/(25 + self.KELVIN_ADJ))) - self.KELVIN_ADJ
    
    
temp1 = Thermometer()

