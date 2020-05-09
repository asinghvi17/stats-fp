import warming
import math
import matplotlib.pyplot as plt

city_map = {
    "Lander": "Wyoming",
    "Wausau": "Wisconsin",
    "Bluefield": "West Virginia",
    "Vancouver": "Washington",
    "Richmond": "Virginia",
    "SaltLakeCity": "Utah",
    "Houston": "Texas",
    "Nashville": "Tennessee",
    "Mitchell": "South Dakota",
    "Aiken": "South Carolina",
    "Williamsport": "Pennsylvania",
    "Portland": "Oregon",
    "Stillwater": "Oklahoma",
    "Toledo": "Ohio",
    "Williston": "North Dakota",
    "Raleigh": "North Carolina",
    "NewYork": "New York",
    "Albuquerque": "New Mexico",
    "Belvidere": "Illinois",
    "Trenton": "New Jersey",
    "Manchester": "New Hampshire",
    "Winnemucca": "Nevada",
    "McCook": "Nebraska",
    "Missoula": "Montana",
    "Jefferson": "Missouri",
    "Gulfport": "Mississippi",
    "SaintCloud": "Minnesota",
    "Kalamazoo": "Michigan",
    "Boston": "Massachusetts",
    "Baltimore": "Maryland",
    "Portland": "Maine",
    "Natchitoches": "Louisiana",
    "Louisville": "Kentucky",
    "Topeka": "Kansas",
    "CedarRapids": "Iowa",
    "SouthBend": "Indiana",
    "Springfield": "Illinois",
    "Boise": "Idaho",
    "Savannah": "Georgia",
    "Tampa": "Florida",
    "WashingtonDC": "District of Columbia",
    "Wilmington": "Delaware",
    "Pueblo": "Colorado",
    "Sacramento": "California",
    "Russellville": "Arkansas",
    "Phoenix": "Arizona",
    "MuscleShoals": "Alabama"
}

state_energies = {}
state_slopes = {}

def main():
    cities = open("data/regression_lines.csv")
    states = open("data/pc_energy_consumption.csv")

    for line in states:
        arr = line.rstrip().split(',')
        state = arr[0]
        energy = float(arr[1])
        state_energies[state] = energy
    states.close()

    for line in cities:
        arr = line.rstrip().split(',')
        city = arr[0]
        b1 = float(arr[2])

        if city not in city_map:
            continue

        state = city_map[city]
        state_slopes[state] = b1
    cities.close()

    x = []
    y = []
    for state in state_slopes:
        x.append(state_slopes[state])
        y.append(state_energies[state])
    mux = warming.mean(x)
    muy = warming.mean(y)

    R = 0
    Sxx = 0
    Syy = 0
    for i in range(len(x)):
        R += (x[i] - mux) * (y[i] - muy)
        Sxx += (x[i] - mux) ** 2
        Syy += (y[i] - muy) ** 2
    R /= math.sqrt(Sxx)
    R /= math.sqrt(Syy)
    print("Sample correlation coefficient r = " + str(R))
    
    plt.scatter(x, y)
    plt.title("Slope vs. per capita energy consumption for U.S. states")
    plt.xlabel("Slope")
    plt.ylabel("Per capita energy consumption (⋅ 10⁶ Btu)")
    plt.show()


if __name__ == "__main__":
    main()
