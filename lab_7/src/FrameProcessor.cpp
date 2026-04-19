#include "FrameProcessor.hpp"

FrameProcessor::FrameProcessor() {
    brightness = 50;
}

void FrameProcessor::setBrightness(int value) {
    brightness = value;
}

void FrameProcessor::onTrackbar(int value, void* userdata) {
    FrameProcessor* fp = static_cast<FrameProcessor*>(userdata);
    fp->setBrightness(value);
}

cv::Mat FrameProcessor::process(const cv::Mat& frame, KeyProcessor::Mode mode) {
    cv::Mat result, temp;

    frame.convertTo(temp, -1, 1, brightness - 50);

    switch (mode) {
        case KeyProcessor::GRAY:
            cv::cvtColor(temp, result, cv::COLOR_BGR2GRAY);
            break;

        case KeyProcessor::BLUR:
            cv::GaussianBlur(temp, result, cv::Size(15,15), 0);
            break;

        case KeyProcessor::CANNY:
            cv::Canny(temp, result, 100, 200);
            break;

        case KeyProcessor::INVERT:
            cv::bitwise_not(temp, result);
            break;

        case KeyProcessor::THRESH:
            cv::cvtColor(temp, temp, cv::COLOR_BGR2GRAY);
            cv::threshold(temp, result, 127, 255, cv::THRESH_BINARY);
            break;

        case KeyProcessor::SOBEL:
            cv::Sobel(temp, result, CV_8U, 1, 1);
            break;

        default:
            result = temp.clone();
    }

    return result;
}