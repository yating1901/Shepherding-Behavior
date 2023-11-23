import os
import cv2

def create_video():
    fps = 30
    size = (640, 480)
    folder_path = os.getcwd() + "/images/"
    vid_write = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)
    # print("folder_path:", folder_path)
    file_list = os.listdir(folder_path)
    # print(len(file_list))
    # for file_name in file_list:
    #     file_path = os.path.join(folder_path, file_name)
    #     if os.path.isfile(file_path):
    #         file_ext = os.path.splitext(file_path)[1]
    #         if file_ext.lower() in ['.avi']:
    #             os.remove(file_path)
    for index in range(len(file_list)):
        file_path = folder_path + str(index) + ".png"
        img = cv2.imread(file_path)
        vid_write.write(img)
    vid_write.release()
    cv2.destroyAllWindows()