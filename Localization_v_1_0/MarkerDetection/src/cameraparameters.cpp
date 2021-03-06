/*****************************
Copyright 2011 Rafael Muñoz Salinas. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY Rafael Muñoz Salinas ''AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL Rafael Muñoz Salinas OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the
authors and should not be interpreted as representing official policies, either expressed
or implied, of Rafael Muñoz Salinas.
********************************/
#include <string>
#include <fstream>
#include <iostream>
#include "cameraparameters.h"

using namespace std;
using namespace cv;

namespace aruco
{


CameraParameters::CameraParameters()
{
    CameraMatrix = Mat();
    Distorsion = Mat();
    CamSize = Size(-1, -1);
    xi = 0;
}

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated"
CameraParameters::CameraParameters(Mat cameraMatrix, Mat distorsionCoeff, Size size, double xi) throw(Exception)
{
    setParams(cameraMatrix, distorsionCoeff, size, xi);
    #pragma GCC diagnostic pop
}


CameraParameters::CameraParameters(const CameraParameters &CI)
{
    CI.CameraMatrix.copyTo(CameraMatrix);
    CI.Distorsion.copyTo(Distorsion);
    CamSize = CI.CamSize;
    xi = CI.xi;
}


CameraParameters &CameraParameters::operator=(const CameraParameters &CI)
{
    CI.CameraMatrix.copyTo(CameraMatrix);
    CI.Distorsion.copyTo(Distorsion);
    CamSize = CI.CamSize;
    xi = CI.xi;
    return *this;
}

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated"
void CameraParameters::setParams(Mat cameraMatrix, Mat distorsionCoeff, Size size, double xi) throw(Exception)
{
    if(cameraMatrix.rows != 3 || cameraMatrix.cols != 3)
        throw Exception(9000, "invalid input cameraMatrix", "CameraParameters::setParams", __FILE__, __LINE__);
    cameraMatrix.convertTo(CameraMatrix, CV_64FC1);
    if(distorsionCoeff.total() < 4 ||  distorsionCoeff.total() >= 7)
        throw Exception(9000, "invalid input distorsionCoeff", "CameraParameters::setParams", __FILE__, __LINE__);
    distorsionCoeff.convertTo(Distorsion, CV_64FC1);
    CamSize = size;
    this->xi = xi;
    #pragma GCC diagnostic pop
}

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated"
void CameraParameters::readFromFile(string path)throw(Exception)
{
    FileStorage fs(path, FileStorage::READ);

    if(!fs.isOpened()) throw Exception(9005, "could not open file:" + path, "CameraParameters::readFromFile", __FILE__, __LINE__);

    fs["camera_matrix"] >> CameraMatrix;
    fs["distortion_coefficients"] >> Distorsion;
    fs["xi"] >> xi;
    fs["image_width"] >> CamSize.width;
    fs["image_height"] >> CamSize.height;
    fs.release();

    CameraMatrix.convertTo(CameraMatrix, CV_64FC1);
    Distorsion.convertTo(Distorsion, CV_64FC1);
    #pragma GCC diagnostic pop
}

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated"
void CameraParameters::resize(Size size)throw(Exception)
{
    if(!isValid())  throw Exception(9007, "invalid object", "CameraParameters::resize", __FILE__, __LINE__);
    if(size == CamSize) return;
    //now, read the camera size
    //resize the camera parameters to fit this image size
    double AxFactor = double(size.width) / double(CamSize.width);
    double AyFactor = double(size.height) / double(CamSize.height);
    CameraMatrix.at<double>(0, 0) *= AxFactor;
    CameraMatrix.at<double>(0, 2) *= AxFactor;
    CameraMatrix.at<double>(1, 1) *= AyFactor;
    CameraMatrix.at<double>(1, 2) *= AyFactor;
    #pragma GCC diagnostic pop
}


};
