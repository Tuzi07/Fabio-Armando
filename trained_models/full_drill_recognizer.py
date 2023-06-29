import torch
import screen_grabber

drill_model = torch.hub.load(
    "ultralytics/yolov5", "custom", path="trained_models/drill.pt"
)
full_drill_model = torch.hub.load(
    "ultralytics/yolov5", "custom", path="trained_models/full_drill.pt"
)


def has_full_drill():
    image = screen_grabber.screen_image()

    drill_results = drill_model(image)

    for _, result in enumerate(drill_results.pandas().xyxy):
        for _, row in result.iterrows():
            if row["confidence"] > 0.75:
                xmax = row["xmax"]
                xmin = row["xmin"]
                ymax = row["ymax"]
                ymin = row["ymin"]
                cropped_image = image.crop((xmin, ymin, xmax, ymax))
                box_results = full_drill_model(cropped_image)
                for _, box_result in enumerate(box_results.pandas().xyxy):
                    for _, box_row in box_result.iterrows():
                        if box_row["name"] == "full" and box_row["confidence"] > 0.84:
                            # drill_results.save()
                            return True

    return False
