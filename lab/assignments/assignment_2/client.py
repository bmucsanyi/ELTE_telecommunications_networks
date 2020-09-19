"""Áramkör szimuláció

Készíts programot, ami leszimulálja az erőforrások lefoglalását és
felszabadítását a JSON fájlban megadott topológia, kapacitások és igények
alapján!

Script paraméterezése: python3 client.py cs.json

A program kimenete:
    esemény sorszám. <esemény név>: <node1><-><node2> st:<szimuálciós idő> [- <sikeres/sikertelen>]

Pl.:
    igény foglalás: A<->C st:1 – sikeres
    igény foglalás: B<->C st:2 – sikeres
    igény felszabadítás: A<->C st:5
    igény foglalás: D<->C st:6 – sikeres
    igény foglalás: A<->C st:7 – sikertelen
    …

Leadás: A program leadása a BE-AD rendszeren .zip formátumban,
amiben egy client.py szerepeljen!
"""
import argparse
import json


class ResourceReservationError(Exception):
    def __init__(self, A, B):
        super().__init__(f"Resource reservation failed from {A} to {B}!")


class NoCircuitError(Exception):
    def __init__(self, A, B):
        super().__init__(f"There is no circuit from {A} to {B}!")


def read_json(file_name):
    with open(file_name) as f:
        return json.load(f)


def setup(network_data):
    link_capacities = {}
    for link in network_data["links"]:
        points = tuple(sorted(link["points"]))  # Key needs to be hashable
        maximum = link["capacity"]
        link_capacities[points] = {"current": 0, "maximum": maximum}
    return link_capacities


def search_circuits(start, end, circuits):
    correct_routes = []
    for circuit in circuits:
        if circuit[0] == start and circuit[-1] == end:
            correct_routes.append(circuit)

    if not correct_routes:
        raise NoCircuitError(start, end)

    return correct_routes


def get_link(circuit, start, link_capacities):
    link_start, link_end = circuit[start], circuit[start + 1]
    points = tuple(sorted((link_start, link_end)))
    link = link_capacities[points]
    return link, link_start, link_end


def reserve_circuit(circuits, bandwidth, link_capacities):
    for circuit_ind, circuit in enumerate(circuits):
        occupied_route = False
        # First we check the route
        for i in range(len(circuit) - 1):
            link, link_start, link_end = get_link(circuit, i, link_capacities)
            available_bandwidth = link["maximum"] - link["current"]

            if available_bandwidth < bandwidth:
                if circuit_ind == len(
                        circuits) - 1:  # Our last resort is occupied, too
                    raise ResourceReservationError(link_start, link_end)
                else:
                    # The current one is occupied,
                    # but we might have a chance with later circuits
                    occupied_route = True
                    break

        if not occupied_route:
            # If the reservation is possible, we do it
            for i in range(len(circuit) - 1):
                link, _, _ = get_link(circuit, i, link_capacities)
                link["current"] += bandwidth
            return circuit  # We reserved this exact circuit


def free_circuit(circuit, bandwidth, link_capacities):
    for i in range(len(circuit) - 1):
        link, _, _ = get_link(circuit, i, link_capacities)
        link["current"] -= bandwidth


def simulate(network_data, link_capacities):
    event_id = 1
    reserved_circuits = []

    for current_time in range(1, network_data["simulation"]["duration"] + 1):
        for demand in network_data["simulation"]["demands"]:
            start, end = demand["end-points"]
            bandwidth = demand["demand"]

            if demand["start-time"] == current_time:
                try:
                    circuits = search_circuits(
                        start, end, network_data["possible-circuits"])
                    print(
                        f"{event_id}. igény foglalás: {start}<->{end} st:{current_time}",
                        end='')
                    circuit = reserve_circuit(circuits, bandwidth,
                                              link_capacities)

                    # There can be many routes... which should be freed?
                    log = {"end-time": demand["end-time"], "circuit": circuit}
                    reserved_circuits.append(log)
                    print(" - sikeres")
                except NoCircuitError:
                    print("Incorrect JSON file! Aborting...")
                    raise
                except ResourceReservationError:
                    print(" - sikertelen")
                event_id += 1

            if demand["end-time"] == current_time:
                circuits = search_circuits(start, end,
                                           network_data["possible-circuits"])

                for log in reserved_circuits[:]:
                    # We found the circuit to be freed...
                    if log["end-time"] == current_time:
                        circuit = log["circuit"]
                        free_circuit(circuit, bandwidth, link_capacities)
                        print(
                            f"{event_id}. igény felszabadítás: {start}<->{end} st:{current_time}"
                        )
                        reserved_circuits.remove(log)
                        break

                event_id += 1


def main(args):
    network_data = read_json(args.file_name)
    link_capacities = setup(network_data)
    simulate(network_data, link_capacities)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name')
    args = parser.parse_args()
    main(args)