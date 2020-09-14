import json


def points_needed(data):
    max_point = sum(
        (
            data["haziPont"]["max"],
            data["1zhPont"]["max"],
            data["mininetPont"]["max"],
            data["2zhPont"]["max"]
        )
    )

    curr_point = sum(
        (
            data["haziPont"]["elert"],
            data["1zhPont"]["elert"],
            data["mininetPont"]["elert"],
        )
    )

    grade_dict = {
        2: 50,
        3: 60,
        4: 75,
        5: 85,
    }

    fail_limit_1 = data["1zhPont"]["minimum"] * data["1zhPont"]["max"]
    failed = data["1zhPont"]["elert"] < fail_limit_1

    for grade in grade_dict:
        minimum_point = grade_dict[grade] * max_point / 100  # Originally its %.
        if failed:
            print(f"{grade} : Remenytelen")
        else:
            fail_limit_2 = data["2zhPont"]["minimum"] * data["2zhPont"]["max"]
            needed_point = minimum_point - curr_point
            if needed_point <= fail_limit_2:
                print(f"{grade} : 10.0")
            elif fail_limit_2 < needed_point <= data["2zhPont"]["max"]:
                print(f"{grade} : {needed_point}")
            else:
                print(f"{grade} : Remenytelen")


def main():
    with open("pontok.json") as f:
        data = json.load(f)
    points_needed(data)


if __name__ == "__main__":
    main()