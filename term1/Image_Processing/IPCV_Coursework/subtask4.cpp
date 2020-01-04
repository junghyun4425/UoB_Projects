/*
 Name: Jeonghyun Kim
 Candidate number: 97485
 Development Environment: macOS Mojave version 10.14 / Xcode version 9.4.1
 */
#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>

# define PI 3.141593

using namespace cv;
using namespace std;

void Threshold(cv::Mat &input, int threshold_val);
void SobelFilter(cv::Mat &input, cv::Mat &sobel_mag, cv::Mat &sobel_grad);
void SobelDiff(cv::Mat &input, cv::Mat &dx, cv::Mat &dy);
void SobelMag(cv::Mat &dx, cv::Mat &dy, cv::Mat &sobel_mag);
void SobelGrad(cv::Mat &dx, cv::Mat &dy, cv::Mat &sobel_grad);
void HoughTransformLine(cv::Mat &sobel_mag, cv::Mat &sobel_grad, int threshold, int min_theta, int max_theta, cv::Mat &hough_line);
void HoughTransformCircle(cv::Mat &sobel_mag, cv::Mat &sobel_grad, int threshold, int min_rad, int max_rad, cv::Mat &hough_circle);
void Hough3DTo2D(cv::Mat &hough_3d, cv::Mat &hough_2d);
void LogTransform(cv::Mat &input, cv::Mat &output);
void detectAndDisplay( Mat frame );
void ImageEnhance(cv::Mat &input, double alpha, int beta, cv::Mat &output);

String cascade_name = "cascade.xml";
CascadeClassifier cascade;

// Controlling Values
int image_number;
int thresh_mag = 80;
int thresh_hough = 90;
int thresh_after_log = 230;
int min_rad = 10;
int max_rad = 90;
double center_percent = 0.25;

