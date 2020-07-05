class Customer(object):
    def __init__(self, customer_id, arrival_time):
        """
            Args:
                customer_id: id of customer
                arrival_time: Time when customer arrive to the service
        """
        self.customer_id = customer_id
        self.arrival_time = arrival_time
        self.service_start = None
        self.service_finish = None

    def start(self, time):
        """
            Starts customer service
            Args:
                time: start service time
        """
        self.service_start = time

    def end(self, time):
        """
            Finish customer service
            Args:
                time: finish service time
        """
        self.service_finish = time

    def service_time(self):
        """
            Returns:
                Service time
        """
        if self.service_start is None:
            return None

        if self.service_finish is None:
            return None

        return self.service_finish - self.service_start
