import boto3
import cv2
import credentials
import os

output_dir = './data'
output_dir_imgs = os.path.join(output_dir, 'imgs')
for file in os.listdir(output_dir_imgs):
    file_path = os.path.join(output_dir_imgs, file)
    if os.path.isfile(file_path):  
        os.remove(file_path)  


os.environ['AWS_DEFAULT_REGION'] = 'us-west-1'

#aws Reko client
reko_client = boto3.client('rekognition', 
                           aws_access_key_id = credentials.access_key, 
                           aws_secret_access_key = credentials.secret_key)

# target class
target_class = None

# load video / take input
cap = cv2.VideoCapture('./test2.mp4')

# read frames
frame_num = -1
ret = True
while ret:
    ret, frame = cap.read()

    if not ret:
        continue
    

    frame_num+=1
    H, W, _ = frame.shape
    # convert each frame to img type jpeg?
    _, buffer = cv2.imencode('.jpg', frame) # buffer 

    # convert buffer to bytes
    image_bytes = buffer.tobytes() 

    # detect obj
    response = reko_client.detect_labels(Image = {'Bytes' : image_bytes}, 
                              MinConfidence=50)
    
    for label in response['Labels']:
        for instance_nmr in range(len(label['Instances'])):

            bounding_box = label['Instances'][instance_nmr]['BoundingBox']
            x1 = int(bounding_box['Left'] * W)
            y1 = int(bounding_box['Top'] * H)
            width = int(bounding_box['Width'] * W)
            height = int(bounding_box['Height'] * H)
            #print(x1, y1, width, height)
            cv2.rectangle(frame, (x1, y1), (x1 + width, y1 + height), (0, 255, 0), 3)
    
    cv2.imwrite(os.path.join(output_dir_imgs, 'frame_{}.jpg'.format(str(frame_num).zfill(6))), frame)
    #cv2.imshow('frame', frame)

# write detections