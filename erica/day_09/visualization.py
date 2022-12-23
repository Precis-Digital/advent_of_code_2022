from day_9 import get_data_into_lines, generate_head_coordinates, generate_tail_coordinates

if __name__ == "__main__":

    head_instructions = get_data_into_lines()

    head_coordinates = generate_head_coordinates(instructions=head_instructions)
    tail_coordinates = generate_tail_coordinates(head_coord=head_coordinates)

    tail_cords = []
    for i in range(8):
        tail_cords.append([(0, 0)] * i + generate_tail_coordinates(head_coord=tail_coordinates))

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    cord_list = [head_coordinates, tail_coordinates] + tail_cords

    points = []
    for i, cords in enumerate(zip(*cord_list)):
        for j, cord in enumerate(cords):
            if i == 0:
                point, = ax.plot(cord[0], cord[1], marker=f"${j}$", linestyle='None')
                points.append(point)
                continue

            points[j].set_data(cord[0], cord[1])

            plt.pause(0.005)
