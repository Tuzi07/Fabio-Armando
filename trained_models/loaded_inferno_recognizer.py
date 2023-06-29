import torch
import screen_grabber

inferno_tower_model = torch.hub.load(
    "ultralytics/yolov5", "custom", path="trained_models/inferno_tower.pt"
)
loaded_inferno_model = torch.hub.load(
    "ultralytics/yolov5", "custom", path="trained_models/loaded_inferno.pt"
)


def has_loaded_inferno():
    image = screen_grabber.screen_image()

    inferno_results = inferno_tower_model(image)

    for _, result in enumerate(inferno_results.pandas().xyxy):
        for _, row in result.iterrows():
            if row["confidence"] > 0.3:
                xmax = row["xmax"]
                xmin = row["xmin"]
                ymax = row["ymax"]
                ymin = row["ymin"]
                cropped_image = image.crop((xmin, ymin, xmax, ymax))
                load_results = loaded_inferno_model(cropped_image)
                for _, box_result in enumerate(load_results.pandas().xyxy):
                    for _, box_row in box_result.iterrows():
                        # print(box_row["name"], "with confidence", box_row["confidence"])
                        if box_row["name"] == "loaded" and box_row["confidence"] > 0.7:
                            # inferno_results.save()
                            return True

    return False
