from tabulate import tabulate


class Log(object):
    def __init__(self, time, event, customer, server, present):
        self.timestamp = time
        self.event = event
        self.customer = customer
        self.server = server
        self.present = present

    def __str__(self):
        if self.server:
            return f"In system: {self.present} | Customer {self.customer} at server {self.server} in time " \
                   f"{self.timestamp}: {self.event}"
        else:
            return f"In system: {self.present} | Customer {self.customer} in time {self.timestamp}: {self.event}"

    def to_tab(self):
        return [self.timestamp, self.event, self.server, self.customer, self.present]


class Logger(object):
    def __init__(self):
        self.logs = []

    def log(self, time, event, customer, server, present) -> None:
        """
            Log event

            Args:
                time (int): Time of event occurrence
                event (string): ARRIVAL | SERVICE | LEAVE
                customer (int): Customer id
                server (int): Server id
                present (int): Number of customers in service

        """
        log = Log(round(time, 4), event, customer, server, present)
        self.logs.append(log)

    def print_logs(self):
        for log in self.logs:
            print(log)

    def clean_logs(self):
        self.logs = []

    def _sort_logs(self):
        self.logs.sort(key=lambda x: x.timestamp)

    def print_tabular(self):
        data = self.get_data()
        headers = ["TIME", "EVENT", "SERVER", "CUSTOMER", "PRESENT"]
        print(tabulate(headers=headers, tabular_data=data))

    def get_data(self):
        return [log.to_tab() for log in self.logs]


log_machine = Logger()
