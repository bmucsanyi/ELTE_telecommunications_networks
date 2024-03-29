"""Ping / Traceroute

Válasszuk ki az első és utolsó 10 nevet a listából,
írjunk egy python programot, ami végig megy a leszűkített
20 elemű listán és minden címre lefuttatja a traceroute és
ping toolokat, majd az eredményeket rendezett formában két fájlba írja!

Script paraméterezése: python3 client.py hosts.csv
(NEM MILLIÓ SOROS ÉS EGY HOST TÖBBSZÖR IS SZEREPELHET!!!)

Traceroute paraméterek: max. 30 hopot vizsgáljunk
Ping paraméterek: 10 próba legyen

Kimeneti fájlok (ld. diák):
    traceroute.json
    ping.json

A teszt 10 perc után lelövi a futást!!!
A párhuzamos futtatás esetén vigyázzunk és limitáljuk a processek
maximális számát!!!
Leadás: A program leadása a BE-AD rendszeren .zip formátumban,
amiben egy client.py szerepeljen!
"""
import argparse
from collections import deque
import datetime
import json
import platform
from subprocess import PIPE, Popen


def head(file_name, n):
    subprocess = Popen(['head', '-n', str(n), file_name],
                       stdout=PIPE,
                       stderr=PIPE)
    subprocess.wait()
    return subprocess.communicate()[0].decode('utf-8')


def tail(file_name, n):
    subprocess = Popen(['tail', '-n', str(n), file_name],
                       stdout=PIPE,
                       stderr=PIPE)
    subprocess.wait()
    return subprocess.communicate()[0].decode('utf-8')


def process_text(text):
    text = text.split()  # Splits on whitespaces.
    list_ = [site.split(',')[1] for site in text]  # Removes ordering.
    return list_


def pretty_print(adj, file_name, list):
    print(f"{adj.capitalize()} ten entries of {file_name}:")
    for entry in list:
        print(f"\t{entry}")


def add_subprocess(command, website, subprocesses, max_subprocesses, data):
    if command not in ["traceroute", "ping"]:
        raise ValueError("Invalid command!")

    if len(subprocesses) == max_subprocesses // 2:
        # The subprocess started last
        subprocesses[0][0].wait()
        output = subprocesses[0][0].communicate()[0].decode('utf-8')
        target = subprocesses[0][1]
        subprocesses.popleft()

        current_data = {
            "target": target,
            "output": output,
        }

        key = "traces" if command == "traceroute" else "pings"
        data[key].append(current_data)

    if command == "traceroute":
        command_list = [command, website, "-m", "30"]
    else:
        command_list = [command, website, "-c", "10"]

    subprocesses.append((Popen(command_list, stdout=PIPE,
                               stderr=PIPE), website))


def finish_subprocesses(command, subprocesses, data):
    if command not in ["traceroute", "ping"]:
        raise ValueError("Invalid command!")

    for subprocess, target in subprocesses:
        subprocess.wait()
        output = subprocess.communicate()[0].decode('utf-8')
        current_data = {
            "target": target,
            "output": output,
        }
        key = "traces" if command == "traceroute" else "pings"
        data[key].append(current_data)


def collect_data(websites, max_subprocesses, verbose):
    # https://superuser.com/questions/731623/opensuse-root-commands-error (PATH=$PATH:/usr/sbin)
    # https://unix.stackexchange.com/questions/26047/how-to-correctly-add-a-path-to-path
    def get_system():
        opsys = platform.system()
        if opsys == "Darwin":
            return "mac"
        else:
            return opsys.lower()

    def setup(code):
        collection = "traces" if code == "traceroute" else "pings"
        return {
            "date": datetime.date.today().strftime("%Y%m%d"),
            "system": get_system(),
            collection: [],
        }

    if verbose:
        print("Starting collecting data...")

    traceroute_data, ping_data = setup("traceroute"), setup("ping")

    tr_subprocesses = deque()
    p_subprocesses = deque()

    for index, website in enumerate(websites):
        if verbose:
            print(f"{index + 1} {website}")

        add_subprocess("traceroute", website, tr_subprocesses,
                       max_subprocesses, traceroute_data)
        add_subprocess("ping", website, p_subprocesses, max_subprocesses,
                       ping_data)

    finish_subprocesses("traceroute", tr_subprocesses, traceroute_data)
    finish_subprocesses("ping", p_subprocesses, ping_data)

    if verbose:
        print("Finished collecting data!")

    return traceroute_data, ping_data


def save_data(traceroute_data, ping_data, verbose):
    if verbose:
        print("Saving data...")

    with open("traceroute.json", "w") as tr, open("ping.json", "w") as p:
        json.dump(traceroute_data, tr)
        json.dump(ping_data, p)

    if verbose:
        print("Data is saved!")


def main(args, verbose=True):
    first_ten = head(args.file_name, 10)
    first_ten = process_text(first_ten)

    last_ten = tail(args.file_name, 10)
    last_ten = process_text(last_ten)

    if verbose:
        pretty_print("first", args.file_name, first_ten)
        pretty_print("last", args.file_name, last_ten)

    websites = first_ten + last_ten
    traceroute_data, ping_data = collect_data(websites, 40, verbose)

    save_data(traceroute_data, ping_data, verbose)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name')
    args = parser.parse_args()
    main(args, verbose=True)