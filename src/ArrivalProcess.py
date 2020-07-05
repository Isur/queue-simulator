from Utils import Utils
from Customer import Customer


class ArrivalProcess(object):
    def __init__(self, arrival_rate):
        """
            Controller of arrival process in the system
            Args:
                arrival_rate: rate of arrivals complies with poisson
        """
        self.arrival_rate = arrival_rate
        self.next_customer = 0
        self.created_customers = 0

    def getNext(self):
        """
            Returns:
                customer: new customer
        """
        customer = Customer(self.created_customers, self.next_customer)
        self.created_customers += 1
        self.next_customer += Utils.exponential_distribution(self.arrival_rate)
        return customer
