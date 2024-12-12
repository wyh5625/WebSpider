import cv2
import numpy as np

def get_slider_shape(image_path):
    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to read")

        # 转换为灰度图像
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 使用高斯模糊减少噪声
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # 使用Canny边缘检测
        edges = cv2.Canny(blurred, 50, 150)

        cv2.imshow('Shapes', edges)
        cv2.waitKey(0)

def find_slider_and_gap(image_path, template_path):
    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to read")

    print(template_path)
    template = cv2.imread(template_path)
    # Resize the image using cv2.resize
    # image = cv2.resize(image, (width, height))

    # Convert the image to grayscale
    # gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Create a mask for white pixels
    # Here, we define white pixels as those with values close to 255
    # You can adjust the threshold as needed
    # threshold = 230  # Adjust this threshold for what you consider "white"
    # _, white_mask = cv2.threshold(gray_template, threshold, 255, cv2.THRESH_BINARY)
    #
    # # Find contours of the white pixels (optional)
    # contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #
    # # Draw contours on the original image (optional)
    # output_image = template.copy()
    # cv2.drawContours(output_image, contours, -1, (0, 255, 0), 2)  # Draw contours in green
    #
    # # Show the original image and the mask
    # cv2.imshow('Original Image', template)
    # cv2.waitKey(0)
    # cv2.imshow('White Pixels Mask', white_mask)
    # cv2.waitKey(0)
    # cv2.imshow('Contours of White Pixels', output_image)
    # cv2.waitKey(0)

    # gray_tmp = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # 使用高斯模糊减少噪声
    # blurred_tmp = cv2.GaussianBlur(gray_tmp, (5, 5), 0)

    # 使用Canny边缘检测
    edges_tmp = cv2.Canny(template, 50, 150)

    # cv2.imshow('temp', template)
    # cv2.waitKey(0)
    # cv2.imshow('Edges', edges_tmp)
    # cv2.waitKey(0)

    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用高斯模糊减少噪声
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 使用Canny边缘检测
    edges = cv2.Canny(blurred, 50, 150)

    # 获取模板图像的宽度和高度
    h, w = edges_tmp.shape[:2]
    # 进行模板匹配
    result = cv2.matchTemplate(edges, edges_tmp, cv2.TM_CCOEFF_NORMED)
    # 设置匹配阈值
    threshold = 0.1
    # yloc, xloc = np.where(result >= threshold)

    # Find the maximum value and its location in the result matrix
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Set a matching threshold
    threshold = 0.1

    # Check if the max_val meets the threshold
    # if max_val >= threshold:
        # Get the coordinates of the best match
    best_match_x, best_match_y = max_loc
    h, w = edges_tmp.shape[:2]  # Get the height and width of the template

    # Draw a rectangle around the best match
    cv2.rectangle(image, (best_match_x, best_match_y), (best_match_x + w, best_match_y + h), (0, 255, 0), 2)
    print(f"Best match found at: {best_match_x}, {best_match_y} with a value of: {max_val}")


    # 在匹配位置绘制矩形框
    # for (x, y) in zip(xloc, yloc):
    #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 显示结果
    # cv2.imshow('Detected', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return best_match_x, best_match_y

    # cv2.imshow('Edges', edges)
    # cv2.waitKey(0)
    #
    #
    #
    # # 使用轮廓检测找到滑块和缺口
    # contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #
    # # 找到最大的两个轮廓（假设滑块和缺口是最明显的两个轮廓）
    # contours = sorted(contours, key=cv2.contourArea, reverse=True)[:2]
    #
    # if len(contours) < 2:
    #     raise ValueError("Not enough contours found")
    #
    # # 计算轮廓的边界框
    # gap_box = cv2.boundingRect(contours[0])
    # slider_box = cv2.boundingRect(contours[1])
    #
    # # 计算滑块和缺口的中心点
    # slider_center = (slider_box[0] + slider_box[2] // 2, slider_box[1] + slider_box[3] // 2)
    # gap_center = (gap_box[0] + gap_box[2] // 2, gap_box[1] + gap_box[3] // 2)


    # 计算滑块和缺口在X轴上的距离
    # distance_x = abs(slider_center[0] - gap_center[0])

    # 绘制边界框和中心点
    # cv2.rectangle(image, slider_box, (0, 255, 0), 2)
    # cv2.rectangle(image, gap_box, (0, 0, 255), 2)
    # cv2.circle(image, slider_center, 5, (0, 255, 0), -1)
    # cv2.circle(image, gap_center, 5, (0, 0, 255), -1)
    # #
    # # # 显示结果图像
    # cv2.imshow('Result', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # print(f"滑块(slider_center)中心坐标: {slider_center}")
    # print(f"缺口(gap_center)中心坐标: {gap_center}")
    # # print(f"滑块和缺口在X轴上的距离: {distance_x}")
    #
    # left_x = min(slider_center[0], gap_center[0])
    # right_x = max(slider_center[0], gap_center[0])
    #
    # return left_x, right_x

def crop_shape(image_path):
    from PIL import Image

    # 打开图片
    image = Image.open(image_path)

    # 定义子图的坐标和尺寸
    x = 145
    y = 485
    width = 110
    height = 110

    # 计算右下角的坐标
    box = (x, y, x + width, y + height)

    # 使用 crop() 方法提取子图
    shape_img = image.crop(box)

    # 显示或保存子图
    # shape_img.show()  # 显示子图
    # shape_img.save('sub_image.png')  # 保存子图
    return shape_img

if __name__ == "__main__":
    # 示例使用
    # image_path = 'bg.png'
    # slider_center, gap_center, distance_x = find_slider_and_gap(image_path)
    # print(f"滑块中心坐标: {slider_center}")
    # print(f"缺口中心坐标: {gap_center}")
    # print(f"滑块和缺口在X轴上的距离: {distance_x}")
    image_path = "block_shapes.png"
    tmp_path = 'template.png'


    template = crop_shape(image_path)
    template.save(tmp_path)

    image_path = "bg.png"
    find_slider_and_gap(image_path, tmp_path)