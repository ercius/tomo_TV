//
//  tlib.hpp
//  TV
//
//  Created by Hovden Group on 5/6/19.
//  Copyright © 2019 Jonathan Schwartz. All rights reserved.
//

#ifndef tlib_hpp
#define tlib_hpp

#include <stdio.h>
#include <Eigen/Core>
#include <Eigen/SparseCore>

void tomography(Eigen::MatrixXf& recon, Eigen::MatrixXf& tiltSeries, Eigen::VectorXf& innerProduct, Eigen::SparseMatrix<float>& A, int beta);

void tomography2D(Eigen::MatrixXf& recon, Eigen::VectorXf& b, Eigen::VectorXf& innerProduct, Eigen::SparseMatrix<float, Eigen::RowMajor>& A, int beta);

Eigen::MatrixXf tv2Dderivative(Eigen::MatrixXf recon);

float tv2D(Eigen::MatrixXf& recon);

void circshift(Eigen::MatrixXf input, Eigen::MatrixXf& output, int i, int j);

Eigen::VectorXf forwardModel(Eigen::MatrixXf input, Eigen::SparseMatrix<float, Eigen::RowMajor>& A);

float rmepsilon(float input);

void parallelRay(int& Nray, Eigen::VectorXf& angles, Eigen::SparseMatrix<float, Eigen::RowMajor>& A);

void removeBadElements(Eigen::VectorXf& xx, Eigen::VectorXf& yy, Eigen::VectorXf I);

#endif /* tlib_hpp */
