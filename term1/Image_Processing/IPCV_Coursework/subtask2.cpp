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

String cascade_name = "cascade.xml";
CascadeClassifier cascade;

int image_number;

int main( int argc, const char** argv )
{
    // 1. Read Input Image
    Mat frame = imread(argv[1], CV_LOAD_IMAGE_COLOR);

    // 1-1. Get the image number
    string str = argv[1];
    size_t pos = str.find("dart");
    str = str.substr(pos + 4);
    if(str[1] == '.') {
        image_number = str[0] - '0';
    } else {
        image_number = ((str[0] - '0') * 10) + (str[1] - '0');
    }

    // 2. Load the Strong Classifier in a structure called `Cascade'
    if( !cascade.load( cascade_name ) ){ printf("--(!)Error loading\n"); return -1; };

    // 3. Detect Darts and Display Result
    detectAndDisplay( frame );

    // 4. Save Result Image
    imwrite( "detected.jpg", frame );

    return 0;
}

void detectAndDisplay( Mat frame )
{
    std::vector<Rect> darts;
    Mat frame_gray;
    int *coord, ndart;
    double tp = 0.0, fp = 0.0, fn = 0.0;

    ifstream dataset ( "DartDataCommaBased.csv" );
    if (!dataset) {
        cout << "File not opened!" << endl;
    }

    string line;
    char tk = ',';
    string s;
    // Find image number e.g. dart(n).jpg from csv data
    for(int i = 0; i <= (image_number + 1); i++) {
        getline(dataset, line);
    }
    // Split line by token
    istringstream data_line(line);
    // Image name, The number of darts
    getline(data_line, s, tk);
    getline(data_line, s, tk);
    ndart = stoi(s);
    coord = new int[ndart];

    // Get x, y coordinates of the answer.
    for(int i = 0; i < ndart * 4; i++) {
        getline(data_line, s, tk);
        coord[i] = stoi(s);
    }

    // 1. Prepare Image by turning it into Grayscale and normalising lighting
    cvtColor( frame, frame_gray, CV_BGR2GRAY );
    equalizeHist( frame_gray, frame_gray );

    // 2. Perform Viola-Jones Object Detection
    cascade.detectMultiScale( frame_gray, darts, 1.1, 1, 0|CV_HAAR_SCALE_IMAGE, Size(50, 50), Size(500,500) );

    // 3. Print number of Darts found
    for(int i = 0; i < ndart * 4; i += 4) {
        for(int j = 0; j < darts.size(); j++) {
            if(darts[j].x <= coord[i] && darts[j].y <= coord[i+1] && (darts[j].x + darts[j].width) >= coord[i+2] &&
               (darts[j].y + darts[j].height) >= coord[i+3]) {
                tp++;
                break;
            }
        }
    }

    // 4. Draw box around darts found
    for( int i = 0; i < darts.size(); i++ ) {
        rectangle(frame, Point(darts[i].x, darts[i].y), Point(darts[i].x + darts[i].width, darts[i].y + darts[i].height), Scalar( 0, 255, 0 ), 2);
    }

    // 5. Draw box annotated darts
    for (int i = 0; i < ndart * 4; i += 4) {
        rectangle(frame, Point(coord[i], coord[i+1]), Point(coord[i+2], coord[i+3]), Scalar(255, 0, 0), 2);
    }

    // 6. Print all scores
    fp = (double) darts.size() - tp;
    fn = (double) ndart - tp;

    double precision = tp / (tp + fp);
    double sensitivity = tp / (tp + fn);
    double f1_score = 2.0 * (precision * sensitivity) / (precision + sensitivity);

    cout << "Real number of darts: " << ndart << endl;
    cout << "Predicted number of darts: " << darts.size() << endl;
    cout << "tp = " << tp << ", fp = " << fp << ", fn = " << fn << endl;
    cout << "F1-score: " << f1_score << endl;
}
