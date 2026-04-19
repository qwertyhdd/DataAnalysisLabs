#pragma once
#include <opencv2/opencv.hpp>
#include "KeyProcessor.hpp"

class FrameProcessor {
private:
    int brightness;

public:
    FrameProcessor();
    static void onTrackbar(int value, void* userdata);

    cv::Mat process(const cv::Mat& frame, KeyProcessor::Mode mode);
    void setBrightness(int value);
};