#include "KeyProcessor.hpp"

KeyProcessor::KeyProcessor() {
    currentMode = NORMAL;
}

void KeyProcessor::processKey(int key) {
    switch (key) {
        case '1': currentMode = NORMAL; break;
        case '2': currentMode = GRAY; break;
        case '3': currentMode = BLUR; break;
        case '4': currentMode = CANNY; break;
        case '5': currentMode = INVERT; break;
        case '6': currentMode = THRESH; break;
        case '7': currentMode = SOBEL; break;
        case 'f': currentMode = FACE; break;
        case 'F': currentMode = FACE; break;
    }
}

KeyProcessor::Mode KeyProcessor::getMode() {
    return currentMode;
}