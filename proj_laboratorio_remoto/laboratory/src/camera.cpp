/**
 * Copyright (C) 2024  Felipe Bombardelli <felipebombardelli@gmail.com>
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 * 
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

// ============================================================================
//  Header
// ============================================================================

#include <stdio.h>
#include <stdlib.h>
#include <ufr.h>

#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

using namespace std;
using namespace cv;

// ============================================================================
//  main
// ============================================================================

int main() {
    link_t camera_pub = ufr_sys_publisher("camera", "@new mqtt:topic @host 185.209.160.8 @topic teste @coder msgpack:obj");

    Mat image;
    VideoCapture video(0);
    std::vector<uchar> buffer;
    buffer.reserve(1024*1024);

    while(1) {
        video >> image;
        cv::imencode(".jpg", image, buffer);
        ufr_write(&camera_pub, (const char*) &buffer[0], buffer.size());

        // Debug
        // imshow("map", image);
        waitKey(100);
        
    }
    return 0;
}