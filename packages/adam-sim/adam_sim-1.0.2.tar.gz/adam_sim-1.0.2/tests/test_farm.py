import numpy as np

from adam_sim import Adam
from adam_sim.entities import AdamInfo, Point, System


def main():
    adam: Adam = Adam()

    info: AdamInfo = adam.load()

    left_path: list[Point] = [info.left_manipulator.end_effector.position + Point(0.0, z, z) for z in np.linspace(0, 1, 100)]
    right_path: list[Point] = [info.right_manipulator.end_effector.position + Point(0.0, -z, z) for z in np.linspace(0, 1, 100)]

    for left_point, right_point in zip(left_path, right_path):
        adam.render()

        adam.left_manipulator.move_to(System(left_point,
                                             info.left_manipulator.systems[-1].x_axis,
                                             info.left_manipulator.systems[-1].y_axis,
                                             info.left_manipulator.systems[-1].z_axis))
        adam.right_manipulator.move_to(System(right_point,
                                              info.right_manipulator.systems[-1].x_axis,
                                              info.right_manipulator.systems[-1].y_axis,
                                              info.right_manipulator.systems[-1].z_axis,
                                              ))

        info = adam.step()

    adam.close()


if __name__ == '__main__':
    main()
