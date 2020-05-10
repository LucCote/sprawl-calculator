import sprawlcalculator as sc

if __name__ == "__main__":
    city = input("Enter a city to get it's sprawl score (or q to quit)\n")
    while city != "q":
        result = sc.get_city_info(city)
        if result:
            name, cntry, pop, lat, long, sprawl_score, img = result
            img.show()
            print(name + ", " + cntry + " has a sprawl score of " + str(sprawl_score) + "\n")
        else:
            print("Unable to find city")
        city = input("Enter a city to get it's sprawl score (or q to quit)\n")