int main( int argc, const char** argv )
{
    // 1-1. Read Input Image
    Mat frame = imread(argv[1], CV_LOAD_IMAGE_COLOR);
    
    // 1-2. Get the image number
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
    int pred_ndart = 0;
    bool *map;
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
    
    // 1. Prepare Image by turning it into Grayscale and normalising lighting + image Enhancement
    Mat frame2;
    ImageEnhance(frame, 1.5, 50, frame2);
    cvtColor( frame2, frame_gray, CV_BGR2GRAY );
    equalizeHist( frame_gray, frame_gray );
    
    // 2-1. Perform Viola-Jones Object Detection
    cascade.detectMultiScale( frame_gray, darts, 1.1, 1, 0|CV_HAAR_SCALE_IMAGE, Size(50, 50), Size(500,500) );
    
    // 2-2. Applying Sobel Filter to get edges
    Mat sobel_mag, sobel_grad;
    SobelFilter(frame_gray, sobel_mag, sobel_grad);
    Threshold(sobel_mag, thresh_mag);
    
    // 2-3. Adopt Hough Transform
    Mat hough_circle, hough_2d, hough_2d_log;
    HoughTransformCircle(sobel_mag, sobel_grad, thresh_hough, min_rad, max_rad, hough_circle);
    Hough3DTo2D(hough_circle, hough_2d);
    imwrite("hough_transform.jpg", hough_2d);
    LogTransform(hough_2d, hough_2d_log);
    Threshold(hough_2d_log, thresh_after_log);
    imwrite("thresholded_hough_log.jpg", hough_2d_log);
    
    // 2-4. Erase rectanles with applying center of HT
    // map is check the rectangles
    map = new bool[darts.size()];
    for(int i = 0; i < darts.size(); i++) map[i] = false;
    
    // Find values from hough space
    int dots;
    for( int i = 0; i < darts.size(); i++ ) {
        dots = 0;
        double margine = (1 - center_percent) / 2;
        // Reduce boxes' size to check on hough space.
        int cen_pos_x0 = round((double)darts[i].x + (double)darts[i].width * margine);
        int cen_pos_y0 = round((double)darts[i].y + (double)darts[i].height * margine);
        
        int cen_pos_x1 = round((double)darts[i].x + (double)darts[i].width * (margine + center_percent));
        int cen_pos_y1 = round((double)darts[i].y + (double)darts[i].height * (margine + center_percent));
        
        // Find values from hough space
        for(int j = cen_pos_x0; j < cen_pos_x1; j++) {
            for(int k = cen_pos_y0; k < cen_pos_y1; k++) {
                if(hough_2d_log.at<uchar>(k, j) > thresh_after_log) {
                    dots++;
                }
            }
        }
        if(dots > 5) {
            map[i] = true;
        }
    }
    
    // The number of 'true' in map is our prediction.
    for(int i = 0; i < darts.size(); i++) {
        if(map[i] == true) pred_ndart++;
    }
    // 3. Print number of Darts found
    for(int i = 0; i < ndart * 4; i += 4) {
        for(int j = 0; j < darts.size(); j++) {
            if(map[j] != true) continue;
            if(darts[j].x <= coord[i] && darts[j].y <= coord[i+1] && (darts[j].x + darts[j].width) >= coord[i+2] &&
               (darts[j].y + darts[j].height) >= coord[i+3]) {
                tp++;
                break;
            }
        }
    }
    
    // 4. Draw box around darts found & count boxs
    for( int i = 0; i < darts.size(); i++ ) {
        if(map[i] == true)
            rectangle(frame, Point(darts[i].x, darts[i].y), Point(darts[i].x + darts[i].width, darts[i].y + darts[i].height), Scalar( 0, 255, 0 ), 2);
    }
    
    // 5. Draw box annotated darts
    for (int i = 0; i < ndart * 4; i += 4) {
        rectangle(frame, Point(coord[i], coord[i+1]), Point(coord[i+2], coord[i+3]), Scalar(255, 0, 0), 2);
    }
    
    // 6. Print all scores
    fp = (double) pred_ndart - tp;
    fn = (double) ndart - tp;
    
    double precision = tp / (tp + fp);
    double sensitivity = tp / (tp + fn);
    double f1_score = 2.0 * (precision * sensitivity) / (precision + sensitivity);
    
    cout << "Real number of darts: " << ndart << endl;
    cout << "Predicted number of darts: " << pred_ndart << endl;
    cout << "tp = " << tp << ", fp = " << fp << ", fn = " << fn << endl;
    cout << "Precision: " << precision << endl;
    cout << "Recall: " << sensitivity << endl;
    cout << "F1-score: " << f1_score << endl;
}

void Threshold(cv::Mat &input, int threshold_val) {
    input.convertTo(input, CV_8U);
    for(int i = 0; i < (input.rows); i++) {
        for(int j = 0; j < (input.cols); j++) {
            int imageval = (int) input.at<uchar>(i ,j);
            if(imageval < threshold_val) imageval = 0;
            input.at<uchar>(i, j) = (uchar) imageval;
        }
    }
}

void SobelFilter(cv::Mat &input, cv::Mat &sobel_mag, cv::Mat &sobel_grad) {
    Mat dx, dy;
    
    SobelDiff(input, dx, dy);
    SobelMag(dx, dy, sobel_mag);
    SobelGrad(dx, dy, sobel_grad);
    
    // Drawing magnitude * gradient image
    Mat sobel_mag_grad;
    sobel_mag_grad.create(sobel_mag.size(), sobel_mag.type());
    for(int i = 0; i < sobel_mag.size[0]; i++) {
        for(int j = 0; j < sobel_mag.size[1]; j++) {
            sobel_mag_grad.at<uchar>(i, j) = (uchar)((double)sobel_mag.at<uchar>(i, j) * sobel_grad.at<double>(i, j) * PI / 180);
        }
    }
    Threshold(sobel_mag_grad, thresh_mag);
    imwrite("sobel_mag_grad.jpg", sobel_mag_grad);
}

