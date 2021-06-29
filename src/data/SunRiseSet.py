import math

class SunRiseSet:
    def __init__(self, year, month, day, place, date_type, local_offset):
        self.year = year
        self.month = month
        self.day = day
        self.latitude, self.longitude = place
        self.date_type = date_type
        self.local_offset = local_offset
        
        
        
        self.sun_longitude = 0
        
        
        
        if self.date_type != 'AD':
            # convert year month and day into AD
            pass

        # extract latitude and longitude form place

        # 1. calculate day of the year
        n1 = math.floor(275 * self.month / 9)
        n2 = math.floor((self.month + 9) / 12)
        n3 = (1 + math.floor((self.year - 4 * math.floor(self.year / 4) + 2) / 3))
        self.day_number = n1 - (n2 * n3) + self.day - 30
#         print(f'1. Day Number = {self.day_number}')
        

    def __calculate_time(self, n):
        # 2. convert to longitude hour and calculate approximate time
        longitude_hour = self.longitude / 15
        time = self.day_number + (n - longitude_hour) / 24
#         print(f'2. Approximate time: {time}')
        
        # 3. calculate sun's mean anomaly
        m = 0.9856 * time - 3.289
#         print(f'3. Sun\'s mean anomaly: {m}')
              
        
        # 4. calculate sun's true longitude
        M1 = math.radians(m)
        M2 = 2 * m
        M2 = math.radians(M2)
        l = m + 1.916 * math.sin(M1) + 0.020 * math.sin(M2) + 282.634
        l = l % 360
        
        self.sun_longitude = l
        
        
        
#         print(f"4. Sun's true latitude: {l}")
        
        # 5a. calculate sun's right ascension
        ra = math.atan(0.91764 * math.tan(math.radians(l)))
        ra = math.degrees(ra)
#         print(f"5a. RA before adjustment: {ra}")
        ra = ra % 360
#         print(f"5a. RA after adjustment: {ra}")

        # 5b.right ascension value needs to be in the same quadrant as l
        l_quadrant = (math.floor(l / 90)) * 90
        ra_quadrant = (math.floor(ra / 90)) * 90
        ra = ra + (l_quadrant - ra_quadrant)
#         print(f"5b. putting right ascension in same quadrant as l: {ra}")

        #5c. right ascension value needs to be converted into hours
        ra = ra / 15
#         print(f"5c. Right ascension value in hours: {ra}")

        # 6. calculate the Sun's declination
        sin_dec = 0.39782 * math.sin(math.radians(l))
        cos_dec = math.cos(math.asin(sin_dec))
#         print(f"6. Sun's Declination\n   SinDec: {sin_dec} \n   CosDec: {cos_dec}")

        # 7a. calculate the Sun's local hour angle
        zenith = 545 / 6 # this is a standard value it as always like this
        zenith = math.radians(zenith)
        latitude = math.radians(self.latitude)
        cos_h = (math.cos(zenith) - (sin_dec * math.sin(latitude))) / (cos_dec * math.cos(latitude))
#         print(f"7a.Sun's Local hour angle(CosH): {cos_h}")
        
        if cos_h > 1:
            print("Sun never rises on this location on this day")
            return None
        if cos_h < -1:
            print("Sun never sets on this location on this day")
            return None


        # 7b. finish calculating H and convert into hours
        h = math.degrees(math.acos(cos_h))
        if n == 6:
            h = 360 - h

        h = h / 360

        # 8. calculate local mean time of rising/setting
        t = h + ra - (0.06571 * time) - 6.622

        # 9. adjust back to UTC
        utc = t - longitude_hour
        utc = utc % 24
        return utc

        # 10. convert UT value to local time zone of latitude/longitude
        local_time = utc + self.local_offset

        return local_time



    def get_time(self, sunrise=True):
        if sunrise:
            time = self.__calculate_time(6)
        else:
            time = self.__calculate_time(18)
        hour = math.floor(time)
        temp = (time - hour) * 60
        minute = math.floor(temp)
        seconds = math.floor((temp - minute) * 60)
        
        return hour, minute, seconds
    
    def get_tithi(self):
        a = math.floor(self.year / 100)
        b = math.floor(a / 4)
        c = 2 - a + b
        e = math.floor(365.25 * (self.year + 4716))
        f = math.floor(30.6001 * (self.month + 1))
        julian_day = c + self.day + e + f - 1524.5
        day_since_new_moon = julian_day - 2451549.5
        new_moons = day_since_new_moon / 29.53
        temp = new_moons - math.floor(new_moons)
        tithi = temp * 29.53
        print(f"calculated rough tithi: {tithi}")
#         tithi  = (tithi + 15) % 30
        tithi = tithi % 30
        actual_tithi = math.floor(tithi)
        
        tithis = {}
        tithi = ['Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami', 'Shasthi',
                'Shaptami', 'Ashtami', 'Nawami', 'Dashami', 'Ekadashi', 'Dwadasi',
                'Tryodashi', 'Chaturdashi', 'wildcard']


        start = 0
        stop = 15
        for _ in range(2):
            for i, j in zip(range(start, stop), tithi):
                tithis[i+1] = f'{j}'
            start += 15
            stop += 15

        tithis[15] = 'Aushi'
        tithis[30] = 'Purnima'
        if actual_tithi >= 15:
            print (f'Krishna {tithis[actual_tithi]}')
        else:
            print(f'Shukla {tithis[actual_tithi]}')
        return actual_tithi
        
        

if __name__ == '__main__':
    place = (27.700769, -85.300140)
    time_ktm = SunRiseSet(year=2021, month=6, day=29, place=place, date_type='AD', local_offset=5.75)
    print(f'Sunrise : {time_ktm.get_time()}\nSunset: {time_ktm.get_time(False)}')

    # Sukla means wanning and Krishna means waxing
    print(f'Tithi: {time_ktm.get_tithi()}')