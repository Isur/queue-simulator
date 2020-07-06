from Utils import Utils


def calc_p0(servers, load):
    sum = 0
    for n in range(0, servers):
        sum += ((servers*load)**n)/Utils.factorial(n)
    res = sum + (((servers*load)**servers)/Utils.factorial(n))*1/(1-load)
    res = res**(-1)
    return res


class CalcModel(object):
    def __init__(self, service_rate, arrival_rate, servers, time_limit):
        self.service_rate = service_rate
        self.arrival_rate = arrival_rate
        self.servers = servers
        self.time_limit = time_limit
        self.system_load = self.calc_system_load()
        self.mean_service_time = 1/service_rate

    def stats(self):
        return self.delay_probability(), self.system_load, self.average_customers_in_queue(), self.mean_service_time, self.average_time_in_system()
        
    def probability_of_n_customers(self, n):
        if self.system_load >= 1:
            return None
        p0 = calc_p0(self.servers, self.system_load)
        if 0 <= n < self.servers:
            result = (((self.servers * self.system_load)**n)/Utils.factorial(n)) * p0
        elif n >= self.servers:
            result = (((self.servers**self.servers)*self.system_load**n)/Utils.factorial(self.servers)) * p0
        else:
            raise Exception
        return result

    def delay_probability(self):
        if self.system_load >= 1:
            return None
        return self.probability_of_n_customers(self.servers)/(1 - self.system_load)

    def calc_system_load(self):
        system_load = self.arrival_rate/(self.service_rate * self.servers)
        return system_load

    def average_customers_in_queue(self):
        if self.system_load >= 1:
            return None
        return self.delay_probability() * self.system_load/(1- self.system_load)

    def average_time_in_system(self):
        if self.system_load >= 1:
            return None
        return self.average_customers_in_queue()/self.arrival_rate

if __name__ == "__main__":
    # service rate | arrival rate | servers | time limit
    test_case = [3.2, 30.4, 10, 15]
    model = CalcModel(test_case[0], test_case[1], test_case[2], test_case[3])
    if model.system_load >= 1:
        print("No steady state")
        print(f"System load: {model.system_load}")
    else:
        print(f"System load: {model.system_load}")
        print(f"Probability of 3 customers: {model.probability_of_n_customers(3)}")
        print(f"Delay probability: {model.delay_probability()}")
        print(f"Average Customers in queue: {model.average_customers_in_queue()}")
        print(f"Average time in system = {model.average_time_in_system()}")
        print(f"Mean service time: {model.mean_service_time}")


