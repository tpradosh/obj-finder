import boto3
import cv2
import credentials
import os

def create_images(target_class, video_path):
    #create the output dirs and reset any files in them
    output_dir = './data'
    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        if os.path.isfile(file_path):  
            os.remove(file_path)


    #aws stuff
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'
    reko_client = boto3.client('rekognition', 
                           aws_access_key_id = credentials.access_key, 
                           aws_secret_access_key = credentials.secret_key)

    target_class = 'Penguin'
    video_path = './test2.mp4' 
    #user input this 
    # load video / take input
    cap = cv2.VideoCapture(video_path) #user input this 

    # read frames
    frame_num = -1
    ret = True
    while ret:
        ret, frame = cap.read()
        frame_num+=1
        if not ret: 
            continue
        
        #x is just the uneeded output
        H, W, x = frame.shape

        # convert each frame to img type jpg
        x, buffer = cv2.imencode('.jpg', frame) # buffer 

        # convert buffer to bytes
        image_bytes = buffer.tobytes() 

        # detect obj
        response = reko_client.detect_labels(Image = {'Bytes' : image_bytes}, 
                                MinConfidence=50)
        
        #create the bounding boxes on the objs
        for label in response['Labels']:
            if label['Name'] == target_class:
                for instance in label['Instances']:

                    bounding_box = instance['BoundingBox']
                    x1 = int(bounding_box['Left'] * W)
                    y1 = int(bounding_box['Top'] * H)
                    width = int(bounding_box['Width'] * W)
                    height = int(bounding_box['Height'] * H)
                    #print(x1, y1, width, height)
                    cv2.rectangle(frame, (x1, y1), (x1 + width, y1 + height), (0, 255, 0), 3)
        
        cv2.imwrite(os.path.join(output_dir, 'frame_{}.jpg'.format(str(frame_num).zfill(6))), frame)
        #cv2.imshow('frame', frame)