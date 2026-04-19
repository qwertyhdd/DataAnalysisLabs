#include <opencv2/opencv.hpp>
#include <chrono>
#include "CameraProvider.hpp"
#include "FrameProcessor.hpp"
#include "KeyProcessor.hpp"
#include "Display.hpp"
#include "FaceDetector.hpp"

cv::Point startPoint, endPoint;
bool drawing = false;

void mouseCallback(int event, int x, int y, int flags, void* userdata) {
    if (event == cv::EVENT_LBUTTONDOWN) {
        drawing = true;
        startPoint = cv::Point(x,y);
    }
    else if (event == cv::EVENT_MOUSEMOVE && drawing) {
        endPoint = cv::Point(x,y);
    }
    else if (event == cv::EVENT_LBUTTONUP) {
        drawing = false;
        endPoint = cv::Point(x,y);
    }
}

int main() {
    CameraProvider camera;
    FrameProcessor processor;
    KeyProcessor keyProcessor;
    Display display;
    FaceDetector detector;
    detector.start();

    if (!camera.isOpened()) return -1;

    cv::namedWindow("Camera");
    cv::setMouseCallback("Camera", mouseCallback);

    int brightness = 50;
    cv::createTrackbar("Brightness", "Camera", &brightness, 100, FrameProcessor::onTrackbar, &processor);

    auto lastTime = std::chrono::high_resolution_clock::now();

    while (true) {
        cv::Mat frame = camera.getFrame();
        if (frame.empty()) break;

        cv::Mat processed;

        if (keyProcessor.getMode() == KeyProcessor::FACE) {
            processed = frame.clone();

            detector.setFrame(frame);
            auto faces = detector.getFaces();

            for (auto &f : faces)
                cv::rectangle(processed, f, cv::Scalar(0,255,0), 2);

        } else {
            processed = processor.process(frame, keyProcessor.getMode());
        }

        auto now = std::chrono::high_resolution_clock::now();
        double fps = 1000.0 / std::chrono::duration_cast<std::chrono::milliseconds>(now - lastTime).count();
        lastTime = now;

        cv::putText(processed, "FPS: " + std::to_string((int)fps),
                    cv::Point(10,30), cv::FONT_HERSHEY_SIMPLEX,
                    1, cv::Scalar(0,255,0), 2);

        if (drawing) {
            cv::rectangle(processed, startPoint, endPoint, cv::Scalar(0,0,255), 2);
        }

        display.show(processed);

        int key = cv::waitKey(30);
        if (key == 27) break;
        keyProcessor.processKey(key);
    }
    detector.stop();

    return 0;
}