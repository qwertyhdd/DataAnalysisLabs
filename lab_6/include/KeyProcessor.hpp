#pragma once

class KeyProcessor {
public:
    enum Mode {
        NORMAL,
        GRAY,
        BLUR,
        CANNY,
        INVERT,
        THRESH,
        SOBEL
    };

private:
    Mode currentMode;

public:
    KeyProcessor();
    void processKey(int key);
    Mode getMode();
};