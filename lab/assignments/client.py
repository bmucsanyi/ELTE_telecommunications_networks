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
A párhuzamos futtatás esetén vigyázzunk és limitáljuk a processek maximális számát!!!
Leadás: A program leadása a BE-AD rendszeren .zip formátumban, amiben egy client.py szerepeljen!
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
        if len(tr_subprocesses) == max_subprocesses // 2:
            # The traceroute subprocess started last
            tr_subprocesses[0][0].wait()
            output = tr_subprocesses[0][0].communicate()[0].decode('utf-8')
            target = tr_subprocesses[0][1]
            tr_subprocesses.popleft()

            current_data = {
                "target": target,
                "output": output,
            }
            traceroute_data["traces"].append(current_data)

        tr_subprocesses.append((Popen(["traceroute", website, "-m", "30"],
                                      stdout=PIPE,
                                      stderr=PIPE), website))

        if len(p_subprocesses) == max_subprocesses // 2:
            p_subprocesses[0][0].wait()  # The ping subprocess started last
            output = p_subprocesses[0][0].communicate()[0].decode('utf-8')
            target = p_subprocesses[0][1]
            p_subprocesses.popleft()

            current_data = {
                "target": target,
                "output": output,
            }
            ping_data["pings"].append(current_data)

        p_subprocesses.append((Popen(["ping", website, "-c", "10"],
                                     stdout=PIPE,
                                     stderr=PIPE), website))

    for subprocess, target in tr_subprocesses:
        subprocess.wait()
        output = subprocess.communicate()[0].decode('utf-8')
        current_data = {
            "target": target,
            "output": output,
        }
        traceroute_data["traces"].append(current_data)

    for subprocess, target in p_subprocesses:
        subprocess.wait()
        output = subprocess.communicate()[0].decode('utf-8')
        current_data = {
            "target": target,
            "output": output,
        }
        ping_data["pings"].append(current_data)

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


def main(verbose=True):
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name')
    args = parser.parse_args()

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
    main(verbose=True)