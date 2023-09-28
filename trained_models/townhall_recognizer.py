import torch
import screen_grabber

town_hall_model = torch.hub.load(
    "ultralytics/yolov5", "custom", path="trained_models/townhall.pt"
)


def distance_from_center(x, y):
    true_x = 0.586601 - 0.588162
    x += true_x
    true_y = 0.334110 - 0.354090
    y += true_y
    x_factor = 1.3511435710167212
    center_x = 1 - 0.503246
    center_y = 0.470522
    delta_x = (x - center_x) * x_factor
    delta_y = y - center_y
    return (delta_x**2 + delta_y**2) ** 0.5


def is_townhall_snipable():
    image = screen_grabber.screen_image()

    inferno_results = town_hall_model(image)

    for _, result in enumerate(inferno_results.pandas().xyxy):
        for _, row in result.iterrows():
            if row["confidence"] > 0.76:
                xmax = row["xmax"]
                xmin = row["xmin"]
                ymax = row["ymax"]
                ymin = row["ymin"]
                # x_center = (xmax + xmin) / 2 / 1920
                # y_center = (ymax + ymin) / 2 / 1080
                x_center = (xmax + xmin) / 2 / 3120
                y_center = (ymax + ymin) / 2 / 1440
                distance = distance_from_center(x_center, y_center)

                if distance > 0.19:
                    print(distance)
                # if distance > 0.15:
                    return True

    return False
