from Customer import Customer
from Utils import Utils


class Server(object):
    def __init__(self, server_id, service_rate):
        """
            Args:
                server_id: id of the server
                service_rate: service rate
        """
        self.server_id = server_id
        self.service_rate = service_rate
        self.customer = None
        self.estimated_finish = None
        self.is_busy = False

    def service(self, customer: Customer, time):
        """
            Start service

            Args:
                customer: Customer object
                time: time when service started
        """
        self.is_busy = True
        self.customer = customer
        customer.start(time)
        self._set_estimated_finish(time)

    def process(self, time):
        """
            Process of service, check if it is time to finish service.

            Args:
                time: current time
        """
        customer = self.customer
        if self.estimated_finish is None or customer is None:
            return None
        if time < self.estimated_finish:
            return None
        self._service_finish()
        return customer

    def _set_estimated_finish(self, start_time):
        self.estimated_finish = start_time + Utils.exponential_distribution(self.service_rate)

    def _service_finish(self):
        self.customer.end(self.estimated_finish)
        self.is_busy = False
        self.customer = None
        self.estimated_finish = None
