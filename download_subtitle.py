
for movie in movies:
    page.get(movie["movie_link"])
    page.listen.start('ajax/down1_ajax')

    download_btn = page.ele('下载字幕文件')
    time.sleep(1)
    download_btn.click()


    # time.sleep(10)

    # Locate start pos of slide bar

    # 切换到 iframe
    iframe_element = page.get_frame('#tcaptcha_iframe_dy')

    if iframe_element:
        # page.switch_to_frame(iframe_element)
        time.sleep(1)

        slider = iframe_element.ele('xpath://div[@class="tc-fg-item tc-slider-normal"]')

        # 提取 BG URL
        bg_style = iframe_element.ele('xpath:.//div[@class="tc-bg-img unselectable"]').attr('style')
        bg_image_url = bg_style.split('url("')[1].split('")')[0]
        width_match = re.search(r'width:\s*([\d.]+)px', bg_style)
        height_match = re.search(r'height:\s*([\d.]+)px', bg_style)
        width = int(float(width_match.group(1)))
        height = int(float(height_match.group(1)))

        bg_img_path = "bg.png"
        if os.path.exists(bg_img_path):
            os.remove(bg_img_path)
        page.download(bg_image_url, '.', bg_img_path)

        # 提取 block shape
        shapes_style = iframe_element.eles('xpath:.//div[@class="tc-fg-item"]')[-1].attr('style')
        shape_image_url = shapes_style.split('url("')[1].split('")')[0]

        blk_img_path = "block_shapes.png"
        if os.path.exists(blk_img_path):
            os.remove(blk_img_path)
        page.download(shape_image_url, '.', blk_img_path)
        get_slider_shape(blk_img_path)

        # 提取 block URL
        fg_style = iframe_element.eles('xpath:.//div[@class="tc-fg-item"]')[1].attr('style')
        # fg_image_url = fg_style.split('url("')[1].split('")')[0]
        print(fg_style)

        # fg_img_path = "fg.png"
        # page.download(fg_image_url, '.', fg_img_path)

        # 使用正则表达式提取 left 的值
        left_value = re.search(r'left:\s*([-+]?\d*\.?\d+)', fg_style).group(1)
        width_value = re.search(r'width:\s*([-+]?\d*\.?\d+)', fg_style).group(1)
        left_value = float(left_value.replace("px", ""))
        width_value = float(width_value.replace("px", ""))
        # print("Left: ", left_value)
        # print("Width: ", width_value)
        start_x = int(25)


        image_path = "block_shapes.png"
        tmp_path = 'template.png'

        template = crop_shape(image_path)
        template.save(tmp_path)
        gap_x, _ = find_slider_and_gap(bg_img_path, tmp_path)

        # Get width of img
        image = cv2.imread(bg_img_path)
        if image is None:
            raise ValueError("Image not found or unable to read")
        # Get the dimensions of the image
        _, width_img = image.shape[:2]

        # with_img
        # slider_x = slider_x * (width/width_img)
        gap_x = gap_x * (width / width_img)

        print(f"Drag from {start_x} to {gap_x}")
        slider.drag(gap_x - start_x, 1, True)
        time.sleep(5)
    else:
        print("iframe 未找到。")

    # Wait for the AJAX response
    data = page.listen.wait()
    caption_url = data.response.body['url']
    print("caption_url: ", caption_url)


