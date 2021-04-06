import os
import uuid
import numpy as np
import matplotlib.pyplot as plt

WIDTH = 1200
HEIGHT = 2000


def generate_heatmap(results, save_path):
    hm = np.zeros((WIDTH, HEIGHT))

    detections = results['processing'][0]['detections']

    for detection in detections:
        try:
            persons = detection['objects']['person']['boxes']
        except KeyError:
            continue

        for box in persons:
            # print(box['y'], box['height'], box['y'] + box['height'])
            # print(box['x'], box['width'], box['x'] + box['width'])

            for i in range(box['y'], box['y'] + box['height'] - 1):
                for j in range(box['x'], box['x'] + box['width'] - 1):
                    hm[i][j] += 1

    fig, ax = plt.subplots()
    ax.imshow(hm)

    heatmap_id = str(uuid.uuid1())
    heatmap_fn = os.path.join(save_path, heatmap_id)
    plt.savefig(heatmap_fn)
    return heatmap_id
