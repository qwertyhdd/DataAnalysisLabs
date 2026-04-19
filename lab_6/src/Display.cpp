#include "Display.hpp"

void Display::show(const cv::Mat& frame) {
    cv::imshow("Camera", frame);
}