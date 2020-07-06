from Simulator import MMC
from CalcModel import CalcModel
from Utils import Utils
from time import time
from multiprocessing import Process, Pipe
from tqdm import tqdm
import os


class Test(object):
    def __init__(self, arrival_rate, service_rate, servers, time_limit, test_id):
        self.service_rate = service_rate
        self.arrival_rate = arrival_rate
        self.servers = servers
        self.time_limit = time_limit
        self.test_id = test_id
        self.total = None
        self.serviced = None
        self.not_serviced = None
        self.mean_time = None
        self.process = None
        self.delay_probability = None
        self.system_load = None
        self.average_customers = None
        self.mean_service_time = None
        self.average_time_in_system = None

    def perform_test(self, process=True):
        simulation = MMC([self.service_rate, self.arrival_rate, self.servers, self.time_limit])
        model = CalcModel(self.service_rate, self.arrival_rate, self.servers, self.time_limit)

        self.delay_probability, self.system_load, self.average_customers, self.mean_service_time, self.average_time_in_system = model.stats()

        if process:
            self.total, self.serviced, self.not_serviced, self.mean_time, self.process = simulation.run(4)
        else:
            self.total, self.serviced, self.not_serviced, self.mean_time, _ = simulation.run(2)

    def get_data(self):
        return [self.total,
                self.serviced,
                self.not_serviced,
                round(self.mean_time, 4),
                self.service_rate,
                self.arrival_rate,
                self.servers,
                self.time_limit,
                self.delay_probability,
                self.system_load,
                self.average_customers,
                self.mean_service_time,
                self.average_time_in_system]


class Tester(object):
    def __init__(self, number_of_tests):
        self.tests = []
        self.results = []
        self.number = number_of_tests
        self.progress = 0

    def prepare_tests(self):
        tests = []
        for i in range(self.number):
            service_rate = Utils.random_number([1, 10])
            arrival_rate = Utils.random_number([1, 10])
            servers = Utils.random_number([2, 5], True)
            time_limit = 10 * (i % 10 + 1)
            test = Test(arrival_rate=arrival_rate, servers=servers, service_rate=service_rate,
                        time_limit=time_limit, test_id=i)
            tests.append(test)
        self.tests = tests

    def run_multi_process(self):
        self.results = []
        process_num = os.cpu_count()
        chunk_size = max(int(Utils.round(self.number / process_num)), 1)
        chunked = [self.tests[i:i + chunk_size] for i in range(0, self.number, chunk_size)]
        print(f"Number of tests: {self.number}")
        print(f"CPU Process number: {process_num}")
        print("Number of tests processed by each process:")
        print([len(chunk) for chunk in chunked])
        print("Progress bar might by little jumpy cause of multiprocessing")
        pbar = tqdm(total=self.number)
        pipe_list = []
        processes = []
        for chunk in chunked:
            recv_end, send_end = Pipe(False)
            p = Process(target=self.__tests, args=[chunk, pbar, send_end])
            processes.append(p)
            pipe_list.append(recv_end)

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        results = [res.recv() for res in pipe_list]
        for chunk in results:
            for result in chunk:
                self.results.append(result)
        pbar.close()

    def __tests(self, chunk, pbar, callback):
        results = []
        example = False
        for i, test in enumerate(chunk):
            pbar.update(4)
            test.perform_test(not example)
            if example is False:
                self.save_results_to_file(test)
                example = True
            results.append(test.get_data())
        callback.send(results)

    def print_results(self, process_time):
        headers = ["Total Customers",
                   "Serviced Customers",
                   "Not Serviced Customers",
                   "Service Mean Time",
                   "Service Rate",
                   "Arrival Rate",
                   "Servers Number",
                   "Time Limit",
                   "Delay probability",
                   "System load",
                   "Average Customers",
                   "Mean Service Time",
                   "Average Time In System"]
        print("")
        print("".join(["=" for x in range(150)]))
        print(f"Tested in {process_time}s")
        print("".join(["=" for x in range(150)]))
        Utils.save_csv(self.results, headers, "../results/results.csv")
        print("Results saved to file '../results/results.csv'")
        print("".join(["=" for x in range(150)]))

    @staticmethod
    def save_results_to_file(random_test: Test):
        data = (f"Run with settings:\n"
                f"Service rate: {random_test.service_rate}\n"
                f"Arrival rate: {random_test.arrival_rate}\n"
                f"Number of servers: {random_test.servers}\n"
                f"Time limit: {random_test.time_limit}")
        data += "\n"
        headers = ["Time", "Event", "Server id", "Customer id", "Customers in system"]
        tab = Utils.get_table(random_test.process, headers)
        data += tab
        Utils.save_txt(data, f"../results/process-{random_test.test_id}.txt")
        Utils.save_csv(random_test.process, headers, f"../results/process-{random_test.test_id}.csv")


if __name__ == "__main__":
    Utils.clear_results()
    tester = Tester(100)
    tester.prepare_tests()
    start_time = time()
    tester.run_multi_process()
    end_time = time()
    tester.print_results(end_time - start_time)
