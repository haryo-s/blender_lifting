import json
import sys
sys.path.append("D:/Photography/CurrentProjects/ProgrammingProjects/blender_lifting/blender_lifting_venv/Lib/site-packages")

import lifting
import cv2

image_path = "D:/Photography/CurrentProjects/ProgrammingProjects/blender_lifting/data/images/F21AN.bmp"
SESSION_PATH = "D:/Photography/CurrentProjects/ProgrammingProjects/blender_lifting/data/saved_sessions/init_session/init"
PROB_MODEL_PATH = 'D:/Photography/CurrentProjects/ProgrammingProjects/blender_lifting/data/saved_sessions/prob_model/prob_model_params.mat'

if len(sys.argv) == 4:
    image_path = sys.argv[1]
    SESSION_PATH = sys.argv[2]
    PROB_MODEL_PATH = sys.argv[3]

# print(str(sys.argv))

def analyse_image():
    # image_path = "data/images/test_image.png"
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_size = image.shape

    pose_estimator = lifting.PoseEstimator(image_size, SESSION_PATH, PROB_MODEL_PATH)
    pose_estimator.initialise()

    pose_2d, visibility, pose_3d = pose_estimator.estimate(image)

    pose_estimator.close()
    
    coordinates = []
    for i in range(len(pose_3d[0][0])):
        for point in pose_3d:
            coordinates.append([point[0][i], point[1][i], point[2][i]])

    # print(json.dumps(coordinates))
    return json.dumps(coordinates)

if __name__ == "__main__":
    print(analyse_image())