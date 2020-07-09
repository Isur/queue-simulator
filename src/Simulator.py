from Server import Server
from ArrivalProcess import ArrivalProcess
from Utils import Utils
from Logger import log_machine
import time


class MMC(object):
    def __init__(self, settings):
        """
            Args:
                settings: [service rate, arrival rate, servers number, time limit]
        """
        self.service_rate, \
            self.arrival_rate, \
            self.servers_number, \
            self.time_limit = settings
        self.customers = []
        self.servers = []
        self.queue = []
        # self.print_settings()
        self._setup_servers()
        self.customers_in_system = 0

    def print_settings(self):
        """
            Print information about current system settings.
        """
        print(f"Run with settings:\n"
              f"Service rate: {self.service_rate}\n"
              f"Arrival rate: {self.arrival_rate}\n"
              f"Number of servers: {self.servers_number}\n"
              f"Time limit: {self.time_limit}")

    def run(self, precision=4):
        """
            Start simulation.
        """
        log_machine.clean_logs()
        current_time = 0
        arrivals = ArrivalProcess(self.arrival_rate)
        while current_time <= self.time_limit:
            if current_time >= arrivals.next_customer:
                customer = arrivals.getNext()
                self.customers.append(customer)
                self.queue.append(customer)
                self.customers_in_system += 1
                log_machine.log(current_time, "ARRIVAL", customer.customer_id, None, self.customers_in_system)

            while len(self.queue) > 0:
                current = self.queue[0]
                server = self._random_server()
                if server is not None:
                    server.service(current, current_time)
                    log_machine.log(current_time,
                                    "SERVICE",
                                    current.customer_id,
                                    server.server_id,
                                    self.customers_in_system)
                    self.queue.pop(0)
                else:
                    break

            for server in self.servers:
                finished = server.process(current_time)
                if finished is not None:
                    self.customers_in_system -= 1
                    log_machine.log(current_time,
                                    "LEAVE",
                                    finished.customer_id,
                                    server.server_id,
                                    self.customers_in_system)
            current_time += 1*10**(-precision)
        total_customers = len(self.customers)
        customers_serviced = total_customers - self.customers_in_system
        customers_not_serviced = self.customers_in_system
        mean = self.stats()
        process = log_machine.get_data()
        return total_customers, customers_serviced, customers_not_serviced, mean, process

    def _setup_servers(self):
        for svr in range(self.servers_number):
            server = Server(svr, self.service_rate)
            self.servers.append(server)

    def _random_server(self) -> Server:
        free_servers = []
        for server in self.servers:
            if not server.is_busy:
                free_servers.append(server)
        if len(free_servers) > 0:
            return Utils.random_element(free_servers)
        return None

    def stats(self):
        time_sum = 0
        num = 0
        for customer in self.customers:
            service_time = customer.service_time()
            if service_time is not None:
                time_sum += service_time
                num += 1
        mean = time_sum / num
        return mean


if __name__ == "__main__":
    # service rate | arrival rate | servers | time limit
    test_cases = [
        [1, 3, 3, 10],
    ]

    logs = []

    for i in range(len(test_cases)):
        print("".join(["=" for x in range(24)]))
        start = time.time()
        model = MMC(test_cases[i])
        total, serviced, not_serviced, mean, process = model.run(4)
        print(f"Total customers: {total}")
        print(f"Served customers: {serviced}")
        print(f"Not served customers: {not_serviced}")
        print(f"Mean service time: {mean}")
        logs.append(log_machine.logs)
        log_machine.clean_logs()
        end = time.time()
        print(f"Simulation time: {round(end - start, 4)}")
        print("Process:")
        for p in process:
            print(p)
        print("".join(["=" for x in range(24)]))