void SobelDiff(cv::Mat &input, cv::Mat &dx, cv::Mat &dy) {
    // set kernels as array for makeing matrix
    int kernelx_arr[] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};
    int kernely_arr[] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};
    
    // make kernel for dx and dy
    Mat kernelx(3, 3, CV_32F, kernelx_arr);
    Mat kernely(3, 3, CV_32F, kernely_arr);
    
    dx.create(input.size(), CV_32F);
    dy.create(input.size(), CV_32F);
    
    int kernelRadiusX = (kernelx.size[0] - 1) / 2;
    int kernelRadiusY = (kernely.size[1] - 1) / 2;
    
    cv::Mat paddedInput;
    cv::copyMakeBorder(input, paddedInput, kernelRadiusX, kernelRadiusX, kernelRadiusY, kernelRadiusY, cv::BORDER_REPLICATE);
    
    for (int i = 0; i < input.rows; i++) {
        for (int j = 0; j < input.cols; j++) {
            int sum_dx = 0;
            int sum_dy = 0;
            for (int m = -kernelRadiusX; m <= kernelRadiusX; m++) {
                for (int n = -kernelRadiusY; n <= kernelRadiusY; n++) {
                    // find the correct indices we are using
                    int imagex = i + m + kernelRadiusX;
                    int imagey = j + n + kernelRadiusY;
                    int kernelxval = m + kernelRadiusX;
                    int kernelyval = n + kernelRadiusY;
                    
                    // get the values from the padded image and the kernel
                    int imageval = (int)paddedInput.at<uchar>(imagex, imagey);
                    int kernalval_dx = kernelx.at<int>(kernelxval, kernelyval);
                    int kernalval_dy = kernely.at<int>(kernelxval, kernelyval);
                    
                    // do the multiplication
                    sum_dx += imageval * kernalval_dx;
                    sum_dy += imageval * kernalval_dy;
                }
            }
            // set the output value as the sum of the convolution
            dx.at<int>(i, j) = sum_dx;
            dy.at<int>(i, j) = sum_dy;
        }
    }
}

void SobelMag(cv::Mat &dx, cv::Mat &dy, cv::Mat &sobel_mag) {
    // Create magitude matrix same as input type & size
    sobel_mag.create(dx.size(), CV_8U);
    
    // Find out min & max magnitude.
    for (int i = 0; i < dx.rows; i++) {
        for (int j = 0; j < dx.cols; j++) {
            int dx_value = dx.at<int>(i, j);
            int dy_value = dy.at<int>(i, j);
            
            int mag = sqrt(dx_value * dx_value + dy_value * dy_value);
            sobel_mag.at<uchar>(i, j) = (uchar)mag;
        }
    }
}

void SobelGrad(cv::Mat &dx, cv::Mat &dy, cv::Mat &sobel_grad) {
    // Create gradient matrix same as input size, but type is double to calculate sin and cos later
    sobel_grad.create(dx.size(), CV_64F);
    
    for (int i = 0; i < dx.rows; i++) {
        for (int j = 0; j < dx.cols; j++) {
            int dx_value = dx.at<int>(i, j);
            int dy_value = dy.at<int>(i, j);
            
            // Compute gradient
            double angle = atan2(dy_value, dx_value);
            
            sobel_grad.at<double>(i, j) = angle;
        }
    }
}

void HoughTransformLine(cv::Mat &sobel_mag, cv::Mat &sobel_grad, int threshold, int min_theta, int max_theta, cv::Mat &hough_line) {
    int row = sobel_mag.size().height;
    int col = sobel_mag.size().width;
    
    int center_x = row / 2;
    int center_y = col / 2;
    
    int rho_size = sqrt(row * row + col * col) / 2.0;
    int theta_size = 180; //max_theta - min_theta;
    
    int size[] = {rho_size, theta_size};
    hough_line.create(2, size, CV_32SC1);
    
    // Initialisation of 2d matrix
    for (int r = 0; r < rho_size; ++r)
        for (int t = 0; t < theta_size; ++t)
            hough_line.at<uchar>(r, t) = 0;
    
    for (int y = 0; y < col; ++y) {
        for (int x = 0; x < row; ++x) {
            if(sobel_mag.at<uchar>(x, y) > threshold) {
                for(int t = 0; t < theta_size; t++) {
                    int rho = round(((double)x - center_x) * cos((double)t * (PI / 180.0))) + (((double)y - center_y) * sin((double)t * (PI / 180.0)));
                    if(rho < 0) {
                        continue;
                    }
                    hough_line.at<int>(rho, t)++;
                }
            }
        }
    }
}

