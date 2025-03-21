import create_images
import create_video

def user_input():

    #do something where its like while obj in the amazon services table 
    target_class = str(input("Enter the object: "))
    video_path = str(input("Enter the video path: "))

    return target_class, video_path

if __name__ == '__main__':
    target_class = "Penguin"
    video_path = "./test2.mp4"
    #create_images.create_images(target_class, video_path)
    create_video.create_video()