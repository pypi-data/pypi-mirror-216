import busio, board

dht, ads, mhz = 0, 0, 0
try:
    from Adafruit_DHT import DHT22, DHT11, read
except:
    dht = 1
    print("DHT not available, library 'Adafruit-DHT' not installed")
try:
    from adafruit_ads1x15 import analog_in, ads1015
except:
    ads = 1
    print("ADS not available, library 'adafruit_ads1x15' not installed")
try:
    from mh_z19 import read_from_pwm, read as mhz_read
except:
    mhz = 1
    print("MHZ19 not available, library 'mh_z19' not installed")


class Sensors:
    def __init__(self, loging_error=True):
        global ads
        self.loging_error = loging_error
        self.cache = {"humidity": 0.0, "temperature": 0.0, "chanels": [-0, -0, -0, -0], "co2": 0}

        try:
            self.ads = ads1015.ADS1015(busio.I2C(board.SCL, board.SDA))
            self.ads_chanels = [
                analog_in.AnalogIn(self.ads, 0),
                analog_in.AnalogIn(self.ads, 1),
                analog_in.AnalogIn(self.ads, 2),
                analog_in.AnalogIn(self.ads, 3)
            ]
        except Exception as ex:
            ads = 1
            if self.loging_error:
                print(f"ADS init error -> {ex}")

    def get_dht(self, _type=22, pin=4):
        if dht:
            if self.loging_error:
                print("DHT not available")
            return {"humidity": self.cache["humidity"], "temperature": self.cache["temperature"]}
        try:
            h, t = read(DHT22 if _type==22 else DHT11, pin)
            if h and t:
                self.cache["humidity"], self.cache["temperature"] = round(h, 2), round(t, 2)
            else:
                if self.loging_error:
                    print(f"DHT error, used cache")
        except Exception as ex:
            if self.loging_error:
                print(f"DHT error ({ex}), used cache")
        return {"humidity": self.cache["humidity"], "temperature": self.cache["temperature"]}

    def get_ads(self, chanel, interpolate=False, interpolate_min=0, interpolate_max=0):
        if ads:
            if self.loging_error:
                print("ADS not available")
            return 0.0
        if chanel > 3 or chanel < 0:
            if self.loging_error:
                print("The wrong channel is selected, only 0, 1, 2, 3 can be used\nUse chanel 0")
            chanel = 0
        try:
            self.cache["chanels"][chanel] = self.ads_chanels[chanel].voltage
        except Exception as ex:
            if self.loging_error:
                print(f"ADS error ({ex}), used cache")
        if interpolate:
            return round(interpolate_min+(interpolate_max-interpolate_min)*(self.cache["chanels"][chanel]/5),2)
        return self.cache["chanels"][chanel]

    def get_mhz(self, gpio=12, pwm=False, _range=5000):
        if mhz:
            if self.loging_error:
                print("MHZ19 not available")
            return self.cache["co2"]
        try:
            if pwm:
                self.cache["co2"] = read_from_pwm(gpio=gpio, range=_range)["co2"]
            else:
                self.cache["co2"] = mhz_read()["co2"]
        except Exception as ex:
            if self.loging_error:
                print(f"MHZ19 error ({ex}), used cache")
        return self.cache["co2"]