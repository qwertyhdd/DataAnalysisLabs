#pragma once
#include <opencv2/opencv.hpp>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>

class FaceDetector {
private:
    cv::dnn::Net net;

    std::thread worker;
    std::mutex mtx;
    std::atomic<bool> running;

    cv::Mat frame;
    std::vector<cv::Rect> faces;

    bool hasFrame = false;

    void run();

public:
    FaceDetector();
    ~FaceDetector();

    void start();
    void stop();

    void setFrame(const cv::Mat& f);
    std::vector<cv::Rect> getFaces();
};