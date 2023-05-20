import face_recognition
import cv2
import numpy as np
import pyttsx3
import json
import datetime
import glob
import time


# using now() to get current time
# current_time = datetime.datetime.now()

def get_face_encoding(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    return face_encoding

def get_current_date():
    current_time = datetime.datetime.now()
    return "{}-{}-{}".format(current_time.day, current_time.month, current_time.year)

folder_path = "images/"
image_paths = glob.glob(folder_path + "*.jpg")

known_face_encodings = []
known_face_names = []

for path in image_paths:
    # image_name = path.split("/")[-1].split(".")[0]
    image_name = path.replace("images\\", "").replace(".jpg", "")
    face_encoding = get_face_encoding(path)
    known_face_encodings.append(face_encoding)
    known_face_names.append(image_name)

video_capture = cv2.VideoCapture(0)

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

text_speech = pyttsx3.init()

while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                with open("data.json", "r") as infile:
                    data = json.load(infile)

                for i in range(len(data)):
                     # Get the attendance data for this person
                    # name = data[i]["name"]
                    # total_attendance = data[i]["total_attendance"]

                    # print(data[i]['name'])
                    if name == data[i]['name']:
                                new_date=get_current_date()
                                if data[i]["present"] == []:
                                    print("recording your attendance")
                                    data[i]["total_attendance"] += 1
                                    data[i]["present"].append(new_date)
                    # Write the updated data to the JSON file
                                    with open("data.json", "w") as outfile:
                                        json.dump(data, outfile, indent=4)
                                    text_speech.say("hello , i,am  ,,,,  daryl   ,,,,, I ,can , recognize , you ,,, your ,name ,is {} ,,, and your attendace is {}".format(known_face_names[best_match_index],data[i]['total_attendance']))
                                
                                elif data[i]["present"][-1] == new_date:
                                    print("your attendance is already recorded")
                                    text_speech.say(" {} your attendance is already recorded for today ,,, and your total attendance is {}".format(known_face_names[best_match_index],data[i]['total_attendance']))
                                    time.sleep(5)
                                    break
                                else:
                                    print("recording your attendance")
                                    
                                    data[i]["total_attendance"] += 1
                                

                                    data[i]["present"].append(new_date)

                    # Write the updated data to the JSON file
                                    with open("data.json", "w") as outfile:
                                        json.dump(data, outfile, indent=4)
                                    text_speech.say("hello , i,am  ,,,,  daryl   ,,,,, I ,can , recognize , you ,,, your ,name ,is {} ,,, and your attendace is {}".format(known_face_names[best_match_index],data[i]['total_attendance']))
    
                

            face_names.append(name)
            # espeak.synth(name) 
            text_speech.runAndWait()

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()