void HoughTransformCircle(cv::Mat &sobel_mag, cv::Mat &sobel_grad, int threshold, int min_rad, int max_rad, cv::Mat &hough_circle) {
    int rad = max_rad - min_rad + 1;
    int row = sobel_mag.size().height;
    int col = sobel_mag.size().width;
    
    int size[3] = {rad, row, col};
    hough_circle.create(3, size, CV_32SC1);
    
    // Initialisation of 3d matrix
    for(int r = 0; r < rad; ++r)
        for (int x = 0; x < row; ++x)
            for (int y = 0; y < col; ++y)
                hough_circle.at<int>(r, x, y) = 0;
    
    for(int r = 0; r < rad; ++r) {
        int r_val = r + min_rad;
        for(int x = 0; x < row; ++x) {
            for (int y = 0; y < col; ++y) {
                if (sobel_mag.at<uchar>(x, y) > threshold) {
                    // plus
                    int x_val1 = (int)(x + r_val * sin(sobel_grad.at<double>(x,y)));
                    int y_val1 = (int)(y + r_val * cos(sobel_grad.at<double>(x,y)));
                    
                    // minus
                    int x_val2 = (int)(x - r_val * sin(sobel_grad.at<double>(x,y)));
                    int y_val2 = (int)(y - r_val * cos(sobel_grad.at<double>(x,y)));
                    
                    if ((x_val1 < 0) || (x_val1 >= row) || (y_val1 < 0) || (y_val1 >= col)
                        || (x_val2 < 0) || (x_val2 >= row) || (y_val2 < 0) || (y_val2 >= col))
                        continue;
                    
                    hough_circle.at<int>(r, x_val1, y_val1)++;
                    hough_circle.at<int>(r, x_val2, y_val2)++;
                }
            }
        }
    }
}

void Hough3DTo2D(cv::Mat &hough_3d, cv::Mat &hough_2d) {
    int size[] = {hough_3d.size[1], hough_3d.size[2]};
    hough_2d.create(2, size, CV_8U);
    
    for (int i = 0; i < hough_3d.size[1]; ++i) {
        for (int j = 0; j < hough_3d.size[2]; ++j) {
            hough_2d.at<uchar>(i, j) = (uchar)0;
        }
    }
    
    for (int k = 0; k < hough_3d.size[0]; ++k) {
        for (int i = 0; i < hough_3d.size[1]; ++i) {
            for (int j = 0; j < hough_3d.size[2]; ++j) {
                int sum = (int)hough_2d.at<uchar>(i, j) + hough_3d.at<int>(k,i,j);
                if(sum > 255) sum = 255;
                hough_2d.at<uchar>(i, j) = (uchar)sum;
            }
        }
    }
}

void LogTransform(cv::Mat &input, cv::Mat &output) {
    
    // logarithmic Scale
    input.convertTo(output, CV_32F);
    log((output + 1), output);
    convertScaleAbs(output, output);
    normalize(output, output, 0, 255, cv::NORM_MINMAX);
    
    // Linear Scale
    //input.convertTo(output, CV_32S);
    //output = output * 2;
}

void ImageEnhance(cv::Mat &input, double alpha, int beta, cv::Mat &output) {
    output.create(input.size(), input.type());
    for(int y = 0; y < input.rows; y++) {
        for(int x = 0; x < input.cols; x++) {
            for(int c = 0; c < input.channels(); c++) {
                output.at<Vec3b>(y,x)[c] = saturate_cast<uchar>(alpha * input.at<Vec3b>(y,x)[c] + beta);
            }
        }
    }
}
