/*
 * Copyright (c) 2018-2019 Arm Limited.
 *
 * SPDX-License-Identifier: MIT
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
#ifndef ARM_COMPUTE_TEST_WINOGRAD_H
#define ARM_COMPUTE_TEST_WINOGRAD_H

#include "arm_compute/core/TensorShape.h"

#include "tests/SimpleTensor.h"

namespace arm_compute
{
namespace test
{
namespace validation
{
namespace reference
{
/** Winograd transform type */
enum class WinogradTransformType
{
    INPUT,  /**< Winograd input transform */
    FILTER, /**< Winograd filter transform */
    OUTPUT  /**< Winograd output transform */
};

template <typename T>
SimpleTensor<T> winograd_input_transform(const SimpleTensor<T> &in, const TensorShape &output_shape, const WinogradInfo &winograd_info);

template <typename T>
SimpleTensor<T> winograd_filter_transform(const SimpleTensor<T> &in, const TensorShape &output_shape, const WinogradInfo &winograd_info);

template <typename T>
SimpleTensor<T> winograd_output_transform(const SimpleTensor<T> &in, const SimpleTensor<T> &b, const TensorShape &output_shape, const WinogradInfo &winograd_info);
} // namespace reference
} // namespace validation
} // namespace test
} // namespace arm_compute
#endif /* ARM_COMPUTE_TEST_WINOGRAD_H */
