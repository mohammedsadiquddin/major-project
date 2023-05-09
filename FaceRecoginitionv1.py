# -*- coding: utf-8 -*-
import time
import face_recognition
import cv2
import numpy as np
# import espeak
import pyttsx3
import json
import datetime

# using now() to get current time
current_time = datetime.datetime.now()

text_speech=pyttsx3.init()

video_capture = cv2.VideoCapture(0)
#list of known family members for 
# Family member 1
sadiq_image = face_recognition.load_image_file("sadiq.jpg")
sadiq_face_encoding = face_recognition.face_encodings(sadiq_image)[0]

#Family member 2

irfan_image = face_recognition.load_image_file("irfan.jpg")
irfan_face_encoding = face_recognition.face_encodings(irfan_image)[0]


shoaib_image = face_recognition.load_image_file("shoaib.jpg")
shoaib_face_encoding = face_recognition.face_encodings(shoaib_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    sadiq_face_encoding,
    irfan_face_encoding,
    shoaib_face_encoding
]
known_face_names = [
    "sadiq",
    "irfan",
    "shoaib"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            
            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                    # Load data from the JSON file
                with open("data.json", "r") as infile:
                    data = json.load(infile)

                for i in range(len(data)):
                     # Get the attendance data for this person
                    # name = data[i]["name"]
                    # total_attendance = data[i]["total_attendance"]

                    # print(data[i]['name'])
                    if name == data[i]['name']:
                                new_date="{}-{}-{}".format(current_time.day,current_time.month,current_time.year)
                                last_date = data[i]["present"][-1]
                                if last_date == new_date:
                                    print("your attendance is already recorded")
                                    text_speech.say(" {} your attendance is already recorded for today ,,, and your total attendance is {}".format(known_face_names[best_match_index],data[i]['total_attendance']))
                                    time.sleep(5)
                                    break
                                else:
                                    print("recording your attendance")
                                    
                                    data[i]["total_attendance"] += 1
                                    
                                    # new_date="{}-{}-{}".format(current_time.day,current_time.month,current_time.year) 

                          
                                    # new_entry = {"date": new_date} 

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