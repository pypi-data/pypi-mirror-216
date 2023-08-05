/*
 * Copyright (c) 2017-2021 Arm Limited.
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
#ifndef ARM_COMPUTE_NEROIPOOLINGLAYERKERNEL_H
#define ARM_COMPUTE_NEROIPOOLINGLAYERKERNEL_H

#include "src/core/NEON/INEKernel.h"
namespace arm_compute
{
class ITensor;

/** Interface for the ROI pooling layer kernel */
class NEROIPoolingLayerKernel : public INEKernel
{
public:
    const char *name() const override
    {
        return "NEROIPoolingLayerKernel";
    }
    /** Default constructor */
    NEROIPoolingLayerKernel();
    /** Prevent instances of this class from being copied (As this class contains pointers) */
    NEROIPoolingLayerKernel(const NEROIPoolingLayerKernel &) = delete;
    /** Prevent instances of this class from being copied (As this class contains pointers) */
    NEROIPoolingLayerKernel &operator=(const NEROIPoolingLayerKernel &) = delete;
    /** Allow instances of this class to be moved */
    NEROIPoolingLayerKernel(NEROIPoolingLayerKernel &&) = default;
    /** Allow instances of this class to be moved */
    NEROIPoolingLayerKernel &operator=(NEROIPoolingLayerKernel &&) = default;
    /** Default destructor */
    ~NEROIPoolingLayerKernel() = default;

    /** Set the input and output tensors.
     *
     * @param[in]  input     Source tensor. Data types supported: QASYMM8/F32
     * @param[in]  rois      ROIs tensor, it is a 2D tensor of size [5, N] (where N is the number of ROIs) containing top left and bottom right corner
     *                       as coordinate of an image and batch_id of ROI [ batch_id, x1, y1, x2, y2 ]. Data types supported: U16
     * @param[out] output    Destination tensor. Data types supported: Same as @p input.
     * @param[in]  pool_info Contains pooling operation information described in @ref ROIPoolingLayerInfo.
     *
     * @note The x and y dimensions of @p output tensor must be the same as that specified by @p pool_info 's pooled
     * width and pooled height.
     * @note The z dimensions of @p output tensor and @p input tensor must be the same.
     * @note The fourth dimension of @p output tensor must be the same as the number of elements in @p rois tensor.
     */
    void configure(const ITensor *input, const ITensor *rois, const ITensor *output, const ROIPoolingLayerInfo &pool_info);

    // Inherited methods overridden:
    void run(const Window &window, const ThreadInfo &info) override;

    /** Static function to check if given info will lead to a valid configuration of @ref NEROIPoolingLayerKernel
     *
     * @param[in] input     Source tensor info. Data types supported: QASYMM8/F32.
     * @param[in] rois      ROIs tensor info. Data types supported: U16
     * @param[in] output    Destination tensor info. Data types supported: Same as @p input.
     * @param[in] pool_info Contains pooling operation information described in @ref ROIPoolingLayerInfo.
     *
     * @note The x and y dimensions of @p output tensor must be the same as @p pool_info 's pooled
     * width and pooled height.
     * @note The datatype of @p output should be the same as the datatype of @p input
     * @note The fourth dimension of @p output tensor must be the same as the number of elements in @p rois array.
     *
     * @return a Status
     */
    static Status validate(const ITensorInfo *input, const ITensorInfo *rois, const ITensorInfo *output, const ROIPoolingLayerInfo &pool_info);

private:
    const ITensor      *_input;
    const ITensor      *_rois;
    const ITensor      *_output;
    ROIPoolingLayerInfo _pool_info;
};
} // namespace arm_compute
#endif /*ARM_COMPUTE_NEROIPOOLINGLAYERKERNEL_H */
