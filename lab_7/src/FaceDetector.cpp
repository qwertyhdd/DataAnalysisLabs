#include "FaceDetector.hpp"

FaceDetector::FaceDetector() {
    net = cv::dnn::readNetFromCaffe(
        "deploy.prototxt",
        "res10_300x300_ssd_iter_140000.caffemodel"
    );
    running = false;
}

FaceDetector::~FaceDetector() {
    stop();
}

void FaceDetector::start() {
    running = true;
    worker = std::thread(&FaceDetector::run, this);
}

void FaceDetector::stop() {
    running = false;
    if (worker.joinable())
        worker.join();
}

void FaceDetector::setFrame(const cv::Mat& f) {
    std::lock_guard<std::mutex> lock(mtx);
    frame = f.clone();
    hasFrame = true;
}

std::vector<cv::Rect> FaceDetector::getFaces() {
    std::lock_guard<std::mutex> lock(mtx);
    return faces;
}

void FaceDetector::run() {
    while (running) {

        if (!hasFrame) {
            std::this_thread::sleep_for(std::chrono::milliseconds(5));
            continue;
        }

        cv::Mat localFrame;

        {
            std::lock_guard<std::mutex> lock(mtx);
            localFrame = frame.clone();
            hasFrame = false;
        }

        cv::Mat blob = cv::dnn::blobFromImage(
            localFrame, 1.0,
            cv::Size(300, 300),
            cv::Scalar(104, 177, 123)
        );

        net.setInput(blob);
        cv::Mat detections = net.forward();

        std::vector<cv::Rect> localFaces;

        cv::Mat detectionMat(
            detections.size[2],
            detections.size[3],
            CV_32F,
            detections.ptr<float>()
        );

        for (int i = 0; i < detectionMat.rows; i++) {
            float confidence = detectionMat.at<float>(i, 2);

            if (confidence > 0.5) {
                int x1 = detectionMat.at<float>(i, 3) * localFrame.cols;
                int y1 = detectionMat.at<float>(i, 4) * localFrame.rows;
                int x2 = detectionMat.at<float>(i, 5) * localFrame.cols;
                int y2 = detectionMat.at<float>(i, 6) * localFrame.rows;

                localFaces.push_back(cv::Rect(
                    cv::Point(x1, y1),
                    cv::Point(x2, y2)
                ));
            }
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(100));

        {
            std::lock_guard<std::mutex> lock(mtx);
            faces = localFaces;
        }
    }
}