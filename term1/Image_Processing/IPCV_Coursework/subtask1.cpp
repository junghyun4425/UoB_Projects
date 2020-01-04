/*
 Name: Jeonghyun Kim
 Candidate number: 97485
 Development Environment: macOS Mojave version 10.14 / Xcode version 9.4.1
*/
#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/opencv.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>

using namespace std;
using namespace cv;

void detectAndDisplay( Mat frame );

String cascade_name = "frontalface.xml";
CascadeClassifier cascade;

int main( int argc, const char** argv )
{
    // 1. Read Input Image
    Mat frame = imread(argv[1], CV_LOAD_IMAGE_COLOR);

    // 2. Load the Strong Classifier in a structure called `Cascade'
    if( !cascade.load( cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };

    // 3. Detect Faces and Display Result
    detectAndDisplay( frame );

    // 4. Save Result Image
    imwrite( "detected.jpg", frame );

    return 0;
}

void detectAndDisplay( Mat frame )
{
    std::vector<Rect> faces;
    Mat frame_gray;

    // 1. Prepare Image by turning it into Grayscale and normalising lighting
    cvtColor( frame, frame_gray, CV_BGR2GRAY );
    equalizeHist( frame_gray, frame_gray );

    // 2. Perform Viola-Jones Object Detection
    cascade.detectMultiScale( frame_gray, faces, 1.1, 1, 0|CV_HAAR_SCALE_IMAGE, Size(50, 50), Size(500,500) );

    // 3. Print number of Faces found
    std::cout << faces.size() << std::endl;

    // 4. Draw box around faces found
    for( int i = 0; i < faces.size(); i++ )
    {
        rectangle(frame, Point(faces[i].x, faces[i].y), Point(faces[i].x + faces[i].width, faces[i].y + faces[i].height), Scalar( 0, 255, 0 ), 2);
    }

    // 5. Print F1-scroe for dart5.jpg and dart15.jpg based on human annotation.
    // dart5.jpg: the number of faces -> 11 / correct -> 11 / missed -> 0
    float tp_dart5 = 11, fp_dart5 = 4, fn_dart5 = 0;
    float precision = tp_dart5 / (tp_dart5 + fp_dart5);
    float sensitivity = tp_dart5 / (tp_dart5 + fn_dart5);
    float f1_score_5 = 2 * (precision * sensitivity) / (precision + sensitivity);

    // dart15.jpg: faces -> 3 / correct -> 2 / missed -> 1
    float tp_dart15 = 2, fp_dart15 = 2, fn_dart15 = 1;
    precision = tp_dart15 / (tp_dart15 + fp_dart15);
    sensitivity = tp_dart15 / (tp_dart15 + fn_dart15);
    float f1_score_15 = 2 * (precision * sensitivity) / (precision + sensitivity);

    // 15. Print F1-score for dart15.jpg
    cout << "F1 score for dart5.jpg: " << f1_score_5 << endl;
    cout << "F1 score for dart15.jpg: " << f1_score_15 << endl;
}
