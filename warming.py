import matplotlib.pyplot as plt

CITY_COLUMN = 1
FILE_COLUMN = 2

IDX_COLUMN = 0
TMAX_COLUMN = 2
TMIN_COLUMN = 3

city_temps = {}  # Dictionary of city name -> list of tuples (year, temp) of January 1st temperatures
output_data = []  # Data to be outputted: list of tuples (city, b0, b1 * 1000) 


def output():  # Output list of tuples into a .csv
    output_file = open("data/regression_lines.csv", "w")
    
    for tup in output_data:
        output_file.write(str(tup[0]) + ',' + str(tup[1]) + ',' + str(tup[2]) + '\n')

    output_file.close()


def mean(arr):  # Compute mean of a list
    total = 0
    for el in arr:
        total += el
    return total/len(arr)


def regression(city):  # Get beta0 and beta1 for a single city
    x = [tup[0] for tup in city_temps[city]]
    y = [tup[1] for tup in city_temps[city]]

    mux = mean(x)
    muy = mean(y)

    beta1 = 0
    denom = 0
    for i in range(len(x)):
        beta1 += (x[i] - mux) * (y[i] - muy)
        denom += (x[i] - mux) ** 2
    beta1 /= denom
    beta0 = muy - beta1 * mux
    
    return beta0, beta1
        
    
def plot(city):
    x = [tup[0] for tup in city_temps[city]]
    y = [tup[1] for tup in city_temps[city]]

    plt.xlabel("Year")
    plt.ylabel("Temperature (F)")
    plt.title("2-year average temperatures vs. year for Sacramento")

    plt.scatter(x, y)
    plt.show()

    
def process(city, file_name):  # Processes data for a single city
    data = open("data/" + file_name + ".csv")
    city_temps[city] = []

    i = 0
    year = None
    day_count = 0
    total_temp = 0
    for line in data:
        if i == 0:
            i += 1
            continue
            
        line = line.replace("\"", "")
        arr = line.rstrip().split(',')
        idx = int(arr[IDX_COLUMN])

        if i == 1:
            year = int(arr[1][:4])  # Get starting year
            i += 1

        tmin = arr[TMIN_COLUMN]
        tmax = arr[TMAX_COLUMN]
        if tmin != "NA" and tmax != "NA":  # Ignore missing values
            tmin = float(tmin)
            tmax = float(tmax)
            total_temp += tmin + tmax
            day_count += 2

        if idx % 730 == 729:  # If on the last day of the year
            if day_count != 0:   
                avg = total_temp/day_count
                city_temps[city].append((year, avg))
            
            year += 2
            day_count = 0
            total_temp = 0

    data.close()

        
def main():  # Reads every city in city_info.csv, and gets the name + filename
    city_info = open("data/city_info.csv")

    i = 0
    name_dict = {}
    for line in city_info:
        if i == 0:
            i += 1
            continue
        
        line = line.replace("\"", "");
        arr = line.rstrip().split(',')
        city = arr[CITY_COLUMN]
        file_name = arr[FILE_COLUMN]

        if city in name_dict:
            continue
        
        name_dict[city] = file_name
        process(city, file_name)
        beta0, beta1 = regression(city)
        
        print(city, beta0, beta1 * 1000)
        output_data.append((city, beta0, beta1 * 1000))

        i += 1

    city_info.close()
    output()
    plot("Phoenix")

    
if __name__ == "__main__":
    main()
